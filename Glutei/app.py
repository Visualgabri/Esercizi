from pathlib import Path
from flask import Flask, request, url_for, send_from_directory
from markupsafe import Markup


app = Flask(__name__)

# Cartella radice: per default la stessa dove si trova app.py
ROOT_DIR = Path(__file__).parent.resolve()
ALLOWED_EXT = {".gif", ".jpg", ".jpeg", ".png", ".webp"}

def list_images(root: Path, recursive: bool) -> list[Path]:
    if recursive:
        return sorted(
            (p for p in root.rglob("*") if p.suffix.lower() in ALLOWED_EXT and p.is_file()),
            key=lambda p: p.as_posix().lower()
        )
    else:
        return sorted(
            (p for p in root.iterdir() if p.suffix.lower() in ALLOWED_EXT and p.is_file()),
            key=lambda p: p.as_posix().lower()
        )

@app.get("/file/<path:relpath>")
def serve_file(relpath: str):
    # Serviamo qualsiasi immagine partendo dalla radice
    safe_path = (ROOT_DIR / relpath).resolve()
    if ROOT_DIR in safe_path.parents or safe_path == ROOT_DIR:
        return send_from_directory(ROOT_DIR, relpath)
    return ("Forbidden", 403)

@app.get("/")
def index():
    # Parametri: ?recursive=1 per includere sottocartelle, ?w=160&h=120 per cambiare dimensioni
    recursive = request.args.get("recursive", "0") == "1"
    w = int(request.args.get("w", 160))
    h = int(request.args.get("h", 120))

    files = list_images(ROOT_DIR, recursive)
    count = len(files)

    # Costruiamo i tag <img> con alt = nome file
    imgs = []
    for p in files:
        rel = p.relative_to(ROOT_DIR).as_posix()
        src = url_for("serve_file", relpath=rel)
        alt = p.name
        imgs.append(f'<img src="{src}" alt="{alt}" loading="lazy">')

    gallery_html = "\n    ".join(imgs) if imgs else '<div class="empty">Nessuna immagine trovata.</div>'

    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8" />
  <title>Galleria dinamica</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root {{ --w:{w}px; --h:{h}px; }}
    html, body {{ margin:0; padding:0; background:#000; color:#ddd; font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif; }}
    header {{ position:sticky; top:0; background:#000; padding:12px; border-bottom:1px solid #222; display:flex; gap:12px; align-items:center; z-index:10; }}
    .pill {{ padding:6px 10px; border:1px solid #444; border-radius:999px; opacity:.8; }}
    .gallery {{ display:flex; flex-wrap:wrap; gap:0; padding:0; }}
    .gallery img {{ width:var(--w); height:var(--h); object-fit:contain; border:none; margin:0; padding:0; background:#000; display:block; }}
    .empty {{ padding:24px; opacity:.8; }}
    a, a:visited {{ color:#9ad; text-decoration:none; }}
  </style>
</head>
<body>
  <header>
    <div class="pill">Cartella: <strong>{ROOT_DIR.name}</strong></div>
    <div class="pill">Immagini: <strong>{count}</strong></div>
    <div class="pill">Sottocartelle: <strong>{"ON" if recursive else "OFF"}</strong> 
      (<a href="?recursive={'0' if recursive else '1'}&w={w}&h={h}">toggle</a>)
    </div>
    <div class="pill">Thumb: <strong>{w}×{h}</strong></div>
  </header>

  <div class="gallery">
    {Markup(gallery_html)}
  </div>
</body>
</html>"""
    return html

if __name__ == "__main__":
    # Avvia il server: http://127.0.0.1:5000/
    # Per cambiare cartella radice, lancia lo script da dentro la cartella che vuoi visualizzare.
    # In alternativa, imposta ROOT_DIR = Path("C:/Percorso/alla/cartella").resolve()
    app.run(debug=False, host="127.0.0.1", port=5000)
