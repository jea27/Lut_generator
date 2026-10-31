"""Manual spatial finishing v1. Not inference of a reference's optical effects."""
import math
import cv2
import numpy as np
from pydantic import BaseModel, ConfigDict, Field


class Look(BaseModel):
    model_config=ConfigDict(extra='forbid',allow_inf_nan=False)
    enabled: bool=False
    strength: float=Field(default=1,ge=0,le=1)
    glow: float=Field(default=0,ge=0,le=1)
    diffusion: float=Field(default=0,ge=0,le=1)
    fade: float=Field(default=0,ge=0,le=1)
    radius: float=Field(default=.008,ge=.001,le=.02)
    threshold: float=Field(default=.7,ge=.3,le=.95)


def apply(rgb,look,alpha=None,cancel=None,progress=None,tile_rows=128):
    """Linear-light highlight glow + diffusion, then bounded encoded fade.

    Radius is a fraction of the short image side. Finite Gaussian support and
    halos avoid tile seams and bound working memory. Transparent RGB cannot
    bleed into visible pixels. Alpha itself is never changed here.
    """
    from .engine import linear,encoded,ProcessingCancelled
    look=Look.model_validate(look)
    if not look.enabled or look.strength==0 or not (look.glow or look.diffusion or look.fade):return rgb
    sigma=max(.5,min(rgb.shape[:2])*look.radius);halo=math.ceil(3*sigma);kernel=2*halo+1
    output=np.empty_like(rgb);h=rgb.shape[0]
    for y in range(0,h,tile_rows):
        if cancel and cancel():raise ProcessingCancelled()
        end=min(h,y+tile_rows);start=max(0,y-halo);stop=min(h,end+halo)
        original=rgb[y:end];crop=slice(y-start,end-start)
        if look.glow or look.diffusion:
            lin=linear(rgb[start:stop]);mask=np.ones(lin.shape[:2],np.float32) if alpha is None else alpha[start:stop]
            def blur(a):return cv2.GaussianBlur(a,(kernel,kernel),sigma,borderType=cv2.BORDER_REFLECT_101)
            weight=blur(mask)[...,None]
            soft=blur(lin*mask[...,None])/np.maximum(weight,1e-6)
            candidate=lin[crop]*(1-look.diffusion*.65)+soft[crop]*look.diffusion*.65
            if look.glow:
                luminance=lin @ np.array([.2126,.7152,.0722],np.float32)
                highlights=np.clip((luminance-look.threshold)/(1-look.threshold),0,1)
                light=blur(lin*(highlights*mask)[...,None])/np.maximum(weight,1e-6)
                candidate=1-(1-candidate)*(1-look.glow*.45*light[crop])
            candidate=np.clip(encoded(candidate),0,1)
        else:candidate=original.copy()
        # Lift blacks and compress range gently; zero remains an exact bypass.
        candidate=candidate*(1-look.fade*.25)+look.fade*.08
        output[y:end]=np.clip(original+look.strength*(candidate-original),0,1)
        if progress:progress(end/h)
    return output
