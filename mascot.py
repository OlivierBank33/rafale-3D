"""Mascotte minuteaero : pilote en combinaison (stickers Gemini détourés dans mascot/stickers/).
Poses : neutral (parle : bouche animée + clignements), talk, talk_wide, blink, laugh, shocked, skeptical, wink_thumb,
point_right, point_up, facepalm, salute, celebrate, helmet, sign, thumbs_down, panic, arms_crossed, shrug.
draw(c, cx, bottom, h, pose='neutral', mouth=0..1, blink=0/1, pop=0..1, tilt=0, alpha=1)
  cx = centre horizontal ; bottom = y du bas du sticker (ligne 957/1024 de l'image) ; h = hauteur du carré 1024 à l'écran.
"""
import os, cairo, numpy as np
from PIL import Image, ImageDraw, ImageFilter

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mascot', 'stickers')
POSES = ['neutral', 'talk', 'talk_wide', 'blink', 'laugh', 'shocked', 'skeptical', 'wink_thumb', 'point_right', 'point_up',
         'facepalm', 'salute', 'celebrate', 'helmet', 'sign', 'thumbs_down', 'panic', 'arms_crossed', 'shrug']
_img, _surf = {}, {}


def _pil(name):
    if name not in _img: _img[name] = Image.open(os.path.join(DIR, name + '.png')).convert('RGBA')
    return _img[name]


def _mask(box, blur):
    m = Image.new('L', (1024, 1024), 0); ImageDraw.Draw(m).ellipse(box, fill=255); return m.filter(ImageFilter.GaussianBlur(blur))


def _to_surface(im):
    a = np.array(im).astype(np.float32)
    al = a[..., 3:4] / 255
    bgra = np.dstack([a[..., 2:3] * al, a[..., 1:2] * al, a[..., 0:1] * al, a[..., 3:4]]).astype(np.uint8)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, im.width, im.height)
    np.ndarray((im.height, s.get_stride() // 4, 4), np.uint8, s.get_data())[:, :im.width] = bgra
    s.mark_dirty(); return s


def _variant(key):
    """key = pose, ou ('neutral', mouth_level 0/1/2, blink 0/1) pour les états parlants."""
    if key in _surf: return _surf[key]
    if isinstance(key, tuple):
        _, ml, bl = key
        im = _pil('neutral').copy()
        if ml:
            p = _pil('talk' if ml == 1 else 'talk_wide')
            im.paste(p, (0, 0), Image.composite(p.getchannel('A'), Image.new('L', im.size, 0), _mask((415, 480, 610, 600), 14)))
        if bl:
            p = _pil('blink')
            im.paste(p, (0, 0), Image.composite(p.getchannel('A'), Image.new('L', im.size, 0), _mask((365, 345, 665, 445), 12)))
    else:
        im = _pil(key)
    # ombre portée douce
    a = im.getchannel('A').filter(ImageFilter.GaussianBlur(16))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: int(v * 0.45)))
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.paste(sh, (8, 14), sh); out.alpha_composite(im)
    _surf[key] = _to_surface(out); return _surf[key]


def draw(c, cx, bottom, h, pose='neutral', mouth=0.0, blink=0, pop=0.0, tilt=0.0, alpha=1.0):
    if pose == 'neutral':
        ml = 0 if mouth < 0.18 else (1 if mouth < 0.55 else 2)
        key = ('neutral', ml, 1 if blink else 0)
    else:
        key = pose
    s = _variant(key)
    k = h / 1024 * (1 + 0.14 * pop)
    c.save(); c.translate(cx, bottom); c.rotate(tilt - 0.05 * pop); c.scale(k, k)
    c.set_source_surface(s, -512, -957); c.paint_with_alpha(alpha)
    c.restore()


def mouth_level(env, ref):
    return np.clip((env / ref - 0.15) * 1.4, 0, 1)
