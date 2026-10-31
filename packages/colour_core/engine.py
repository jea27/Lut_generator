"""Conservative global colour matching in CIELAB D65, encoded-sRGB I/O."""
import cv2
import numpy as np
from functools import lru_cache
from pydantic import BaseModel, ConfigDict, Field

M = np.array([[.4124564,.3575761,.1804375],[.2126729,.7151522,.0721750],
              [.0193339,.1191920,.9503041]], dtype=np.float32)
WHITE = np.array([.95047,1.,1.08883], dtype=np.float32)


class Recipe(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)
    version: int = Field(default=1, ge=1, le=1)
    domain: str = Field(default='encoded-sRGB-D65', pattern='^encoded-sRGB-D65$')
    method: str = Field(default='lab-statistics', pattern='^(lab-statistics|mean-only)$')
    scale: list[float] = Field(default_factory=lambda:[1.,1.,1.], min_length=3, max_length=3)
    offset: list[float] = Field(default_factory=lambda:[0.,0.,0.], min_length=3, max_length=3)
    intensity: float = Field(default=1., ge=0., le=1.)
    exposure: float = Field(default=0., ge=-2., le=2.)
    contrast: float = Field(default=1., ge=.6, le=1.4)
    saturation: float = Field(default=1., ge=0., le=2.)
    temperature: float = Field(default=0., ge=-1., le=1.)


def validate_recipe(recipe):
    r = Recipe.model_validate(recipe)
    if any(not .8 <= x <= 1.2 for x in r.scale) or any(abs(x)>12 for x in r.offset):
        raise ValueError('Recipe statistics outside conservative bounds')
    return r


def linear(rgb):
    return np.where(rgb <= .04045, rgb/12.92, ((rgb+.055)/1.055)**2.4)


def encoded(rgb):
    rgb = np.maximum(rgb,0)
    return np.where(rgb<=.0031308,12.92*rgb,1.055*rgb**(1/2.4)-.055)


def to_lab(rgb):
    xyz = linear(rgb) @ M.T / WHITE
    d=6/29
    f=np.where(xyz>d**3,np.cbrt(xyz),xyz/(3*d*d)+4/29)
    return np.stack([116*f[...,1]-16,500*(f[...,0]-f[...,1]),200*(f[...,1]-f[...,2])],axis=-1)


def from_lab(lab):
    fy=(lab[...,0]+16)/116
    f=np.stack([fy+lab[...,1]/500,fy,fy-lab[...,2]/200],axis=-1)
    d=6/29
    xyz=np.where(f>d,f**3,3*d*d*(f-4/29))*WHITE
    return xyz @ np.linalg.inv(M).T  # linear RGB, deliberately not clipped


def sample(rgb, alpha=None, size=512):
    h,w=rgb.shape[:2]; factor=min(1.,size/max(h,w))
    small=cv2.resize(rgb,(max(1,round(w*factor)),max(1,round(h*factor))),interpolation=cv2.INTER_AREA)
    if alpha is not None:
        mask=cv2.resize(alpha,(small.shape[1],small.shape[0]),interpolation=cv2.INTER_NEAREST)>.05
        pixels=small[mask]
        if len(pixels)==0: raise ValueError('Image is fully transparent')
        return pixels.reshape(-1,1,3)
    return small


def analyze(rgb, alpha=None):
    pixels=sample(rgb,alpha).reshape(-1,3)
    lab=to_lab(pixels)
    lum=linear(pixels) @ M[1]
    bins=np.minimum((pixels*16).astype(int),15)
    keys=bins[:,0]*256+bins[:,1]*16+bins[:,2]
    counts=np.bincount(keys,minlength=4096)
    dominant=[]
    for key in np.argsort(counts)[-6:][::-1]:
        if counts[key]==0: continue
        color=np.mean(pixels[keys==key],axis=0)
        dominant.append({'hex':'#'+''.join(f'{round(float(x)*255):02x}' for x in color),
                         'fraction':float(counts[key]/len(pixels))})
    return {'lab_mean':lab.mean(axis=0).tolist(),'lab_std':lab.std(axis=0).tolist(),
            'luminance_mean':float(lum.mean()), 'luminance_p05':float(np.percentile(lum,5)),
            'luminance_p95':float(np.percentile(lum,95)),
            'contrast_p95_p05':float(np.percentile(lum,95)-np.percentile(lum,5)),
            'histograms':[np.histogram(pixels[:,c],bins=64,range=(0,1))[0].tolist() for c in range(3)],
            'dominant':dominant,'sample_pixels':len(pixels)}


def fit(source, reference, method='lab-statistics', source_alpha=None, reference_alpha=None):
    a=analyze(source,source_alpha); b=analyze(reference,reference_alpha)
    if method not in ('lab-statistics','mean-only'): raise ValueError('Unknown matching method')
    scale=np.ones(3) if method=='mean-only' else np.clip(np.divide(np.array(b['lab_std']),a['lab_std'],
                            out=np.ones(3),where=np.array(a['lab_std'])>1.),.8,1.2)
    offset=np.clip(np.array(b['lab_mean'])-np.array(a['lab_mean'])*scale,-12,12)
    return Recipe(method=method,scale=scale.tolist(),offset=offset.tolist())


def gamut_map(rgb):
    # Compress towards equal-channel luminance. Preserves hue direction in linear RGB.
    neutral=np.clip(rgb @ M[1],0,1)[...,None]
    delta=rgb-neutral
    ratios=np.where(delta>1e-8,(1-neutral)/np.maximum(delta,1e-8),
                    np.where(delta < -1e-8,-neutral/np.minimum(delta,-1e-8),1.))
    factor=np.minimum(1,np.min(ratios,axis=-1,keepdims=True))
    return np.clip(neutral+delta*np.maximum(factor,0),0,1)


def evaluate_global(rgb, recipe):
    r=validate_recipe(recipe)
    a=np.asarray(rgb,dtype=np.float32)
    if a.shape[-1]!=3 or not np.isfinite(a).all() or a.min()<0 or a.max()>1:
        raise ValueError('Expected finite encoded sRGB in [0,1]')
    neutral=(r.scale==[1.,1.,1.] and r.offset==[0.,0.,0.] and r.exposure==0 and
             r.contrast==1 and r.saturation==1 and r.temperature==0)
    if r.intensity==0 or neutral: return a.copy()
    lab=to_lab(a)
    candidate=lab*np.array(r.scale,dtype=np.float32)+np.array(r.offset,dtype=np.float32)
    # Lightness offset tapers at black/white, preserving endpoint detail.
    u=lab[...,0]/100
    candidate[...,0]=lab[...,0]+np.clip(candidate[...,0]-lab[...,0],-15,15)*4*u*(1-u)
    candidate[...,1:]*=r.saturation
    matched=encoded(gamut_map(from_lab(candidate)))
    matched=np.clip(a+np.clip(matched-a,-.25,.25),0,1)
    lin=linear(matched)
    gains=2**r.exposure*np.exp(np.array([r.temperature*.12,0,-r.temperature*.12],dtype=np.float32))
    lin=gains*lin/(1+(gains-1)*lin)  # endpoint-preserving, exposure-like tone curve
    styled=np.clip(encoded(lin),0,1)
    if r.contrast!=1:
        x=np.clip(styled,1e-7,1-1e-7)
        styled=1/(1+np.exp(-r.contrast*np.log(x/(1-x))))
        styled=np.where(matched==0,0,np.where(matched==1,1,styled))
    return np.clip(a+r.intensity*(styled-a),0,1).astype(np.float32)


@lru_cache(maxsize=16)
def lut_grid(recipe_json):
    recipe=Recipe.model_validate_json(recipe_json)
    grid=np.array([[red,green,blue] for blue in np.linspace(0,1,33)
                   for green in np.linspace(0,1,33) for red in np.linspace(0,1,33)],dtype=np.float32)
    return evaluate_global(grid,recipe).reshape(33,33,33,3)


def transform(rgb, recipe):
    r=validate_recipe(recipe)
    a=np.asarray(rgb,dtype=np.float32)
    if a.shape[-1]!=3 or not np.isfinite(a).all() or a.min()<0 or a.max()>1:
        raise ValueError('Expected finite encoded sRGB in [0,1]')
    neutral=(r.scale==[1.,1.,1.] and r.offset==[0.,0.,0.] and r.exposure==0 and
             r.contrast==1 and r.saturation==1 and r.temperature==0)
    if r.intensity==0 or neutral:return a.copy()
    # The rendered look IS the 33^3 LUT, not a second analytic approximation.
    table=lut_grid(r.model_dump_json());flat=a.reshape(-1,3);position=flat*32
    lower=np.floor(position).astype(np.int32);fraction=position-lower
    output=np.zeros_like(flat)
    for blue in (0,1):
        for green in (0,1):
            for red in (0,1):
                bits=np.array([red,green,blue]);indices=np.minimum(lower+bits,32)
                weight=np.prod(np.where(bits,fraction,1-fraction),axis=1)
                output+=table[indices[:,2],indices[:,1],indices[:,0]]*weight[:,None]
    return np.clip(output.reshape(a.shape),0,1)


class ProcessingCancelled(Exception):pass


def render(rgb, recipe, cancel=None, progress=None):
    # Bound working arrays independently of full-resolution file size.
    output=np.empty_like(rgb,dtype=np.float32)
    for y in range(0,rgb.shape[0],64):
        if cancel and cancel():raise ProcessingCancelled()
        output[y:y+64]=transform(rgb[y:y+64],recipe)
        if progress:progress(min(1,(y+64)/rgb.shape[0]))
    return output


def cube(recipe, size=33):
    r=validate_recipe(recipe)
    if size!=33: raise ValueError('MVP exports 33^3 only')
    values=lut_grid(r.model_dump_json()).reshape(-1,3)
    header=['# LumaForge v0.1: fixed global encoded sRGB -> encoded sRGB D65',
            '# Not an input LUT, not Rec.709/Log/HDR. No masks or adaptive per-image steps.',
            'TITLE "LumaForge global look"','LUT_3D_SIZE 33','DOMAIN_MIN 0.0 0.0 0.0','DOMAIN_MAX 1.0 1.0 1.0']
    return '\n'.join(header+['%.7f %.7f %.7f'%tuple(row) for row in values])+'\n'
