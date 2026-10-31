"""Deterministic, bounded observations and user-directed shooting proposals.

No semantics/EXIF inference, external API, model weights or copyrighted frames.
Sources are attributed links, not copies of manuals or third-party diagrams.
"""
from typing import Literal, Protocol
import numpy as np
from pydantic import BaseModel, ConfigDict, Field
from packages.colour_core import engine

SOURCES = [
    {'id':'arri-shutter', 'title':'ARRI ALEXA 35 SUP 5.2 — shutter equation, pp.26/43',
     'url':'https://www.arri.com/resource/blob/401824/823cd1114755dc134ff9ee3c98be6e15/alexa-35-sup-5-2-0-user-manual-en-data.pdf',
     'verified_on':'2026-10-31'},
    {'id':'arri-lighting', 'title':'ARRI Lighting Handbook — light size, key/fill/separation',
     'url':'https://www.arri.com/en/learn/lighting/lighting-handbook', 'verified_on':'2026-10-31'},
    {'id':'asc-fill', 'title':'ASC — Lighting a Set with Stephen H. Burum: measured fill and mood',
     'url':'https://theasc.com/article/lighting-a-set/', 'verified_on':'2026-10-31'},
]


class Setup(BaseModel):
    model_config=ConfigDict(extra='forbid',allow_inf_nan=False)
    shot: Literal['wide','medium','close']='medium'
    key_side: Literal['left','right','back','front']='left'
    softness: Literal['soft','hard']='soft'
    contrast: Literal['low','medium','high']='medium'
    sensor_width_mm: float=Field(default=36,ge=6,le=70)
    focal_mm: float | None=Field(default=None,ge=4,le=300)
    aperture: float=Field(default=4,ge=1,le=22)
    fps: float=Field(default=25,ge=1,le=120)
    shutter_angle: float=Field(default=180,ge=1,le=360)
    white_balance_k: int=Field(default=5600,ge=2000,le=12000)
    camera_height_m: float=Field(default=1.5,ge=.1,le=3)
    movement: Literal['locked','handheld','slow-move']='locked'


def item(kind, title, detail, sources=(), uncertainty=None):
    return {'kind':kind,'title':title,'detail':detail,'source_ids':list(sources),
            'uncertainty':uncertainty}


def observations(rgb, alpha=None):
    a=np.asarray(rgb,dtype=np.float32)
    if a.ndim!=3 or a.shape[2]!=3 or min(a.shape[:2])<2 or max(a.shape[:2])>512:
        raise ValueError('Planner requires a 2–512 pixel bounded SDR sample')
    if not np.isfinite(a).all() or a.min()<0 or a.max()>1:
        raise ValueError('Invalid planner SDR sample')
    mask=np.ones(a.shape[:2],dtype=bool)
    if alpha is not None:
        alpha=np.asarray(alpha)
        if alpha.shape!=a.shape[:2] or not np.isfinite(alpha).all() or alpha.min()<0 or alpha.max()>1:
            raise ValueError('Invalid planner alpha')
        mask=alpha>.05
    if not mask.any():raise ValueError('No visible reference pixels')
    lum=engine.linear(a) @ engine.M[1]
    visible=lum[mask]
    p05,p50,p95=np.percentile(visible,[5,50,95]).tolist()
    # Bright centroid is an image-space measurement, never a light direction.
    bright=(lum>=p95)&mask
    ys,xs=np.nonzero(bright)
    centroid=[float(xs.mean()/max(1,a.shape[1]-1)),float(ys.mean()/max(1,a.shape[0]-1))]
    return {'analysis_dimensions':[a.shape[1],a.shape[0]],'aspect_ratio':a.shape[1]/a.shape[0],
            'linear_srgb_luminance':{'p05':p05,'p50':p50,'p95':p95},
            'encoded_clipped_fraction':float(np.mean(np.any(a[mask]>=254/255,axis=1))),
            'bright_region_centroid_xy':centroid,
            'palette':engine.analyze(a,alpha)['dominant'],
            'limits':'SDR display-referred pixels, not scene radiance, lighting ratio or illuminant CCT.'}


class PlannerProvider(Protocol):
    id: str
    requires_network: bool
    def analyze(self, rgb, alpha=None) -> dict: ...


class LocalRules:
    id='local-rules-v1'
    requires_network=False
    def analyze(self, rgb, alpha=None):return observations(rgb,alpha)


def generate(rgb, setup:Setup, alpha=None, recipe=None, provider_id='local-rules-v1'):
    # Explicit allowlist: there is no remote transport, opt-in switch or fallback.
    if provider_id!='local-rules-v1':raise ValueError('Provider unavailable; external image transmission is disabled')
    s=Setup.model_validate(setup)
    obs=LocalRules().analyze(rgb,alpha)
    shot={'wide':'Plano general: incluir entorno y comprobar líneas/perspectiva.',
          'medium':'Plano medio: ajustar encuadre a la acción y separación del fondo.',
          'close':'Primer plano: revisar ojos, foco y distorsión por proximidad.'}[s.shot]
    side={'left':(-2,-1),'right':(2,-1),'back':(1,2),'front':(0,-2)}[s.key_side]
    side_label={'left':'izquierda','right':'derecha','back':'contraluz','front':'frontal'}[s.key_side]
    fill_stops={'low':1,'medium':2,'high':3}[s.contrast]
    shutter=s.shutter_angle/(360*s.fps)
    suggestions={
        'composition':[
            item('observation','Formato medido',f"Relación ancho/alto {obs['aspect_ratio']:.3f} en muestra normalizada; no identifica el formato de sensor."),
            item('recommendation','Escala elegida por ti',shot,uncertainty='No hay detector de sujetos/escala de plano en esta versión.'),
            item('recommendation','Ángulo y altura',f'Partir de cámara a {s.camera_height_m:g} m; ajustar al sujeto y comparar verticales/horizonte.',uncertainty='La altura y el ángulo originales son desconocidos.'),
            item('estimate','Perspectiva y profundidad','Comparar tamaños relativos y líneas de fuga; cambiar distancia de cámara antes de cerrar el encuadre.',uncertainty='No se calcula profundidad 3D ni ubicación original del sujeto.'),
        ],
        'lighting':[
            item('observation','Altas luces en la imagen',f"Centro de región luminosa normalizado x={obs['bright_region_centroid_xy'][0]:.2f}, y={obs['bright_region_centroid_xy'][1]:.2f}.",uncertainty='Esto no identifica la posición de una fuente, key, práctica o ventana.'),
            item('recommendation','Key/fill/rim propuestos',f'Key desde {side_label}; fill próximo al eje de cámara y rim opcional para separación. Posiciones editables en diagrama.',('arri-lighting','asc-fill'),uncertainty='Es un montaje propuesto, no el esquema de la referencia.'),
            item('recommendation','Calidad de luz','Probar fuente grande/difusión próxima al sujeto.' if s.softness=='soft' else 'Probar fuente pequeña y banderas para controlar sombra y derrame.',('arri-lighting',),uncertainty='La dureza elegida por el usuario no se detecta automáticamente.'),
            item('recommendation','Contraste orientativo',f'Punto de partida: fill {fill_stops} pasos por debajo de key en mediciones incidentes separadas ({2**fill_stops}:1 key:fill). Medir y ajustar; no es (key+fill):fill.',('asc-fill',),uncertainty='No se estima una relación de iluminación desde percentiles de la fotografía.'),
            item('recommendation','Temperatura y prácticas',f'Probar WB {s.white_balance_k} K elegido por ti, carta gris y fuentes/prácticas medidas. Ajustar mezcla o geles.',uncertainty='CCT original desconocida; el color procesado no permite recuperarla.'),
        ],
        'camera':[
            item('source_confirmed','Obturación calculada',f'{s.fps:g} fps y {s.shutter_angle:g}° → {shutter:.6f} s (1/{1/shutter:.2f} s).',('arri-shutter',),uncertainty='Fórmula confirmada; fps/ángulo son elecciones del usuario, no metadatos de la referencia. Probar flicker con las luces reales.'),
            item('recommendation','Apertura, foco y exposición',f'Partir de f/{s.aperture:g} elegido por ti. Ajustar separación sujeto/fondo, enfocar y medir exposición con carta gris, waveform y altas luces.',uncertainty='Apertura y profundidad de campo originales desconocidas; ISO base depende de tu cámara.'),
            item('recommendation','Captura y movimiento',{'locked':'Trípode, plano fijo y prueba de estabilidad.','handheld':'Cámara al hombro/mano con ensayo y soporte adecuado.','slow-move':'Ensayar movimiento lento con soporte disponible.'}[s.movement]+' Usar perfil validado de cámara; preparar copia SDR sRGB para Color Studio.',uncertainty='Color Studio todavía no ingiere Log/HDR ni vídeo. No se identifica cámara, códec ni rango dinámico original.'),
        ],
        'postproduction':[
            item('recommendation','Continuidad de color','Normalizar entradas a SDR sRGB con herramienta/perfil de cámara verificados; comparar por planos y carta. Aplicar Color Match con intensidad moderada.'),
            item('recommendation','Acabado y exportación','Glow, difusión y fade se ajustan manualmente y se guardan en la receta. .cube contiene solo color; render PNG/JPG conserva el acabado. No se infiere el look completo ni halation.'),
        ],
    }
    equivalent=None
    if s.focal_mm is not None:
        equivalent=36*s.focal_mm/s.sensor_width_mm
        suggestions['camera'].insert(0,item('recommendation','Focal y sensor elegidos',
            f'{s.focal_mm:g} mm / sensor ancho {s.sensor_width_mm:g} mm → equivalente horizontal 36 mm: {equivalent:.1f} mm.',
            uncertainty='Cálculo geométrico de tu propuesta, no una estimación de la óptica original; se desconoce el recorte.'))
    else:
        suggestions['camera'].insert(0,item('estimate','Focal original: sin datos',
            'Elegir una focal disponible, fijar distancia y contrastar perspectiva/encuadre.',uncertainty='Sin evidencia suficiente: no se asigna una focal numérica desde la foto.'))
    diagram=[{'id':'subject','label':'Sujeto','x':0,'y':0,'enabled':True},
             {'id':'camera','label':'Cámara','x':0,'y':-3,'enabled':True},
             {'id':'key','label':'Key','x':side[0],'y':side[1],'enabled':True},
             {'id':'fill','label':'Fill','x':-side[0]*.75,'y':-2,'enabled':True},
             {'id':'rim','label':'Rim','x':1,'y':2,'enabled':False},
             {'id':'practical','label':'Práctica','x':-3,'y':2,'enabled':False}]
    return {'schema':'lumaforge-shot-plan-v1','provider':LocalRules.id,'experimental':True,
            'original_setup_recovered':False,'human_validated':False,'setup':s.model_dump(),
            'observations':obs,'sections':suggestions,'diagram':{'units':'metres-proposed','nodes':diagram},
            'calculations':{'exposure_seconds':shutter,'horizontal_focal_equivalent_mm':equivalent},
            'equipment':{
                'low_budget':['Cámara y óptica disponibles; soporte estable','Ventana controlada o fuente existente, reflector y tela negra','Carta gris, cinta y prueba de foco/exposición'],
                'professional':['Fuentes regulables con difusión y control de derrame','Banderas/negative fill y rim opcional','Fotómetro, monitor con waveform y carta de color']},
            'checklist':[{'id':key,'text':label,'checked':False} for key,label in [
                ('rights','Confirmar derechos de referencia, autoría y consentimiento cuando proceda.'),
                ('safety','Asegurar soportes/cables y seguir seguridad del fabricante; no improvisar rigging eléctrico.'),
                ('frame','Igualar encuadre, perspectiva, foco y separación del fondo en monitor.'),
                ('exposure','Grabar carta gris/color, medir exposición y comprobar altas luces/ruido.'),
                ('wb','Ajustar WB con carta y comprobar mezclas de luz.'),
                ('flicker','Grabar prueba con fps/obturación elegidos y comprobar flicker/movimiento.'),
                ('continuity','Comparar planos y exportación con la misma gestión de color.')]],
            'sources':[dict(source) for source in SOURCES],
            'recipe':engine.validate_recipe(recipe).model_dump() if recipe is not None else None,
            'limits':['Propuesta inicial local, no reproducción fiel ni datos confirmados del rodaje original.',
                      'No detector de personas, luces, óptica, profundidad o atmósfera; hipótesis dirigidas por el usuario.',
                      'Fuentes enlazadas; no se redistribuyen fotografías, diagramas o manuales de terceros.']}
