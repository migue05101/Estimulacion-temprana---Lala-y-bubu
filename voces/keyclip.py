# Quita el fondo de croma de un video de Flow y produce un mp4 "lado a lado" (color | alfa) con el audio.
# uso: python3 keyclip.py entrada.mp4 salida.mp4 [alto=560] [verde|azul]
import sys, subprocess, json
import numpy as np, cv2

src, dst = sys.argv[1], sys.argv[2]
H = int(sys.argv[3]) if len(sys.argv) > 3 else 560
kind = sys.argv[4] if len(sys.argv) > 4 else 'verde'
info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate', '-of', 'json', src]))['streams'][0]
W0, H0 = info['width'], info['height']; fps = info['r_frame_rate']
raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'])
frames = np.frombuffer(raw, np.uint8).reshape(-1, H0, W0, 3)

def bgmask(f):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    if kind == 'verde': m = (h > 40) & (h < 90) & (s > 80) & (v > 50)
    else: m = (h > 95) & (h < 130) & (s > 90) & (v > 50)
    m = m.astype(np.uint8)
    # fondo = solo lo conectado con el borde (los puntos verdes de la ropa no se borran)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    # dentro del personaje solo se borran huecos grandes de croma puro (entre el pelo, bajo los brazos);
    # los puntos de colores de la ropa son pequeños y menos saturados, se quedan
    keep = [i for i in range(1, n) if i in border or (stats[i, cv2.CC_STAT_AREA] > 60 and hsv[..., 1][lab == i].mean() > 150)]
    return np.isin(lab, keep)

masks = [bgmask(f) for f in frames]
fg_any = np.zeros(masks[0].shape, bool)
for m in masks: fg_any |= ~m
ys, xs = np.where(fg_any)
pad = 24
x0, x1 = max(0, xs.min() - pad), min(W0, xs.max() + pad); y0, y1 = max(0, ys.min() - pad), min(H0, ys.max() + pad)
cw, ch = x1 - x0, y1 - y0
outW = int(round(cw * H / ch / 2)) * 2
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{outW * 2}x{H}', '-r', fps, '-i', '-',
                        '-i', src, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-preset', 'slow', '-crf', '21', '-pix_fmt', 'yuv420p',
                        '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', '-shortest', dst], stdin=subprocess.PIPE)
k3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)); k9 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
for f, m in zip(frames, masks):
    fg = (~m).astype(np.uint8) * 255
    fg = cv2.erode(fg, k3)
    alpha = cv2.GaussianBlur(fg, (5, 5), 0)
    col = f.astype(np.int16)
    band = cv2.dilate(m.astype(np.uint8), k9).astype(bool) & ~m          # borde: quitar el reflejo del croma
    b, g, r = col[..., 0], col[..., 1], col[..., 2]
    if kind == 'verde':
        lim = np.maximum(r, b); g[band] = np.minimum(g[band], lim[band])
    else:
        lim = np.maximum(r, g); b[band] = np.minimum(b[band], lim[band])
    col = np.clip(col, 0, 255).astype(np.uint8)
    col[m] = 0
    c = cv2.resize(col[y0:y1, x0:x1], (outW, H), interpolation=cv2.INTER_AREA)
    a = cv2.resize(alpha[y0:y1, x0:x1], (outW, H), interpolation=cv2.INTER_AREA)
    enc.stdin.write(np.hstack([c, cv2.cvtColor(a, cv2.COLOR_GRAY2BGR)]).tobytes())
enc.stdin.close(); enc.wait()
print(json.dumps({'crop': [int(x0), int(y0), int(cw), int(ch)], 'size': [outW, H], 'frames': len(frames)}))
