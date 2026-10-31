import io
import unittest
import numpy as np
from PIL import Image
from pydantic import ValidationError
from packages.colour_core import engine,image_io
from packages.colour_core.look import Look,apply


class LookTests(unittest.TestCase):
    def setUp(self):
        self.rgb=np.random.default_rng(19).random((257,193,3),dtype=np.float32)

    def test_legacy_disabled_and_zero_bypass_are_exact(self):
        legacy=engine.Recipe(version=1)
        np.testing.assert_array_equal(engine.render(self.rgb,legacy),self.rgb)
        for look in [Look(enabled=False,glow=1),Look(enabled=True,strength=0,diffusion=1),Look(enabled=True)]:
            np.testing.assert_array_equal(engine.render(self.rgb,engine.Recipe(look=look)),self.rgb)
        with self.assertRaises(ValueError):engine.render(self.rgb,engine.Recipe(version=1,look=Look(enabled=True,glow=1)))

    def test_tiles_have_no_seams_and_are_finite_at_extremes(self):
        look=Look(enabled=True,glow=1,diffusion=1,fade=1,radius=.02)
        full=apply(self.rgb,look,tile_rows=1000)
        tiled=apply(self.rgb,look,tile_rows=31)
        np.testing.assert_allclose(full,tiled,atol=2e-6)
        self.assertTrue(np.isfinite(tiled).all());self.assertGreaterEqual(tiled.min(),0);self.assertLessEqual(tiled.max(),1)
        self.assertTrue(np.any(tiled!=self.rgb))

    def test_glow_spreads_highlights_and_diffusion_reduces_edges(self):
        bright=np.zeros((129,129,3),np.float32);bright[60:69,60:69]=1
        glow=apply(bright,Look(enabled=True,glow=1,radius=.02))
        self.assertGreater(float(glow[59,64].mean()),0)
        black=apply(bright*0,Look(enabled=True,glow=1))
        np.testing.assert_array_equal(black,bright*0)
        blurred=apply(bright,Look(enabled=True,diffusion=1,radius=.02))
        self.assertLess(float(blurred[60,64].mean()),1)
        self.assertGreater(float(blurred[59,64].mean()),0)

    def test_alpha_hidden_rgb_does_not_bleed_and_input_is_preserved(self):
        a=np.zeros((129,129,3),np.float32);a[:]=[0,.5,0]
        alpha=np.ones(a.shape[:2],np.float32);alpha[:,:50]=0
        b=a.copy();b[:,:50]=[1,0,1]
        look=Look(enabled=True,glow=1,diffusion=1,radius=.02)
        original=b.copy();left=apply(a,look,alpha);right=apply(b,look,alpha)
        np.testing.assert_allclose(left[:,50:],right[:,50:],atol=1e-6)
        np.testing.assert_array_equal(original,b)
        with Image.open(io.BytesIO(image_io.encode(right,alpha))) as im:
            np.testing.assert_array_equal(np.array(im.getchannel('A')),np.rint(alpha*255).astype('uint8'))

    def test_cube_is_color_only_and_json_roundtrip_keeps_effects(self):
        base=engine.Recipe(exposure=.2)
        effect=base.model_copy(update={'look':Look(enabled=True,glow=.5,diffusion=.4,fade=.3)})
        self.assertEqual(engine.cube(base),engine.cube(effect))
        self.assertIn('Spatial glow, diffusion and fade are excluded',engine.cube(effect))
        roundtrip=engine.validate_recipe(__import__('json').loads(effect.model_dump_json()))
        np.testing.assert_array_equal(engine.render(self.rgb,effect),engine.render(self.rgb,roundtrip))
        self.assertGreater(float(np.abs(engine.render(self.rgb,effect)-engine.render(self.rgb,base)).mean()),.001)

    def test_fade_monotonic_and_cancel_is_cooperative(self):
        ramp=np.repeat(np.linspace(0,1,100,dtype=np.float32)[None,:,None],3,axis=2)
        out=apply(ramp,Look(enabled=True,fade=1))
        self.assertGreater(float(out.min()),0);self.assertLess(float(out.max()),1)
        self.assertGreaterEqual(float(np.diff(out,axis=1).min()),0)
        with self.assertRaises(engine.ProcessingCancelled):apply(self.rgb,Look(enabled=True,glow=.5),cancel=lambda:True)
        for value in [float('nan'),-1,1.1]:
            with self.assertRaises(ValidationError):Look(glow=value)
