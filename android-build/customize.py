"""Turn the stock Capacitor Android project into Dream Ball: icons, splash, portrait lock,
immersive full screen, signing and version numbers. Run from the repo root:
    python3 android-build/customize.py app/android <versionCode>
"""
import os, re, sys, shutil, glob
from PIL import Image

root, code = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1
here = os.path.dirname(os.path.abspath(__file__))
main = os.path.join(root, 'app', 'src', 'main')
res = os.path.join(main, 'res')

# 1. icons (legacy, round and adaptive layers)
for d in os.listdir(os.path.join(here, 'res')):
    dst = os.path.join(res, d); os.makedirs(dst, exist_ok=True)
    for f in os.listdir(os.path.join(here, 'res', d)):
        shutil.copy(os.path.join(here, 'res', d, f), os.path.join(dst, f))
print('icons copied')

# 2. splash screens: replace every splash.png, keeping each one's size
splash = Image.open(os.path.join(here, 'splash.png')).convert('RGB')
for p in glob.glob(os.path.join(res, '**', 'splash.png'), recursive=True):
    w, h = Image.open(p).size
    bg = Image.new('RGB', (w, h), (18, 21, 44))
    s = min(w / splash.width, h / splash.height)
    im = splash.resize((max(1, int(splash.width * s)), max(1, int(splash.height * s))), Image.LANCZOS)
    bg.paste(im, ((w - im.width) // 2, (h - im.height) // 2)); bg.save(p)
    print('splash', p, w, h)

# 3. portrait lock on the main activity
mf = os.path.join(main, 'AndroidManifest.xml')
x = open(mf).read()
def lock(m):
    tag = m.group(0)
    if 'screenOrientation' not in tag: tag = tag.replace('<activity', '<activity\n            android:screenOrientation="portrait"', 1)
    return tag
x = re.sub(r'<activity[^>]*MainActivity[^>]*>', lock, x, flags=re.S)
open(mf, 'w').write(x); print('portrait lock', 'screenOrientation' in x)

# 4. immersive full screen, screen stays awake
ma = glob.glob(os.path.join(main, 'java', '**', 'MainActivity.java'), recursive=True)[0]
pkg = re.search(r'package\s+([\w.]+);', open(ma).read()).group(1)
open(ma, 'w').write(f'''package {pkg};

import android.os.Bundle;
import android.view.WindowManager;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {{
    @Override
    public void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        hideBars();
    }}

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {{
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) hideBars();
    }}

    private void hideBars() {{
        WindowInsetsControllerCompat c = WindowCompat.getInsetsController(getWindow(), getWindow().getDecorView());
        c.hide(WindowInsetsCompat.Type.systemBars());
        c.setSystemBarsBehavior(WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
    }}
}}
''')
print('fullscreen activity', ma)

# 5. signing + version numbers
bg = os.path.join(root, 'app', 'build.gradle')
g = open(bg).read()
ks = os.path.join(here, 'dreamball.keystore').replace('\\', '/')
if 'signingConfigs' not in g:
    g = g.replace('buildTypes {', f'''signingConfigs {{
        release {{
            storeFile file("{ks}")
            storePassword "treyyyverse"
            keyAlias "dreamball"
            keyPassword "treyyyverse"
        }}
    }}
    buildTypes {{''', 1)
g = re.sub(r'(buildTypes\s*\{\s*release\s*\{)', r'\1\n            signingConfig signingConfigs.release', g, count=1)
g = re.sub(r'versionCode\s+\d+', f'versionCode {code}', g)
g = re.sub(r'versionName\s+"[^"]*"', f'versionName "1.{code}"', g)
open(bg, 'w').write(g); print('signing + version', code)
