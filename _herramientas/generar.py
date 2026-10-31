"""Genera las páginas de tutoriales y el menú lateral de SIG EDUCA.

Uso:  python3 _herramientas/generar.py
Para agregar un tutorial: escribe su contenido en _herramientas/contenido/<slug>.html
y agrega una entrada a TUTORIALES. Los temas sin página enlazan a la portada.
"""
import hashlib, html, pathlib, re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CANAL = "https://www.youtube.com/@SIG_EDUCA"

YT_ICON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .6 12 31 31 0 0 0 1 16.8a3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .4-4.8 31 31 0 0 0-.4-4.8ZM9.7 15.1V8.9l5.8 3.1Z"/></svg>'
IG_ICON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>'
LI_ICON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9.5h4V21H3Zm7 0h3.8v1.6h.1c.5-1 1.8-2 3.8-2 4 0 4.8 2.6 4.8 6V21h-4v-5.2c0-1.2 0-2.8-1.7-2.8s-2 1.3-2 2.7V21h-4Z"/></svg>'
REDES = [
    ("YouTube", "@SIG_EDUCA", CANAL, YT_ICON),
    ("Instagram", "@sig_educa", "https://www.instagram.com/sig_educa", IG_ICON),
    ("LinkedIn", "in/sig-educa", "https://www.linkedin.com/in/sig-educa", LI_ICON),
]

def pie():
    enlaces = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}" title="{n}">{i}</a>' for n, _, u, i in REDES)
    return f'<footer class="foot"><span>© 2026 SIG EDUCA</span><span class="redes">{enlaces}</span></footer>'

def contacto():
    tarjetas = "\n".join(f'''      <a class="red" href="{u}" target="_blank" rel="noopener"><span class="ic">{i}</span><span><strong>{n}</strong><small>{h}</small></span></a>''' for n, h, u, i in REDES)
    return f'''<!-- contacto:inicio -->
    <p>¿Tienes preguntas, sugerencias o quieres proponer un tema para un próximo tutorial? Escríbenos por cualquiera de nuestras redes.</p>
    <div class="redes-grid">
{tarjetas}
    </div>
    <!-- contacto:fin -->'''

# (grupo, slug o None, título, ancla en portada si no tiene página)
MENU = [
    ("Google Earth Engine", [
        ("registro-earth-engine", "Creación y registro en Earth Engine", None),
        ("importar-shapefile", "Importar shapefile en Earth Engine", None),
        ("filtrar-shapefiles", "Trabajar con shapefiles en Earth Engine", None),
    ]),
]

TUTORIALES = {
    "registro-earth-engine": {
        "titulo": "Creación y registro en Google Earth Engine",
        "descripcion": "Crea tu cuenta, registra un proyecto para uso no comercial y ejecuta tu primer script en Google Earth Engine.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "15 min",
        "video": "LoQwc3ne0FU",  # ID del video de YouTube
        "siguiente": ("Importar shapefile en Earth Engine", "tutoriales/importar-shapefile.html"),
    },
    "importar-shapefile": {
        "titulo": "Importar shapefile en Google Earth Engine",
        "descripcion": "Aprende en pocos minutos a subir un shapefile a tus assets y visualizarlo en el mapa de Google Earth Engine.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "10 min",
        "video": "4N9yYsmth0Q",
        "siguiente": ("Trabajar con shapefiles en Earth Engine", "tutoriales/filtrar-shapefiles.html"),
    },
    "filtrar-shapefiles": {
        "titulo": "Trabajar con shapefiles en Google Earth Engine",
        "descripcion": "Aprende a filtrar y visualizar correctamente shapefiles en Google Earth Engine con filter y filterMetadata.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "10 min",
        "video": "pusJLWYqUx4",
        "siguiente": ("Ruta de aprendizaje", "index.html#ruta"),
    },
}

def menu(prefijo, actual=None):
    base = f"{prefijo}index.html" if prefijo else ""
    partes = ['<nav class="side" id="side" aria-label="Secciones">',
              '    <h4>Inicio</h4>', '    <ul>',
              f'      <li><a href="{base}#inicio">Bienvenida</a></li>',
              f'      <li><a href="{base}#primeros-pasos">Primeros pasos</a></li>',
              f'      <li><a href="{base}#ruta">Ruta de aprendizaje</a></li>', '    </ul>']
    for grupo, items in MENU:
        partes += [f'    <h4>{grupo}</h4>', '    <ul>']
        for slug, titulo, ancla in items:
            href = f"{prefijo}tutoriales/{slug}.html" if slug else (f"{prefijo}index.html#{ancla}" if prefijo else f"#{ancla}")
            on = ' class="on" aria-current="page"' if slug and slug == actual else ''
            partes.append(f'      <li><a href="{href}"{on}>{titulo}</a></li>')
        partes.append('    </ul>')
    partes += ['    <h4>Más</h4>', '    <ul>']
    for ancla, t in [("contacto", "Contacto")]:
        partes.append(f'      <li><a href="{prefijo}index.html#{ancla}">{t}</a></li>' if prefijo else f'      <li><a href="#{ancla}">{t}</a></li>')
    partes += ['    </ul>', '  </nav>']
    return "\n".join(partes)

def cabecera(prefijo):
    return f'''<header class="top">
  <div class="top-in">
    <button class="menu-btn" id="menuBtn" aria-label="Abrir menú" aria-expanded="false">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
    <a class="brand" href="{prefijo}index.html"><img src="{prefijo}assets/img/logo-sig-educa.png" alt="SIG EDUCA" width="171" height="95"></a>
    <div class="search">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <input id="q" type="search" placeholder="Buscar" aria-label="Buscar">
    </div>
    <button class="theme-btn" id="themeBtn" type="button" role="switch" aria-checked="false" aria-label="Modo oscuro"><span class="knob"><svg class="sun" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg><svg class="moon" width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg></span></button>
    <a class="btn ghost" href="{CANAL}" target="_blank" rel="noopener">YouTube</a>
    <a class="btn" href="{prefijo}index.html#ruta">Tutoriales</a>
  </div>
</header>'''

def video(t):
    if t["video"]:
        return f'''<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{t["video"]}" title="{html.escape(t["titulo"])}" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>'''
    return f'''<div class="video pend"><div><p>Mira el video de este tutorial en el canal de SIG EDUCA.</p><a class="btn" href="{CANAL}/videos" target="_blank" rel="noopener">Ver en YouTube</a></div></div>'''

def pagina(slug, t):
    contenido = (RAIZ / "_herramientas/contenido" / f"{slug}.html").read_text()
    nivel, clase = t["nivel"]
    sig_t, sig_href = t["siguiente"]
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; frame-src https://www.youtube-nocookie.com; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(t["titulo"])} · SIG EDUCA</title>
<meta name="description" content="{html.escape(t["descripcion"])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="../assets/style.css">
<script src="../assets/theme.js"></script>
</head>
<body>
{cabecera("../")}

<div class="shell">
  {menu("../", slug)}

  <main>
    <div class="crumb">tutoriales / {html.escape(t["herramienta"].lower())}</div>
    <h1>{html.escape(t["titulo"])}</h1>
    <div class="meta-row"><span class="lvl {clase}">{nivel}</span><span>{t["duracion"]}</span><span>{html.escape(t["herramienta"])}</span></div>
    <p class="lead">{html.escape(t["descripcion"])}</p>
    {video(t)}
{contenido}
    <div class="pager two">
      <a href="../index.html#ruta"><small>Volver</small>← Ruta de aprendizaje</a>
      <a href="../{sig_href}"><small>Siguiente</small>{html.escape(sig_t)} →</a>
    </div>
    {pie()}
  </main>

  <aside class="toc" aria-label="En esta página">
    <h4>En esta página</h4>
    <ul id="toc"></ul>
  </aside>
</div>
<script src="../assets/tutorial.js"></script>
</body>
</html>
'''

def version(texto):
    """Agrega ?v=<hash> a los CSS/JS para que el navegador no use una copia vieja."""
    for nombre in ("style.css", "tutorial.js", "theme.js", "inicio.js"):
        h = hashlib.md5((RAIZ / "assets" / nombre).read_bytes()).hexdigest()[:8]
        texto = re.sub(rf'assets/{re.escape(nombre)}(\?v=\w+)?"', f'assets/{nombre}?v={h}"', texto)
    return texto

def main():
    for slug, t in TUTORIALES.items():
        (RAIZ / "tutoriales" / f"{slug}.html").write_text(version(pagina(slug, t)))
    idx = RAIZ / "index.html"
    s = idx.read_text()
    s = re.sub(r'<nav class="side" id="side".*?</nav>', lambda m: menu(""), s, count=1, flags=re.S)
    s = re.sub(r'<footer class="foot">.*?</footer>', lambda m: pie(), s, count=1, flags=re.S)
    s = re.sub(r'<!-- contacto:inicio -->.*?<!-- contacto:fin -->', lambda m: contacto(), s, count=1, flags=re.S)
    idx.write_text(version(s))
    print("Generados:", ", ".join(TUTORIALES))

if __name__ == "__main__":
    main()
