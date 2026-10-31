"""Decode SDR JPG/PNG, apply orientation/ICC, strip metadata in derived exports."""
import io
import warnings
import numpy as np
from PIL import Image, ImageCms, ImageOps

MAX_PIXELS=24_000_000
SRGB=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB'))


def decode(payload, max_side=None):
    if not isinstance(payload,bytes) or len(payload)>100*1024*1024:
        raise ValueError('Encoded image exceeds safe local size limit')
    if payload.startswith(b'\x89PNG\r\n\x1a\n') and len(payload)>24 and payload[24]!=8:
        raise ValueError('MVP supports 8-bit PNG only; prepare an SDR sRGB copy first')
    with warnings.catch_warnings():
        warnings.simplefilter('error', Image.DecompressionBombWarning)
        with Image.open(io.BytesIO(payload)) as original:
            if original.format not in ('JPEG','PNG') or getattr(original,'n_frames',1)!=1:
                raise ValueError('Only still JPEG/PNG are supported')
            if original.width*original.height>MAX_PIXELS or max(original.size)>12000:
                raise ValueError('Maximum 24 megapixels and 12000 pixels per side')
            if original.mode not in ('RGB','RGBA','L','LA','P'):
                raise ValueError('Only 8-bit SDR RGB/grayscale PNG/JPEG; CMYK/16-bit/RAW unsupported')
            # Check PNG chunk CRCs/truncation before processing pixels. JPEG
            # decoding below remains strict (LOAD_TRUNCATED_IMAGES is not enabled).
            try: original.verify()
            except (OSError,SyntaxError) as error: raise ValueError('Invalid or truncated image data') from error
        with Image.open(io.BytesIO(payload)) as original:
            image=ImageOps.exif_transpose(original)
            if max_side: image.thumbnail((max_side,max_side),Image.Resampling.LANCZOS)
            rgba=image.convert('RGBA')
            alpha=np.asarray(rgba.getchannel('A'),dtype=np.float32)/255.
            rgb=rgba.convert('RGB')
            profile=original.info.get('icc_profile')
            notes=[]
            if profile:
                try:
                    rgb=ImageCms.profileToProfile(rgb,ImageCms.ImageCmsProfile(io.BytesIO(profile)),SRGB,
                                                  renderingIntent=1,outputMode='RGB')
                except Exception as error: raise ValueError('Invalid or unsupported ICC profile') from error
                notes.append('Embedded ICC converted to sRGB, relative colorimetric')
            else: notes.append('No ICC: explicitly assumed sRGB; RAW/Log/HDR are not supported')
            pixels=np.asarray(rgb,dtype=np.float32)/255.
            if not np.any(alpha>.05): raise ValueError('Image is fully transparent')
            return pixels, alpha if np.any(alpha<1) else None, notes


def encode(rgb, alpha=None, format='PNG'):
    if format not in ('PNG','JPEG'): raise ValueError('Unsupported export format')
    pixels=np.clip(np.rint(rgb*255),0,255).astype(np.uint8)
    if alpha is not None and format=='JPEG':
        pixels=np.rint(pixels*alpha[...,None]+255*(1-alpha[...,None])).astype(np.uint8)
    image=Image.fromarray(pixels)
    if alpha is not None and format=='PNG': image.putalpha(Image.fromarray(np.rint(alpha*255).astype(np.uint8)))
    stream=io.BytesIO()
    image.save(stream,format=format,icc_profile=SRGB.tobytes(),**({'quality':95,'subsampling':0} if format=='JPEG' else {}))
    return stream.getvalue()
