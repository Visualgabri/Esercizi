import os

def genera_html_per_cartella(cartella):
    immagini = []
    estensioni_valide = ('.gif', '.jpg', '.jpeg', '.png')
    
    for nome_file in sorted(os.listdir(cartella)):
        if nome_file.lower().endswith(estensioni_valide):
            immagini.append(nome_file)

    if not immagini:
        print("❌ Nessuna immagine trovata nella cartella.")
        return

    nome_cartella = os.path.basename(os.path.abspath(cartella))
    nome_file_html = nome_cartella + ".html"
    output_path = os.path.join(cartella, nome_file_html)

    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <title>{nome_cartella}</title>
  <style>
    body {{ margin: 0; padding: 0; background: #000; }}
    .gallery {{ display: flex; flex-wrap: wrap; }}
    .gallery img {{ width: 160px; height: 120px; object-fit: contain; border: none; margin: 0; padding: 0; }}
  </style>
</head>
<body>
  <div class="gallery">
"""

    for immagine in immagini:
        html += f'    <img src="{immagine}" alt="{immagine}">\n'

    html += """  </div>
</body>
</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ File HTML creato: {output_path}")


if __name__ == "__main__":
    cartella_input = input("📂 Inserisci il percorso della cartella con le immagini: ").strip('"')
    if not os.path.isdir(cartella_input):
        print("❌ Cartella non trovata.")
    else:
        genera_html_per_cartella(cartella_input)
