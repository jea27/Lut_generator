import io
import unittest
import numpy as np
from PIL import Image
from pydantic import ValidationError
from packages.colour_core.engine import Recipe, analyze, fit, transform, render, cube, to_lab, from_lab, encoded
from packages.colour_core.image_io import decode, encode


class EngineTests(unittest.TestCase):
    def setUp(self): self.a=np.random.default_rng(7).random((31,47,3),dtype=np.float32)

    def test_neutral_and_zero_strength_exact_identity(self):
        np.testing.assert_array_equal(transform(self.a,Recipe()),self.a)
        np.testing.assert_array_equal(transform(self.a,Recipe(intensity=0,offset=[10,12,-12],exposure=2)),self.a)
        np.testing.assert_allclose(transform(self.a,fit(self.a,self.a)),self.a,atol=2e-6)

    def test_color_roundtrip_and_known_primary(self):
        np.testing.assert_allclose(to_lab(np.array([[1,0,0]],dtype=np.float32))[0],[53.2408,80.0925,67.2032],atol=.002)
        np.testing.assert_allclose(encoded(from_lab(to_lab(self.a))),self.a,atol=5e-6)

    def test_extreme_controls_finite_and_bounded_and_tiled_equal(self):
        r=Recipe(scale=[1.2,.8,1.2],offset=[12,-12,12],exposure=2,saturation=2,temperature=-1,contrast=1.4)
        b=transform(self.a,r)
        self.assertTrue(np.isfinite(b).all());self.assertGreaterEqual(b.min(),0);self.assertLessEqual(b.max(),1)
        np.testing.assert_array_equal(b,render(self.a,r))
        for invalid in ({'scale':[float('nan'),1,1]},{'intensity':1.1},{'offset':[1,2]}, {'unexpected':1}):
            with self.assertRaises(ValidationError): Recipe(**invalid)
        with self.assertRaises(ValueError): transform(self.a,Recipe(scale=[2,1,1]))

    def test_two_baselines_and_flat_input_stable(self):
        ref=np.clip(self.a*.4+np.array([.3,.1,.2]),0,1).astype('float32')
        a=fit(self.a,ref);b=fit(self.a,ref,'mean-only')
        self.assertNotEqual(a.scale,b.scale)
        flat=np.full((8,8,3),.5,dtype='float32')
        np.testing.assert_array_equal(transform(flat,fit(flat,flat)),flat)
        self.assertTrue(np.isfinite(transform(flat,fit(flat,ref))).all())

    def test_analysis_histogram_counts_and_alpha_ignored(self):
        a=analyze(self.a)
        self.assertEqual(sum(a['histograms'][0]),a['sample_pixels'])
        self.assertGreater(a['contrast_p95_p05'],0)
        self.assertTrue(a['dominant'][0]['hex'].startswith('#'))
        mask=np.zeros(self.a.shape[:2]);mask[0,0]=1
        self.assertEqual(analyze(self.a,mask)['sample_pixels'],1)
        with self.assertRaises(ValueError): analyze(self.a,mask*0)

    def test_lut_identity_order_and_roundtrip_interpolation(self):
        text=cube(Recipe()); lines=[x for x in text.splitlines() if x and (x[0].isdigit() or x[0]=='-')]
        table=np.array([[float(x) for x in line.split()] for line in lines]).reshape(33,33,33,3)
        self.assertEqual(len(lines),33**3)
        np.testing.assert_allclose(table[0,0,1],[1/32,0,0],atol=1e-7)
        r=fit(self.a,np.clip(self.a+.07,0,1));text=cube(r)
        table=np.array([[float(x) for x in line.split()] for line in text.splitlines() if line[0].isdigit()]).reshape(33,33,33,3)
        pixels=self.a.reshape(-1,3);position=pixels*32; low=np.floor(position).astype(int);frac=position-low
        interpolated=np.zeros_like(pixels)
        for blue in (0,1):
            for green in (0,1):
                for red in (0,1):
                    bits=np.array([red,green,blue]);indices=np.minimum(low+bits,32)
                    weight=np.prod(np.where(bits,frac,1-frac),axis=1)
                    interpolated+=table[indices[:,2],indices[:,1],indices[:,0]]*weight[:,None]
        error=np.abs(interpolated-transform(pixels,r))
        self.assertLess(float(np.percentile(error,95)),2e-6)
        self.assertLess(float(error.max()),2e-6)

    def test_real_png_jpeg_alpha_icc_exports(self):
        alpha=np.ones(self.a.shape[:2],dtype='float32');alpha[:,0]=0
        original=self.a.copy()
        png=encode(self.a,alpha,'PNG');a,al,notes=decode(png)
        self.assertEqual(a.shape,self.a.shape);np.testing.assert_array_equal(al,alpha)
        self.assertTrue(notes[0].startswith('Embedded'))
        jpeg=encode(self.a,alpha,'JPEG');a,al,_=decode(jpeg)
        self.assertIsNone(al);self.assertGreater(a[:,0].mean(),.98)
        np.testing.assert_array_equal(original,self.a)
        with self.assertRaises((ValueError,OSError)):decode(b'GIF89a'+b'\x00'*10)

    def test_exif_orientation_and_invalid_icc(self):
        image=Image.new('RGB',(20,10),'red');exif=Image.Exif();exif[274]=6
        buf=io.BytesIO();image.save(buf,format='JPEG',exif=exif)
        rgb,_,notes=decode(buf.getvalue());self.assertEqual(rgb.shape,(20,10,3));self.assertIn('assumed sRGB',notes[0])
        buf=io.BytesIO();image.save(buf,format='PNG',icc_profile=b'not a profile')
        with self.assertRaises(ValueError): decode(buf.getvalue())


if __name__=='__main__':unittest.main()
