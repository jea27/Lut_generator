"""Synthetic infrastructure/physics tests; not evidence of faithful cinematography."""
import io
import json
import socket
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from PIL import Image
from fastapi.testclient import TestClient
from pydantic import ValidationError
from apps.api.main import create_app
from apps.api.capabilities import catalogue
from packages.colour_core import engine
from packages.shot_planner.planner import Setup,generate,observations


class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.rgb=np.random.default_rng(17).random((48,64,3),dtype=np.float32)

    def test_deterministic_local_report_has_no_unfounded_original_camera_or_lighting(self):
        before=self.rgb.copy()
        with patch.object(socket,'socket',side_effect=AssertionError('Network forbidden')):
            a=generate(self.rgb,Setup());b=generate(self.rgb,Setup())
        self.assertEqual(a,b)
        np.testing.assert_array_equal(self.rgb,before)
        self.assertFalse(a['human_validated']);self.assertFalse(a['original_setup_recovered'])
        self.assertIsNone(a['calculations']['horizontal_focal_equivalent_mm'])
        self.assertIn('sin datos',a['sections']['camera'][0]['title'])
        self.assertTrue(all(not check['checked'] for check in a['checklist']))
        self.assertEqual(a['provider'],'local-rules-v1')

    def test_shutter_math_and_horizontal_equivalence_use_explicit_user_inputs(self):
        for fps in (24,25,29.97,60):
            a=generate(self.rgb,Setup(fps=fps,shutter_angle=180,focal_mm=25,sensor_width_mm=24))
            self.assertAlmostEqual(a['calculations']['exposure_seconds'],1/(2*fps))
            self.assertAlmostEqual(a['calculations']['horizontal_focal_equivalent_mm'],37.5)
        a=generate(self.rgb,Setup(fps=50,shutter_angle=90))
        self.assertEqual(a['calculations']['exposure_seconds'],1/200)

    def test_claim_types_uncertainty_and_attribution_are_explicit(self):
        a=generate(self.rgb,Setup())
        sources={s['id'] for s in a['sources']}
        kinds=set()
        for rows in a['sections'].values():
            for row in rows:
                kinds.add(row['kind']);self.assertTrue(set(row['source_ids'])<=sources)
                if row['kind']=='source_confirmed':self.assertTrue(row['source_ids'])
                if row['kind']=='estimate':self.assertTrue(row['uncertainty'])
        self.assertEqual(kinds,{'observation','estimate','recommendation','source_confirmed'})
        self.assertTrue(all(s['url'].startswith(('https://www.arri.com/','https://theasc.com/')) for s in a['sources']))

    def test_alpha_hidden_pixels_do_not_influence_observations(self):
        alpha=np.ones((48,64),dtype=np.float32);alpha[:24]=0
        changed=self.rgb.copy();changed[:24]=1
        a=observations(self.rgb,alpha);b=observations(changed,alpha)
        self.assertEqual(a,b)
        with self.assertRaises(ValueError):observations(self.rgb,np.zeros_like(alpha))
        with self.assertRaises(ValueError):observations(self.rgb,np.full_like(alpha,np.nan))

    def test_input_ranges_nonfinite_and_remote_provider_are_rejected(self):
        for value in ({'fps':0},{'sensor_width_mm':0},{'focal_mm':float('nan')},{'shutter_angle':361},{'unknown':'x'}):
            with self.assertRaises(ValidationError):Setup(**value)
        with self.assertRaises(ValueError):generate(self.rgb,Setup(),provider_id='remote')
        with self.assertRaises(ValueError):observations(np.zeros((1024,32,3)))
        with self.assertRaises(ValueError):observations(self.rgb*2)

    def test_optical_effect_recipe_is_preserved_separately_from_color_lut(self):
        recipe=engine.Recipe(look={'enabled':True,'glow':.2,'diffusion':.1,'fade':.1})
        a=generate(self.rgb,Setup(),recipe=recipe)
        self.assertEqual(a['recipe'],recipe.model_dump())
        self.assertNotEqual(a['schema'],'lumaforge-look-recipe')
        neutral=recipe.model_copy(update={'look':recipe.look.model_copy(update={'enabled':False})})
        self.assertEqual(engine.cube(recipe),engine.cube(neutral))

    def test_capability_catalogue_does_not_treat_paid_modes_as_security_policy(self):
        a=catalogue();a['license_policy']['safety_always_on']=False
        self.assertTrue(catalogue()['license_policy']['safety_always_on'])
        self.assertFalse(catalogue()['license_policy']['payments'])
        self.assertFalse(catalogue()['license_policy']['enforcement'])
        self.assertTrue(all(not p['requires_network'] and not p['transmits_images'] for p in catalogue()['providers']))
        self.assertEqual(next(x['status'] for x in a['capabilities'] if x['id']=='video-shot-match'),'planned')
        self.assertTrue(all(c['title']['es']!=c['id'] for c in a['capabilities'] if c['status']=='planned'))

    def test_api_plan_preferences_migration_and_shared_engine_workflow(self):
        with tempfile.TemporaryDirectory() as directory:
            from pathlib import Path
            root=Path(directory)
            (root/'preferences.json').write_text(json.dumps({'language':'es','welcome_seen':True,'export_format':'png'}))
            with TestClient(create_app(root),base_url='http://127.0.0.1') as client:
                token=client.get('/api/session').json()['csrf']
                client.headers.update({'X-LumaForge-Local':'1','X-Color-Studio-Token':token})
                self.assertEqual(client.get('/api/preferences').json()['workspace'],'creator')
                buffer=io.BytesIO();Image.fromarray((self.rgb*255).astype('uint8')).save(buffer,format='PNG')
                response=client.post('/api/images',files={'file':('private-reference.png',buffer.getvalue())})
                identifier=response.json()['id']
                body={'reference_id':identifier,'setup':{'fps':25,'shutter_angle':180},'recipe':engine.Recipe().model_dump()}
                plan=client.post('/api/planner',json=body)
                self.assertEqual(plan.status_code,200,plan.text)
                self.assertNotIn('private-reference',plan.text);self.assertNotIn(identifier,plan.text)
                self.assertNotIn(str(root),plan.text);self.assertNotIn('exif',plan.text.lower())
                self.assertGreaterEqual(plan.json()['metrics']['wall_ms'],0)
                before={p.name:p.read_bytes() for p in (root/'images').glob('*.png')}
                exports=[]
                for mode in ('creator','pro','creator'):
                    preferences=client.get('/api/preferences').json();preferences['workspace']=mode
                    self.assertEqual(client.put('/api/preferences',json=preferences).status_code,200)
                    result=client.post('/api/export/png',json={'source_id':identifier,'recipe':body['recipe']})
                    self.assertEqual(result.status_code,200);exports.append(result.content)
                self.assertEqual(exports[0],exports[1]);self.assertEqual(exports[1],exports[2])
                self.assertEqual(before,{p.name:p.read_bytes() for p in (root/'images').glob('*.png')})
                self.assertEqual(client.post('/api/planner',json={**body,'provider':'remote'}).status_code,422)
                self.assertEqual(client.post('/api/planner',json={**body,'reference_id':'../private'}).status_code,404)
                self.assertEqual(client.get('/api/capabilities').json()['schema_version'],1)
