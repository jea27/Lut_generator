"""Bound streamed input before parsing, independently of Content-Length claims."""
from fastapi import HTTPException
from starlette.responses import JSONResponse


class RequestLimits:
    def __init__(self, app, capacity=4):
        self.app, self.capacity, self.active = app, capacity, 0

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http' or not scope['path'].startswith('/api/'):
            return await self.app(scope, receive, send)
        write = scope['method'] not in ('GET', 'HEAD', 'OPTIONS')
        headers = scope.get('headers', [])
        lengths = [v for k, v in headers if k.lower() == b'content-length']
        limit = 33 * 1024 * 1024 if scope['path'] == '/api/images' else 64 * 1024
        if write:
            if len(lengths) > 1 or lengths and (not lengths[0].isdigit() or len(lengths[0]) > 12):
                return await JSONResponse({'detail': 'Invalid Content-Length'}, 400)(scope, receive, send)
            if not lengths and scope['method'] != 'DELETE':
                return await JSONResponse({'detail': 'Content-Length required'}, 411)(scope, receive, send)
            declared = int(lengths[0]) if lengths else 0
            if declared > limit:
                return await JSONResponse({'detail': 'Request exceeds local size limit'}, 413)(scope, receive, send)
        else:
            declared = limit
        heavy = write and (scope['path'] in ('/api/images', '/api/fit', '/api/preview', '/api/planner')
                           or scope['path'].startswith('/api/export/'))
        if heavy and self.active >= self.capacity:
            return await JSONResponse({'detail': 'Local engine busy; retry after current operations'}, 429)(scope, receive, send)
        if heavy:
            self.active += 1
        count = 0

        async def bounded_receive():
            nonlocal count
            message = await receive()
            if message['type'] == 'http.request':
                count += len(message.get('body', b''))
                if count > min(limit, declared):
                    raise HTTPException(413, 'Request exceeds declared/local size limit')
            return message

        try:
            await self.app(scope, bounded_receive, send)
        finally:
            if heavy:
                self.active -= 1
