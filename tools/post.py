# Hero post: bloom, grain, vignette, the DEIMOS title resolving after the lock, a fade to the page's black at the
# bottom, rounded corners and a hairline border; encode an animated WebP for GitHub.
import glob, sys, numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont
frames = sorted(glob.glob('frames/f_*.png'))
OUT_W = int(sys.argv[1]) if len(sys.argv) > 1 else 960
Q = int(sys.argv[2]) if len(sys.argv) > 2 else 70
rng = np.random.default_rng(1)
def font(size, want='Bold'):
    for i in range(14):
        try:
            f = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', size, index=i)
            if f.getname()[1] == want: return f
        except Exception: break
    return ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', size)
out = []
for n, fp in enumerate(frames, 1):
    im = Image.open(fp).convert('RGB')
    W, H = im.size
    a = np.asarray(im).astype(np.float32) / 255
    lum = a.max(2, keepdims=True)
    bright = np.clip((lum - .55) / .45, 0, 1) * a
    b = Image.fromarray((bright * 255).astype(np.uint8))
    bloom = (np.asarray(b.filter(ImageFilter.GaussianBlur(W / 90))).astype(np.float32) * .9 + np.asarray(b.filter(ImageFilter.GaussianBlur(W / 28))).astype(np.float32) * .7) / 255
    a = 1 - (1 - a) * (1 - np.clip(bloom, 0, 1))            # screen
    # lens chromatic aberration: red pushed out, blue pulled in, growing toward the edges
    def radial(ch, k):
        im_ = Image.fromarray((np.clip(ch, 0, 1) * 255).astype(np.uint8))
        w2, h2 = int(W * k), int(H * k)
        im_ = im_.resize((w2, h2), Image.BILINEAR)
        l, t = (w2 - W) // 2, (h2 - H) // 2
        return np.asarray(im_.crop((l, t, l + W, t + H))).astype(np.float32) / 255
    a = np.stack([radial(a[..., 0], 1.006), a[..., 1], radial(a[..., 2], 0.994) if False else a[..., 2]], -1)
    yy, xx = np.mgrid[0:H, 0:W]
    v = 1 - .5 * np.clip(((xx - W / 2) / (W / 1.6)) ** 2 + ((yy - H / 2) / (H / 1.25)) ** 2, 0, 1)
    a *= v[..., None]
    a += rng.normal(0, .018, a.shape)
    img = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    # the title, after the mark locks (frames 160..)
    t = np.clip((n - 158) / 18, 0, 1) * np.clip((216 - n) / 14, 0, 1)
    if t > 0:
        d = ImageDraw.Draw(img, 'RGBA')
        f1 = font(int(H * .135)); f2 = font(int(H * .036), 'Medium')
        title = 'D E I M O S'
        tw = d.textlength(title, font=f1)
        x = W * .075; y = H * .36
        d.text((x, y), title, font=f1, fill=(242, 240, 234, int(255 * t)))
        d.text((x + 4, y + H * .17), 'MISSION CONTROL FOR THE AGE OF AGENTS', font=f2, fill=(193, 68, 14, int(255 * t)))
    # fade the bottom to the page's black, rounded corners, hairline border
    a = np.asarray(img).astype(np.float32)
    fade = np.clip((yy - (H - H * .09)) / (H * .09), 0, 1)[..., None]
    a = a * (1 - fade) + np.array([5, 4, 10], np.float32) * fade
    img = Image.fromarray(a.astype(np.uint8)).resize((OUT_W, round(OUT_W * H / W)), Image.LANCZOS)
    w2, h2 = img.size
    mask = Image.new('L', (w2, h2), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, w2 - 1, h2 - 1), radius=16, fill=255)
    bg = Image.new('RGBA', (w2, h2), (0, 0, 0, 0)); img = img.convert('RGBA'); img.putalpha(mask)
    ImageDraw.Draw(img).rounded_rectangle((0, 0, w2 - 1, h2 - 1), radius=16, outline=(255, 255, 255, 34), width=1)
    out.append(img)
out[0].save('profile/assets/hero.webp', save_all=True, append_images=out[1:], duration=1000 // 24, loop=0, quality=Q, method=4)
still = out[190].copy(); still.save('profile/assets/hero-still.png')
import os; print('hero.webp', os.path.getsize('profile/assets/hero.webp') // 1024, 'KB', out[0].size)
