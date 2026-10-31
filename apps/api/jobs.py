"""One serial batch worker, durable status, cooperative cancellation, private outputs."""
import hashlib
import json
import threading
import uuid
from pathlib import Path
from packages.colour_core import engine, image_io
from .storage import atomic_json


class Jobs:
    def __init__(self,root,processing_lock):
        self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True)
        self.processing_lock=processing_lock;self.mutex=threading.RLock();self.records={};self.cancel_events={}
        for path in self.root.glob('*/job.json'):
            try:
                record=json.loads(path.read_bytes())
                if record['status'] in ('queued','running','cancelling'):
                    record.update(status='interrupted',message='Previous operation was interrupted; retry creates a new batch')
                    atomic_json(path,record)
                self.records[record['id']]=record
            except (ValueError,KeyError,OSError):continue

    def save(self,record):atomic_json(self.root/record['id']/'job.json',record)

    def get(self,identifier):
        with self.mutex:
            if identifier not in self.records:raise KeyError(identifier)
            return json.loads(json.dumps(self.records[identifier]))

    def active(self):
        with self.mutex:return any(r['status'] in ('queued','running','cancelling') for r in self.records.values())

    def start(self,ids,recipe,format,resolve):
        recipe=engine.validate_recipe(recipe)
        with self.mutex:
            if self.active():raise ValueError('A batch is active; cancel or wait before starting another')
            identifier=str(uuid.uuid4());event=threading.Event()
            record={'id':identifier,'status':'queued','progress':0,'total':len(ids),'completed':0,
                    'format':format,'source_ids':ids,'recipe':recipe.model_dump(),'items':[], 'message':''}
            self.records[identifier]=record;self.cancel_events[identifier]=event;self.save(record)
        def worker():
            with self.mutex:record['status']='running';self.save(record)
            try:
                for index,source in enumerate(ids):
                    if event.is_set():raise engine.ProcessingCancelled()
                    try:
                        with self.processing_lock:
                            rgb,alpha,_=image_io.decode(resolve(source).read_bytes())
                            def progress(fraction):
                                with self.mutex:record['progress']=round((index+fraction)/len(ids)*100,1)
                            output=engine.render(rgb,recipe,cancel=event.is_set,progress=progress,alpha=alpha)
                            payload=image_io.encode(output,alpha,'PNG' if format=='png' else 'JPEG')
                            if event.is_set():raise engine.ProcessingCancelled()
                            filename=f'batch-{index+1:03d}.{format}';destination=self.root/identifier/filename
                            temporary=destination.with_suffix(destination.suffix+'.part')
                            try:
                                with temporary.open('xb') as stream:stream.write(payload)
                                if event.is_set():raise engine.ProcessingCancelled()
                                temporary.rename(destination)
                            finally:temporary.unlink(missing_ok=True)
                        item={'index':index,'status':'completed','filename':filename,'sha256':hashlib.sha256(payload).hexdigest()}
                    except engine.ProcessingCancelled:raise
                    except (ValueError,OSError):item={'index':index,'status':'failed','message':'Cannot process this input; verify format, size and disk space'}
                    with self.mutex:
                        record['items'].append(item);record['completed']=len(record['items']);self.save(record)
                with self.mutex:
                    record.update(status='completed_with_errors' if any(i['status']=='failed' for i in record['items']) else 'completed',progress=100)
            except engine.ProcessingCancelled:
                with self.mutex:record.update(status='cancelled',message='Cancelled; completed outputs remain available')
            except Exception:
                with self.mutex:record.update(status='failed',message='Batch failed; completed outputs remain available')
            finally:
                with self.mutex:self.save(record)
        threading.Thread(target=worker,daemon=True,name='color-studio-batch').start()
        return self.get(identifier)

    def cancel(self,identifier):
        with self.mutex:
            if identifier not in self.records:raise KeyError(identifier)
            if self.records[identifier]['status'] in ('queued','running','cancelling'):
                self.cancel_events[identifier].set();self.records[identifier]['status']='cancelling';self.save(self.records[identifier])
            return self.get(identifier)
