"""Versioned capability catalogue, not a payment or security bypass mechanism."""
from copy import deepcopy

CATALOG = {
    'schema_version': 1,
    'modes': ['creator', 'pro'],
    'engine': 'colour_core',
    'license_policy': {'mode': 'technical-evaluation', 'enforcement': False, 'payments': False,
                       'safety_always_on': True},
    'capabilities': [
        {'id': 'color-match', 'modes': ['creator','pro'], 'status': 'available'},
        {'id': 'manual-look', 'modes': ['creator','pro'], 'status': 'available'},
        {'id': 'presets', 'modes': ['creator','pro'], 'status': 'available'},
        {'id': 'image-export', 'modes': ['creator','pro'], 'status': 'available'},
        {'id': 'lut-export', 'modes': ['pro'], 'status': 'available'},
        {'id': 'batches', 'modes': ['pro'], 'status': 'available'},
        {'id': 'shot-planner', 'modes': ['pro'], 'status': 'experimental'},
        {'id': 'automatic-look', 'modes': ['creator','pro'], 'status': 'planned'},
        {'id': 'raw-log-hdr', 'modes': ['pro'], 'status': 'planned'},
        {'id': 'video-shot-match', 'modes': ['pro'], 'status': 'planned'},
        {'id': 'pro-curves', 'modes': ['pro'], 'status': 'planned'},
        {'id': 'color-profiles', 'modes': ['pro'], 'status': 'planned'},
    ],
    'providers': [{'id': 'local-rules-v1', 'requires_network': False, 'transmits_images': False}],
}


def catalogue():
    result=deepcopy(CATALOG)
    titles={
        'automatic-look':('Detección automática del acabado','Automatic finish detection'),
        'raw-log-hdr':('Ingesta RAW, Log y HDR','RAW, Log and HDR ingestion'),
        'video-shot-match':('Matching entre planos de vídeo','Video shot matching'),
        'pro-curves':('Edición avanzada de curvas','Advanced curve editing'),
        'color-profiles':('Perfiles y espacios de color adicionales','Additional colour profiles and spaces'),
    }
    for capability in result['capabilities']:
        es,en=titles.get(capability['id'],(capability['id'],capability['id']))
        capability['title']={'es':es,'en':en}
    return result
