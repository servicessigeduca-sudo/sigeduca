"""Genera las páginas de tutoriales y el menú lateral de SIG EDUCA.

Uso:  python3 _herramientas/generar.py
Para agregar un tutorial: escribe su contenido en _herramientas/contenido/<slug>.html
y agrega una entrada a TUTORIALES. Los temas sin página enlazan a la portada.
"""
import hashlib, html, pathlib, re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CANAL = "https://www.youtube.com/@SIG_EDUCA"
SITIO = "https://servicessigeduca-sudo.github.io/sigeduca/"

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

CORREO = "servicessigeduca@gmail.com"
MAIL_ICON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="3"/><path d="m3 6 9 7 9-7"/></svg>'

def contacto():
    correo = f'''      <a class="red r-mail" href="mailto:{CORREO}"><span class="ic">{MAIL_ICON}</span><span><strong>Correo</strong><small>{CORREO}</small></span></a>'''
    tarjetas = correo + "\n" + "\n".join(f'''      <a class="red r-{n.lower()}" href="{u}" target="_blank" rel="noopener"><span class="ic">{i}</span><span><strong>{n}</strong><small>{h}</small></span></a>''' for n, h, u, i in REDES)
    return f'''<!-- contacto:inicio -->
    <p>¿Tienes preguntas, sugerencias o quieres proponer un tema para un próximo tutorial? Escríbenos al correo o por cualquiera de nuestras redes.</p>
    <div class="redes-grid">
{tarjetas}
    </div>
    <!-- contacto:fin -->'''

# (grupo, slug o None, título, ancla en portada si no tiene página)
# Cursos: agrupan las lecciones en orden. El menú lateral y la portada salen de aquí.
GEE_ICONO = "M7.853.717a1.19 1.19 0 00-.65.17L4.53 2.49c-.53.317-.732.984-.467 1.543l.93 1.958a9.217 9.217 0 00-1.745 3.076l-2.124.135A1.198 1.198 0 000 10.399v3.116a1.2 1.2 0 001.084 1.194l2.171.21a9.207 9.207 0 001.748 3.066l-.941 1.982a1.198 1.198 0 00.467 1.543l2.673 1.603a1.2 1.2 0 001.605-.347l1.22-1.771a9.22 9.22 0 001.971.216c.032 0 .064-.004.096-.004a9.245 9.245 0 001.876-.212l1.22 1.77a1.2 1.2 0 001.606.348l2.673-1.603c.53-.317.732-.984.467-1.543l-.941-1.982c.022-.025.048-.049.07-.076.066-.077.125-.159.188-.238a9.225 9.225 0 001.484-2.736l2.138-.137A1.198 1.198 0 0024 13.601v-3.116a1.2 1.2 0 00-1.084-1.194V9.29l-2.16-.21a9.182 9.182 0 00-1.501-2.786c-.063-.08-.124-.16-.19-.238-.018-.022-.039-.043-.058-.065l.93-1.958a1.198 1.198 0 00-.467-1.543L16.797.887a1.2 1.2 0 00-1.605.347L13.99 2.976a9.169 9.169 0 00-1.896-.219c-.033 0-.064-.004-.096-.004a9.2 9.2 0 00-1.992.223L8.808 1.234a1.2 1.2 0 00-.955-.517zm4.148 3.882c.574 0 1.13.072 1.668.197a7.41 7.41 0 015.384 4.993 7.36 7.36 0 01.332 2.193c0 .764-.116 1.5-.332 2.193a7.407 7.407 0 01-5.384 4.992 7.393 7.393 0 01-1.668.199c-4.071 0-7.384-3.313-7.384-7.384 0-4.07 3.313-7.383 7.384-7.383zM11.907 6C9.558 6 8.429 7.207 8.429 7.207c3.501-1.577 5.23 2.986 6.702 4.386 1.472 1.4 2.887.203 2.887.203-.012-.787-.252-1.533-.252-1.533-.968.168-1.398-.494-1.97-1.252C15.224 8.253 13.561 6 11.907 6zm-3.84 3.228c-.705.015-1.3.35-1.653 1-.868 1.601-.096 3.64-.096 3.64s.3-1.532 1.537-1.309c1.238.224 1.754 1.208 2.504 1.985.75.776 1.895 2.064 3.978 2.064 2.082 0 3.018-1.516 3.435-2.937v-.002l-.053.04c-1.265.98-3.335.882-4.548-.275-.89-.846-1.403-1.908-2.135-2.68-.981-1.038-2.065-1.545-2.97-1.526z"

CURSOS = [
    {
        "id": "curso-gee",
        "herramienta": "gee", "nivel": "básico",
        "tarjeta": "Del registro en la plataforma a la teledetección: vectores, DEM, Landsat, Sentinel-2, índices de vegetación, agua e inundaciones.",
        "titulo": "Google Earth Engine básico",
        "marca": "gee",
        "icono": GEE_ICONO,
        "descripcion": "Da tus primeros pasos en la nube de Google. Aprende a registrarte, a manejar datos vectoriales, a trabajar con modelos de elevación y a descargar imágenes de Landsat y Sentinel. Después crearás composiciones sin nubes, calcularás índices de vegetación, detectarás agua, mapearás inundaciones y extraerás cuerpos de agua, primero con Landsat 9 y luego con Sentinel-2.",
        "lecciones": ["registro-earth-engine", "importar-shapefile", "filtrar-shapefiles", "exportar-shapefile",
                      "descargar-dem", "analisis-terreno", "descargar-landsat-9", "descargar-sentinel-2",
                      "composicion-landsat", "composicion-sentinel-2",
                      "indices-vegetacion-landsat", "indices-vegetacion-sentinel-2",
                      "deteccion-agua-landsat", "deteccion-agua-sentinel-2",
                      "inundaciones-landsat", "inundaciones-sentinel-2",
                      "cuerpos-agua-landsat", "cuerpos-agua-sentinel-2"],
    },
    {
        "id": "curso-gee-intermedio",
        "herramienta": "gee", "nivel": "intermedio",
        "tarjeta": "Analiza colecciones completas: series de tiempo de Landsat y Sentinel-2, índices año a año, agua con DSWE y animaciones.",
        "titulo": "Google Earth Engine intermedio",
        "marca": "gee",
        "icono": GEE_ICONO,
        "descripcion": "Pasa de analizar una imagen a analizar colecciones completas. Construirás series de tiempo anuales con Landsat 4 a 9 y con Sentinel-2, calcularás índices espectrales año a año, clasificarás el agua superficial con el método DSWE del USGS (Jones, 2019), graficarás cómo cambia su área y crearás animaciones GIF de la serie.",
        "lecciones": ["serie-tiempo-landsat", "serie-tiempo-sentinel-2", "indices-serie-tiempo",
                      "agua-dswe", "area-agua-dswe", "gif-serie-tiempo"],
    },
    {
        "id": "curso-qgis",
        "herramienta": "qgis", "nivel": "básico",
        "tarjeta": "Instala el SIG de escritorio libre más usado del mundo. Muy pronto llegan nuevas lecciones.",
        "titulo": "QGIS básico",
        "marca": "qgis",
        "icono": "M12.879 13.006v3.65l-3.004-3.048v-3.495h3.582l2.852 2.893h-3.43zm10.886 7.606V24h-3.654l-5.73-5.9v-3.55h3.354l6.03 6.062zm-10.828-1.448l3.372 3.371c-1.309.442-2.557.726-4.325.726C5.136 23.26 0 18.243 0 11.565 0 4.92 5.136 0 11.984 0 18.864 0 24 4.952 24 11.565c0 2.12-.523 4.076-1.457 5.759l-3.625-3.725a8.393 8.393 0 0 0 .24-2.005c0-4.291-3.148-7.527-7.1-7.527-3.954 0-7.248 3.236-7.248 7.527s3.33 7.6 7.247 7.6c.548 0 .661.017.88-.03z",
        "descripcion": "Empieza con el SIG de escritorio libre más usado del mundo. Primero lo instalamos, y muy pronto llegan nuevas lecciones.",
        "lecciones": ["descargar-qgis"],
    },
]
# Rutas por herramienta: cada una agrupa sus cursos por nivel, de básico a avanzado.
# "proximos" son los niveles anunciados que todavía no tienen curso.
HERRAMIENTAS = [
    {"id": "gee", "nombre": "Google Earth Engine",
     "lema": "Teledetección y análisis geoespacial en la nube, programando en JavaScript.",
     "proximos": ["avanzado"]},
    {"id": "qgis", "nombre": "QGIS",
     "lema": "El SIG de escritorio libre para crear, editar y analizar mapas.",
     "proximos": []},
]
# Apps desarrolladas por SIG EDUCA. Cada app:
# {"nombre": ..., "descripcion": ..., "url": "https://...", "herramienta": "Google Earth Engine",
#  "imagen": "assets/img/apps/<archivo>.jpg" (opcional), "leccion": "<slug de tutorial>" (opcional)}
APPS = [
    {"nombre": "Easy Download DEMs",
     "descripcion": "Descarga un modelo digital de elevación de cualquier lugar del mundo sin registrarte ni programar. Dibuja tu área, elige el conjunto de datos y obtén un GeoTIFF ligero en pocos clics.",
     "tarjeta": "Descarga un modelo digital de elevación de cualquier lugar del mundo sin registrarte ni programar.",
     "etiquetas": ["SRTM", "NASADEM", "ALOS", "ASTER GED", "ETOPO1", "GTOPO30"],
     "url": "https://ee-sigeduca.projects.earthengine.app/view/easy-download-dems",
     "herramienta": "Google Earth Engine",
     "imagen": "assets/img/apps/easy-download-dems.jpg",
     "id": "easy-download-dems",
     "presentacion": "Conseguir un modelo digital de elevación suele exigir crear una cuenta en un portal, buscar las teselas de tu zona y unirlas a mano. Easy Download DEMs resuelve todo eso en el navegador: dibujas tu área sobre el mapa, eliges el conjunto de datos y obtienes un GeoTIFF recortado, listo para abrir en QGIS o ArcGIS Pro. No necesitas registrarte ni saber programar.",
     "pasos": ["Elige un modo de dibujo en el panel de la izquierda: Rectángulo o Polígono.",
               "Dibuja tu área de interés sobre el mapa. Puedes editarla o moverla antes de continuar.",
               "En el panel de la derecha, selecciona el modelo de elevación. El predeterminado es SRTM de 30 m.",
               "Revisa el modelo y el sombreado que aparecen en el mapa, pulsa <strong>Descargar MDE</strong> y luego el enlace <strong>Descargar</strong>.",
               "Recibirás un GeoTIFF en coordenadas geográficas (EPSG:4326). Según el modelo elegido, el resultado tarda de 1 a 3 minutos."],
     "datos": [["SRTM", "30 m", "NASA, misión del transbordador Endeavour (2000)"],
               ["NASADEM", "30 m", "NASA, reprocesamiento de SRTM con menos vacíos"],
               ["ALOS DSM", "30 m", "JAXA, modelo de superficie AW3D30"],
               ["ASTER GED", "100 m", "NASA JPL, elevación del producto de emisividad de ASTER"],
               ["ETOPO1", "1,8 km", "NOAA, relieve terrestre y batimetría"],
               ["GTOPO30", "1 km", "USGS, modelo global de 1996"]],
     "notas": ["Para áreas muy grandes con modelos de 30 m, el archivo puede superar el límite de descarga directa de Earth Engine. Si pasa, divide el área o elige un modelo de menor resolución.",
               "ALOS DSM es un modelo de superficie: incluye la altura de árboles y edificios. SRTM y NASADEM se acercan más al terreno, aunque en bosques densos también registran parte del dosel."]},
]

def bloque_apps():
    """Portada: galería de apps, cada una con una vista previa en un marco de navegador."""
    out = ["<!-- apps:inicio -->", '    <div class="apps">']
    for a in APPS:
        shot = (f'<img src="{a["imagen"]}" alt="Vista previa de {html.escape(a["nombre"])}" loading="lazy" width="960" height="540">'
                if a.get("imagen") else '<span class="app-sin-img">Vista previa próximamente</span>')
        chips = "".join(f"<li>{html.escape(e)}</li>" for e in a.get("etiquetas", []))
        out.append(f'''      <article class="app">
        <div class="app-shot">{shot}</div>
        <div class="app-body">
          <span class="app-tipo">App de {html.escape(a.get("herramienta", "Google Earth Engine"))}</span>
          <h3><a class="stretch" href="apps/{a["id"]}.html">{html.escape(a["nombre"])}</a></h3>
          <p>{html.escape(a.get("tarjeta", a["descripcion"]))}</p>
          {f'<ul class="app-chips" aria-label="Datos disponibles">{chips}</ul>' if chips else ''}
          <span class="btn app-cta">Conoce la app →</span>
        </div>
      </article>''')
    if not APPS:
        out.append('''      <article class="app prox"><div class="app-body"><h3>Muy pronto</h3><p>Estamos preparando las primeras apps.</p></div></article>''')
    out += ["    </div>", "    <!-- apps:fin -->"]
    return "\n".join(out)

NIVEL_NUM = {"básico": 1, "intermedio": 2, "avanzado": 3}

def cursos_de(h):
    return sorted([c for c in CURSOS if c["herramienta"] == h["id"]], key=lambda c: NIVEL_NUM[c["nivel"]])

def icono_herramienta(h):
    return next(c["icono"] for c in CURSOS if c["herramienta"] == h["id"])

MENU = [(c["titulo"], [(s, None, None) for s in c["lecciones"]]) for c in CURSOS]
NOMBRE_CORTO = {
    "registro-earth-engine": "Creación y registro", "importar-shapefile": "Importar shapefile",
    "filtrar-shapefiles": "Filtrar shapefiles", "exportar-shapefile": "Descargar shapefiles",
    "descargar-dem": "Descargar un DEM", "analisis-terreno": "Análisis de terreno",
    "descargar-landsat-9": "Imagen de Landsat 9", "descargar-sentinel-2": "Imagen de Sentinel-2",
    "composicion-landsat": "Composición con Landsat 9",
    "composicion-sentinel-2": "Composición con Sentinel-2",
    "indices-vegetacion-landsat": "Vegetación con Landsat 9",
    "indices-vegetacion-sentinel-2": "Vegetación con Sentinel-2",
    "deteccion-agua-landsat": "Agua con Landsat 9",
    "deteccion-agua-sentinel-2": "Agua con Sentinel-2",
    "inundaciones-landsat": "Inundaciones con Landsat 9",
    "inundaciones-sentinel-2": "Inundaciones con Sentinel-2",
    "cuerpos-agua-landsat": "Cuerpos de agua con Landsat 9",
    "cuerpos-agua-sentinel-2": "Cuerpos de agua con Sentinel-2",
    "serie-tiempo-landsat": "Series de tiempo con Landsat",
    "serie-tiempo-sentinel-2": "Series de tiempo con Sentinel-2",
    "indices-serie-tiempo": "Índices año a año",
    "agua-dswe": "Agua con DSWE",
    "area-agua-dswe": "Área de agua por año",
    "gif-serie-tiempo": "Animación GIF",
    "descargar-qgis": "Instalar QGIS",
}


def curso_de(slug):
    for c in CURSOS:
        if slug in c["lecciones"]:
            return c, c["lecciones"].index(slug) + 1, len(c["lecciones"])
    return None, 0, 0


def minutos(c):
    return sum(int(TUTORIALES[s]["duracion"].split()[0]) for s in c["lecciones"])


def lista_lecciones(c, prefijo):
    filas = []
    for n, s in enumerate(c["lecciones"], 1):
        t = TUTORIALES[s]
        filas.append(f'''        <li class="leccion" data-k="{t["claves"]}"><span class="l-num">{n:02d}</span><a href="{prefijo}tutoriales/{s}.html"><span class="l-tit">{html.escape(t["titulo"])}</span><span class="l-res">{html.escape(t["resumen"])}</span></a><span class="l-dur">{t["duracion"]}</span></li>''')
    return "\n".join(filas)


def meta_curso(c, con_nivel=True):
    n = len(c["lecciones"])
    nivel = f'<span>nivel {c["nivel"]}</span>' if con_nivel else ''
    return (f'<span class="tag gratis">gratis</span>{nivel}'
            f'<span>{n} {"lección" if n == 1 else "lecciones"}</span><span>{minutos(c)} min</span>')


def logo_curso(c):
    return f'<span class="curso-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{c["icono"]}"/></svg></span>'


def bloque_cursos():
    """Portada: una ruta por herramienta con sus cursos por nivel y, oculta, la lista de lecciones para el buscador."""
    out = ["<!-- cursos:inicio -->", '    <div class="rutas" id="cursos">']
    for h in HERRAMIENTAS:
        cs = cursos_de(h)
        if not cs:
            continue
        out.append(f'''      <section class="ruta c-{h["id"]}" aria-label="{html.escape(h["nombre"])}">
        <header class="ruta-cab"><span class="curso-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{icono_herramienta(h)}"/></svg></span><div><h3>{html.escape(h["nombre"])}</h3><p>{html.escape(h["lema"])}</p></div></header>
        <div class="cursos">''')
        for c in cs:
            claves = " ".join(TUTORIALES[sl]["claves"] + " " + TUTORIALES[sl]["titulo"] for sl in c["lecciones"])
            out.append(f'''          <article class="curso-card c-{c["marca"]}" data-k="{html.escape(claves.lower())}">
            <span class="nivel-paso">Nivel {NIVEL_NUM[c["nivel"]]} · {c["nivel"]}</span>
            <h4><a class="stretch" href="cursos/{c["id"]}.html">{html.escape(c["titulo"])}</a></h4>
            <p>{html.escape(c.get("tarjeta", c["descripcion"]))}</p>
            <div class="curso-meta">{meta_curso(c, False)}</div>
          </article>''')
        for nv in h["proximos"]:
            out.append(f'''          <article class="curso-card prox" aria-disabled="true">
            <span class="nivel-paso">Nivel {NIVEL_NUM[nv]} · {nv}</span>
            <h4>{html.escape(h["nombre"])} {nv}</h4>
            <p>Estamos preparando este curso. Mientras tanto, completa el nivel anterior.</p>
            <div class="curso-meta"><span>próximamente</span></div>
          </article>''')
        out.append("        </div>\n      </section>")
    out.append("    </div>")
    out.append('    <ol class="lecciones" id="busqueda" hidden>')
    for c in CURSOS:
        out.append(lista_lecciones(c, ""))
    out.append("    </ol>")
    out.append("    <!-- cursos:fin -->")
    return "\n".join(out)


def pagina_curso(c):
    primera = c["lecciones"][0]
    titulo = f"Curso {c['titulo']}"
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; frame-src https://www.youtube-nocookie.com; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(titulo)} · SIG EDUCA</title>
<meta name="description" content="{html.escape(c["descripcion"])}">
{seo(titulo + " · SIG EDUCA", c["descripcion"], f"cursos/{c['id']}.html", "../")}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="../assets/style.css">
<script src="../assets/theme.js"></script>
</head>
<body>
{cabecera("../")}

<div class="shell">
  {menu("../", curso=c["id"])}

  <main>
    <div class="crumb"><a href="../index.html#ruta">cursos</a> / {html.escape(c["titulo"].lower())}</div>
    <div class="curso-hero c-{c["marca"]}">{logo_curso(c)}<h1>{html.escape(titulo)}</h1></div>
    <div class="curso-meta grande">{meta_curso(c)}</div>
    <p class="lead">{html.escape(c["descripcion"])}</p>
    <a class="btn" href="../tutoriales/{primera}.html">Empezar el curso →</a>

    <h2 id="lecciones">Lecciones <a class="anchor" href="#lecciones" aria-label="Enlace a esta sección">#</a></h2>
    <ol class="lecciones">
{lista_lecciones(c, "../")}
    </ol>
    <div class="pager"><a href="../index.html#ruta"><small>Volver</small>← Todos los cursos</a></div>
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


INICIO_TITULO = "SIG EDUCA · Tutoriales de ArcGIS Pro, QGIS y Google Earth Engine"
INICIO_DESCRIPCION = "SIG EDUCA es una iniciativa educativa para fortalecer el aprendizaje de los SIG en español: ArcGIS Pro, QGIS y Google Earth Engine, paso a paso."

TUTORIALES = {
    "registro-earth-engine": {
        "resumen": "Crea tu cuenta, registra el proyecto y abre el Code Editor.",
        "claves": "registro cuenta crear proyecto google cloud earth engine inicio",
        "titulo": "Creación y registro en Google Earth Engine",
        "descripcion": "Crea tu cuenta, registra un proyecto para uso no comercial y ejecuta tu primer script en Google Earth Engine.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "15 min",
        "video": "LoQwc3ne0FU",  # ID del video de YouTube
        "siguiente": ("Importar shapefile en Earth Engine", "tutoriales/importar-shapefile.html"),
    },
    "importar-shapefile": {
        "resumen": "Sube un shapefile a tus assets y muéstralo en el mapa.",
        "claves": "shapefile shp importar subir asset featurecollection vector",
        "titulo": "Importar shapefile en Google Earth Engine",
        "descripcion": "Aprende en pocos minutos a subir un shapefile a tus assets y visualizarlo en el mapa de Google Earth Engine.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "10 min",
        "video": "4N9yYsmth0Q",
        "siguiente": ("Trabajar con shapefiles en Earth Engine", "tutoriales/filtrar-shapefiles.html"),
    },
    "filtrar-shapefiles": {
        "resumen": "Filtra con filter y filterMetadata y visualiza el resultado en el mapa.",
        "claves": "filtrar filter filtermetadata feature collection shapefile colombia bogota addlayer",
        "titulo": "Trabajar con shapefiles en Google Earth Engine",
        "descripcion": "Aprende a filtrar y visualizar correctamente shapefiles en Google Earth Engine con filter y filterMetadata.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "10 min",
        "video": "pusJLWYqUx4",
        "siguiente": ("Descargar shapefiles de Earth Engine", "tutoriales/exportar-shapefile.html"),
    },
    "exportar-shapefile": {
        "resumen": "Exporta una Feature Collection a Google Drive en formato SHP.",
        "claves": "exportar descargar shapefile shp export table todrive drive bogota",
        "titulo": "Descargar shapefiles de Google Earth Engine",
        "descripcion": "Aprende en pocos minutos a descargar correctamente un shapefile desde Google Earth Engine con Export.table.toDrive.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "5 min",
        "video": "L7pWd3Z1P1U",
        "siguiente": ("Descargar un DEM en Earth Engine", "tutoriales/descargar-dem.html"),
    },
    "descargar-dem": {
        "resumen": "Selecciona, recorta, visualiza y exporta un modelo digital de elevación.",
        "claves": "dem modelo digital elevacion alos srtm descargar export image geotiff",
        "titulo": "Descargar un DEM en Google Earth Engine",
        "descripcion": "Aprende a descargar Modelos Digitales de Elevación (DEM) en Google Earth Engine en 5 minutos o menos: seleccionar, recortar, visualizar y exportar.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "5 min",
        "video": "FJD6jEZ9P-o",
        "siguiente": ("Análisis de terreno en Earth Engine", "tutoriales/analisis-terreno.html"),
    },
    "analisis-terreno": {
        "resumen": "Calcula pendiente, aspecto y sombreado con ee.Terrain.products.",
        "claves": "terreno pendiente slope aspecto aspect sombreado hillshade morfometria dem terrain",
        "titulo": "Análisis de terreno en Google Earth Engine",
        "descripcion": "Calcula parámetros morfométricos de un DEM en Google Earth Engine: pendiente, aspecto y sombreado, y descárgalos a Google Drive.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "6 min",
        "video": "mep4lPZQKgc",
        "siguiente": ("Descargar imagen de Landsat 9", "tutoriales/descargar-landsat-9.html"),
    },
    "descargar-landsat-9": {
        "resumen": "Filtra por fecha, nubes y Path/Row, y exporta la imagen a Drive.",
        "claves": "landsat 9 imagen satelital path row wrs descargar reflectancia",
        "titulo": "Descargar imagen satelital de Landsat 9 en Google Earth Engine",
        "descripcion": "Aprende de manera sencilla a filtrar, visualizar y descargar imágenes satelitales de Landsat 9 desde Google Earth Engine.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "8 min",
        "video": "a7s_zqWZQ8c",
        "siguiente": ("Descargar imagen de Sentinel-2", "tutoriales/descargar-sentinel-2.html"),
    },
    "descargar-sentinel-2": {
        "resumen": "Filtra la colección Sentinel-2 y exporta una imagen a 10 m.",
        "claves": "sentinel 2 imagen satelital copernicus esa descargar nubes",
        "titulo": "Descargar imagen satelital de Sentinel-2 en Google Earth Engine",
        "descripcion": "Aprende de manera sencilla a filtrar, visualizar y descargar imágenes satelitales de Sentinel-2 desde Google Earth Engine.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "5 min",
        "video": "y1wd69VnOyA",
        "siguiente": ("Composición sin nubes con Landsat 9", "tutoriales/composicion-landsat.html"),
    },
    "composicion-landsat": {
        "resumen": "Combina muchas escenas de Landsat 9 en una mediana limpia de nubes.",
        "claves": "composicion mediana median nubes mascara cloud mask qa_pixel factor escala landsat 9",
        "titulo": "Composición sin nubes con Landsat 9 en Google Earth Engine",
        "descripcion": "Crea una composición de mediana sin nubes con Landsat 9 aplicando el factor de escala y la máscara QA_PIXEL, y expórtala a Google Drive.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "10 min",
        "video": None,
        "siguiente": ('Composición sin nubes con Sentinel-2', 'tutoriales/composicion-sentinel-2.html'),
    },
    "composicion-sentinel-2": {
        "resumen": "Crea una mediana sin nubes de Sentinel-2 con la máscara SCL.",
        "claves": "composicion mediana median nubes mascara cloud mask scl sentinel 2 calendarrange",
        "titulo": "Composición sin nubes con Sentinel-2 en Google Earth Engine",
        "descripcion": "Crea una composición de mediana sin nubes con Sentinel-2 usando la banda SCL, y expórtala a Google Drive a 10 m.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "10 min",
        "video": None,
        "siguiente": ('Índices de vegetación con Landsat 9', 'tutoriales/indices-vegetacion-landsat.html'),
    },
    "indices-vegetacion-landsat": {
        "resumen": "Calcula NDVI, EVI, SAVI, MSAVI, NDMI, NBR y NBR2 con Landsat 9.",
        "claves": "indices espectrales vegetacion ndvi evi savi msavi ndmi nbr nbr2 landsat 9 expression normalizeddifference",
        "titulo": "Índices de vegetación con Landsat 9 en Google Earth Engine",
        "descripcion": "Calcula, visualiza y exporta siete índices de vegetación con Landsat 9, y conoce quién propuso cada uno y para qué.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "15 min",
        "video": None,
        "siguiente": ('Índices de vegetación con Sentinel-2', 'tutoriales/indices-vegetacion-sentinel-2.html'),
    },
    "indices-vegetacion-sentinel-2": {
        "resumen": "Calcula siete índices de vegetación a 10 m con Sentinel-2.",
        "claves": "indices espectrales vegetacion ndvi evi savi msavi ndmi nbr nbr2 sentinel 2",
        "titulo": "Índices de vegetación con Sentinel-2 en Google Earth Engine",
        "descripcion": "Calcula, visualiza y exporta siete índices de vegetación con Sentinel-2 en Google Earth Engine.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "15 min",
        "video": None,
        "siguiente": ('Detección de agua con Landsat 9', 'tutoriales/deteccion-agua-landsat.html'),
    },
    "deteccion-agua-landsat": {
        "resumen": "Detecta el agua con NDWI, MNDWI y AWEInsh en Landsat 9.",
        "claves": "agua deteccion ndwi mndwi awei aweinsh rios cienagas lagos landsat 9",
        "titulo": "Detección de agua con Landsat 9 en Google Earth Engine",
        "descripcion": "Calcula NDWI, MNDWI y AWEInsh con Landsat 9 para detectar agua, y conoce el origen de cada índice.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "10 min",
        "video": None,
        "siguiente": ('Detección de agua con Sentinel-2', 'tutoriales/deteccion-agua-sentinel-2.html'),
    },
    "deteccion-agua-sentinel-2": {
        "resumen": "Detecta ríos y canales estrechos con NDWI, MNDWI y AWEInsh a 10 m.",
        "claves": "agua deteccion ndwi mndwi awei aweinsh rios canales sentinel 2",
        "titulo": "Detección de agua con Sentinel-2 en Google Earth Engine",
        "descripcion": "Calcula NDWI, MNDWI y AWEInsh con Sentinel-2 para detectar agua con 10 m de resolución.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "10 min",
        "video": None,
        "siguiente": ('Mapeo de inundaciones con Landsat 9', 'tutoriales/inundaciones-landsat.html'),
    },
    "inundaciones-landsat": {
        "resumen": "Compara el agua antes y después de una inundación y calcula el área en km².",
        "claves": "inundacion inundaciones flood mapeo area km2 pixelarea antes despues landsat 9 pakistan",
        "titulo": "Mapeo de inundaciones con Landsat 9 en Google Earth Engine",
        "descripcion": "Mapea una inundación con imágenes de Landsat 9 de antes y después, y calcula el área inundada en Google Earth Engine.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "15 min",
        "video": None,
        "siguiente": ('Mapeo de inundaciones con Sentinel-2', 'tutoriales/inundaciones-sentinel-2.html'),
    },
    "inundaciones-sentinel-2": {
        "resumen": "Mide el agua durante y después de una inundación con Sentinel-2.",
        "claves": "inundacion inundaciones flood mapeo area km2 pixelarea sentinel 2 monteria sinu cordoba",
        "titulo": "Mapeo de inundaciones con Sentinel-2 en Google Earth Engine",
        "descripcion": "Mapea una inundación con composiciones de Sentinel-2 y calcula el área cubierta por agua en cada periodo.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "15 min",
        "video": None,
        "siguiente": ('Extracción de cuerpos de agua con Landsat 9', 'tutoriales/cuerpos-agua-landsat.html'),
    },
    "cuerpos-agua-landsat": {
        "resumen": "Convierte una máscara de agua de Landsat 9 en polígonos y expórtalos como shapefile.",
        "claves": "cuerpos de agua extraer vectorizar reducetovectors poligonos shapefile shp connectedpixelcount landsat 9",
        "titulo": "Extracción de cuerpos de agua con Landsat 9 en Google Earth Engine",
        "descripcion": "Extrae ríos, ciénagas y lagunas como polígonos a partir de Landsat 9 y expórtalos como shapefile.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "15 min",
        "video": None,
        "siguiente": ('Extracción de cuerpos de agua con Sentinel-2', 'tutoriales/cuerpos-agua-sentinel-2.html'),
    },
    "cuerpos-agua-sentinel-2": {
        "resumen": "Extrae cuerpos de agua a 10 m y expórtalos como shapefile.",
        "claves": "cuerpos de agua extraer vectorizar reducetovectors poligonos shapefile shp connectedpixelcount sentinel 2",
        "titulo": "Extracción de cuerpos de agua con Sentinel-2 en Google Earth Engine",
        "descripcion": "Extrae cuerpos de agua como polígonos a partir de Sentinel-2 y expórtalos como shapefile desde Google Earth Engine.",
        "herramienta": "Google Earth Engine",
        "nivel": ("básico", "b"),
        "duracion": "15 min",
        "video": None,
        "siguiente": ("Series de tiempo con Landsat", "tutoriales/serie-tiempo-landsat.html"),
    },
    "serie-tiempo-landsat": {
        "resumen": "Une Landsat 4, 5, 7, 8 y 9 y crea una mediana sin nubes por año desde 1984.",
        "claves": "series de tiempo serie temporal multitemporal landsat 4 5 7 8 9 merge mediana anual coleccion imagecollection",
        "titulo": "Series de tiempo con Landsat 4 a 9 en Google Earth Engine",
        "descripcion": "Une las colecciones de Landsat 4, 5, 7, 8 y 9 y crea una mediana anual sin nubes para analizar cuatro décadas de cambios.",
        "herramienta": "Google Earth Engine",
        "nivel": ("intermedio", "i"),
        "duracion": "20 min",
        "video": None,
        "siguiente": ("Series de tiempo con Sentinel-2", "tutoriales/serie-tiempo-sentinel-2.html"),
    },
    "serie-tiempo-sentinel-2": {
        "resumen": "Crea una mediana anual sin nubes de Sentinel-2 a 10 m y exporta cada año.",
        "claves": "series de tiempo serie temporal multitemporal sentinel 2 harmonized mediana anual coleccion",
        "titulo": "Series de tiempo con Sentinel-2 en Google Earth Engine",
        "descripcion": "Crea una serie de medianas anuales sin nubes con Sentinel-2 y exporta cada año a Google Drive.",
        "herramienta": "Google Earth Engine",
        "nivel": ("intermedio", "i"),
        "duracion": "15 min",
        "video": None,
        "siguiente": ("Índices espectrales en series de tiempo", "tutoriales/indices-serie-tiempo.html"),
    },
    "indices-serie-tiempo": {
        "resumen": "Calcula NDVI, EVI, NDMI y MNDWI para cada año, grafícalos y mapea el cambio.",
        "claves": "indices espectrales series de tiempo ndvi evi ndmi mndwi grafico chart tendencia cambio landsat",
        "titulo": "Índices espectrales en series de tiempo con Landsat en Google Earth Engine",
        "descripcion": "Aplica una función de índices a toda una serie anual de Landsat, grafica su evolución y mapea dónde cambió la vegetación.",
        "herramienta": "Google Earth Engine",
        "nivel": ("intermedio", "i"),
        "duracion": "20 min",
        "video": None,
        "siguiente": ("Agua superficial con DSWE", "tutoriales/agua-dswe.html"),
    },
    "agua-dswe": {
        "resumen": "Aplica las cinco pruebas del método DSWE del USGS a una serie anual de Landsat.",
        "claves": "dswe dynamic surface water extent jones 2019 usgs agua superficial humedales clasificacion landsat",
        "titulo": "Agua superficial con DSWE (Jones, 2019) en Google Earth Engine",
        "descripcion": "Clasifica el agua superficial de cada año con el método DSWE del USGS, desarrollado por John W. Jones, sobre una serie de Landsat.",
        "herramienta": "Google Earth Engine",
        "nivel": ("intermedio", "i"),
        "duracion": "20 min",
        "video": None,
        "siguiente": ("Evolución del área de agua", "tutoriales/area-agua-dswe.html"),
    },
    "area-agua-dswe": {
        "resumen": "Calcula los km² de agua de cada año, grafica su evolución y expórtala a CSV.",
        "claves": "area de agua km2 pixelarea grafico evolucion dswe csv embalse cienaga sequia",
        "titulo": "Evolución del área de agua con DSWE en Google Earth Engine",
        "descripcion": "Calcula el área de agua de cada año a partir de DSWE, controla los huecos por nubes y grafica cómo cambia en el tiempo.",
        "herramienta": "Google Earth Engine",
        "nivel": ("intermedio", "i"),
        "duracion": "15 min",
        "video": None,
        "siguiente": ("Animación GIF de una serie de tiempo", "tutoriales/gif-serie-tiempo.html"),
    },
    "gif-serie-tiempo": {
        "resumen": "Convierte la serie anual y la máscara de agua en GIF con el año en cada cuadro.",
        "claves": "gif animacion timelapse getvideothumburl serie de tiempo texto año dswe",
        "titulo": "Animación GIF de una serie de tiempo en Google Earth Engine",
        "descripcion": "Crea animaciones GIF de una serie anual de Landsat y de su máscara de agua, con el año escrito en cada cuadro.",
        "herramienta": "Google Earth Engine",
        "nivel": ("intermedio", "i"),
        "duracion": "15 min",
        "video": None,
        "siguiente": ("Todos los cursos", "index.html#ruta"),
    },
    "descargar-qgis": {
        "resumen": "Instala QGIS LTR en Windows, macOS o Linux paso a paso.",
        "claves": "qgis instalar descargar windows mac macos linux ltr",
        "titulo": "Descargar e instalar QGIS",
        "descripcion": "Guía paso a paso para descargar e instalar QGIS LTR en Windows, macOS y Linux.",
        "herramienta": "QGIS",
        "nivel": ("básico", "b"),
        "duracion": "10 min",
        "video": "oT2Qb2FC4cY",
        "siguiente": ("Todos los cursos", "index.html#ruta"),
    },
}

def seo(titulo, descripcion, ruta, prefijo):
    """Etiquetas para buscadores y para la vista previa al compartir en redes."""
    url = SITIO + ruta
    tipo = "article" if ruta else "website"
    t, d = html.escape(titulo), html.escape(descripcion)
    return f'''<!-- seo:inicio -->
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="{prefijo}assets/img/favicon.png">
<link rel="apple-touch-icon" href="{prefijo}assets/img/apple-touch-icon.png">
<meta name="robots" content="index, follow">
<meta property="og:type" content="{tipo}">
<meta property="og:site_name" content="SIG EDUCA">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITIO}assets/img/compartir.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{SITIO}assets/img/compartir.png">
<!-- seo:fin -->'''

def pagina_app(a):
    titulo = f"{a['nombre']} · App de SIG EDUCA"
    pasos = "\n".join(f"      <li>{p}</li>" for p in a.get("pasos", []))
    datos = "".join(f'          <tr><td class="n">{html.escape(d[0])}</td><td>{html.escape(d[1])}</td><td>{html.escape(d[2])}</td></tr>\n' for d in a.get("datos", []))
    notas = "\n".join(f'    <div class="callout"><p>{n}</p></div>' for n in a.get("notas", []))
    abrir = f'<a class="btn" href="{html.escape(a["url"])}" target="_blank" rel="noopener">Abrir la app ↗</a>'
    secciones = ""
    if pasos:
        secciones += f'''
    <h2 id="como-usarla">Cómo usarla <a class="anchor" href="#como-usarla" aria-label="Enlace a esta sección">#</a></h2>
    <ol class="pasos-app">
{pasos}
    </ol>'''
    if datos:
        secciones += f'''
    <h2 id="datos">Datos disponibles <a class="anchor" href="#datos" aria-label="Enlace a esta sección">#</a></h2>
    <div class="tbl">
      <table>
        <thead><tr><th>Modelo</th><th>Resolución</th><th>Fuente</th></tr></thead>
        <tbody>
{datos}        </tbody>
      </table>
    </div>'''
    if notas:
        secciones += f'''
    <h2 id="ten-en-cuenta">Ten en cuenta <a class="anchor" href="#ten-en-cuenta" aria-label="Enlace a esta sección">#</a></h2>
{notas}'''
    img = (f'<img src="../{a["imagen"]}" alt="Captura de {html.escape(a["nombre"])}" width="960" height="540">' if a.get("imagen") else "")
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; frame-src https://www.youtube-nocookie.com; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(titulo)}</title>
<meta name="description" content="{html.escape(a["descripcion"])}">
{seo(titulo, a["descripcion"], f"apps/{a['id']}.html", "../")}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="../assets/style.css">
<script src="../assets/theme.js"></script>
</head>
<body>
{cabecera("../")}

<div class="shell">
  {menu("../", app=a["id"])}

  <main>
    <div class="crumb"><a href="../index.html#apps">apps</a> / {html.escape(a["nombre"].lower())}</div>
    <span class="app-tipo">App de {html.escape(a.get("herramienta", "Google Earth Engine"))} · gratis · sin registro</span>
    <h1>{html.escape(a["nombre"])}</h1>
    <p class="lead">{html.escape(a["descripcion"])}</p>
    <div class="app-hero">
      <div class="app-shot">{img}</div>
    </div>
    <div class="app-acciones">{abrir}</div>

    <h2 id="que-es">Qué es <a class="anchor" href="#que-es" aria-label="Enlace a esta sección">#</a></h2>
    <p>{a.get("presentacion", "")}</p>
{secciones}

    <div class="app-acciones fin">{abrir}</div>
    <div class="pager"><a href="../index.html#apps"><small>Volver</small>← Todas las apps</a></div>
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


def menu(prefijo, actual=None, curso=None, app=None):
    base = f"{prefijo}index.html" if prefijo else ""
    if actual and not curso:
        curso = (curso_de(actual)[0] or {}).get("id")
    partes = ['<nav class="side" id="side" aria-label="Secciones">', '    <ul>',
              f'      <li><a href="{base}#inicio">Inicio</a></li>',
              f'      <li><a href="{base}#primeros-pasos">Primeros pasos</a></li>',
              f'      <li><a href="{base}#ruta">Cursos</a></li>']
    for h in HERRAMIENTAS:
        cs = cursos_de(h)
        if not cs:
            continue
        h_abierta = " open" if any(c["id"] == curso for c in cs) else ""
        partes += [f'      <li class="grupo"><details{h_abierta}>',
                   f'        <summary>{html.escape(h["nombre"])}</summary>', '        <ul>']
        for c in cs:
            abierto = " open" if c["id"] == curso else ""
            partes += [f'          <li class="grupo nivel"><details{abierto}>',
                       f'            <summary>Nivel {c["nivel"]}</summary>', '            <ul>']
            on = ' class="on" aria-current="page"' if c["id"] == curso and not actual else ''
            partes.append(f'              <li><a href="{prefijo}cursos/{c["id"]}.html"{on}>Presentación del curso</a></li>')
            for n, slug in enumerate(c["lecciones"], 1):
                on = ' class="on" aria-current="page"' if slug == actual else ''
                completo = html.escape(TUTORIALES[slug]["titulo"])
                partes.append(f'              <li><a href="{prefijo}tutoriales/{slug}.html"{on} title="{completo}">{n}. {NOMBRE_CORTO.get(slug, completo)}</a></li>')
            partes += ['            </ul>', '          </details></li>']
        partes += ['        </ul>', '      </details></li>']
    a_abierta = " open" if app else ""
    partes += [f'      <li class="grupo"><details{a_abierta}>',
               '        <summary>Apps</summary>', '        <ul>']
    for a in APPS:
        on = ' class="on" aria-current="page"' if a["id"] == app else ''
        partes.append(f'          <li><a href="{prefijo}apps/{a["id"]}.html"{on}>{html.escape(a["nombre"])}</a></li>')
    partes += ['        </ul>', '      </details></li>']
    partes.append(f'      <li><a href="{base}#contacto">Contacto</a></li>')
    partes += ['    </ul>', '  </nav>']
    return "\n".join(partes)


def cabecera(prefijo):
    return f'''<header class="top">
  <div class="top-in">
    <button class="menu-btn" id="menuBtn" aria-label="Abrir menú" aria-expanded="false">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
    <a class="brand" aria-label="SIG EDUCA, inicio" href="{prefijo}index.html"><img src="{prefijo}assets/img/logo-sig-educa.png" alt="" width="90" height="112"><span class="brand-txt">SIG <b>EDUCA</b></span></a>
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
    return ""


# ---- Resaltado de sintaxis JavaScript (se hace al generar, sin scripts en el navegador) ----
_JS_KW = {"var", "let", "const", "function", "return", "if", "else", "for", "while", "do",
          "new", "typeof", "in", "of", "this", "break", "continue", "switch", "case", "default"}
_JS_LIT = {"true", "false", "null", "undefined"}
_JS_GLOBAL = {"ee", "Map", "Export", "print", "ui", "Math", "require", "JSON", "Number", "String"}
_JS_TOKEN = re.compile(r"""(?P<c>//[^\n]*|/\*[\s\S]*?\*/)
  |(?P<s>'(?:\\.|[^'\\\n])*'|"(?:\\.|[^"\\\n])*"|`(?:\\.|[^`\\])*`)
  |(?P<n>\b\d+(?:\.\d+)?(?:[eE][-+]?\d+)?\b|\.\d+\b)
  |(?P<id>[A-Za-z_$][\w$]*)""", re.X)

def _resaltar_js(texto):
    salida, pos = [], 0
    def span(clase, t):
        return f'<span class="{clase}">{html.escape(t, quote=False)}</span>'
    for m in _JS_TOKEN.finditer(texto):
        salida.append(html.escape(texto[pos:m.start()], quote=False))
        t = m.group()
        if m.lastgroup == "id":
            resto = texto[m.end():].lstrip(" ")
            if t in _JS_KW:
                salida.append(span("k", t))
            elif t in _JS_LIT:
                salida.append(span("n", t))
            elif t in _JS_GLOBAL:
                salida.append(span("g", t))
            elif resto.startswith("("):
                salida.append(span("f", t))
            else:
                salida.append(html.escape(t, quote=False))
        else:
            salida.append(span(m.lastgroup, t))
        pos = m.end()
    salida.append(html.escape(texto[pos:], quote=False))
    return "".join(salida)

def resaltar_codigo(contenido):
    def un_bloque(m):
        plano = html.unescape(re.sub(r"</?span[^>]*>", "", m.group(2)))
        return m.group(1) + _resaltar_js(plano) + "</pre>"
    return re.sub(r"(<pre>)(.*?)</pre>", un_bloque, contenido, flags=re.S)

def pagina(slug, t):
    contenido = resaltar_codigo((RAIZ / "_herramientas/contenido" / f"{slug}.html").read_text())
    nivel, clase = t["nivel"]
    sig_t, sig_href = t["siguiente"]
    c, n, total = curso_de(slug)
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; frame-src https://www.youtube-nocookie.com; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(t["titulo"])} · SIG EDUCA</title>
<meta name="description" content="{html.escape(t["descripcion"])}">
{seo(t["titulo"] + " · SIG EDUCA", t["descripcion"], f"tutoriales/{slug}.html", "../")}
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
    <div class="crumb"><a href="../index.html#ruta">cursos</a> / <a href="../cursos/{c["id"]}.html">{html.escape(c["titulo"].lower())}</a></div>
    <h1>{html.escape(t["titulo"])}</h1>
    <div class="meta-row"><span class="lvl {clase}">{nivel}</span><span>Lección {n} de {total}</span><span>{t["duracion"]}</span><span>{html.escape(t["herramienta"])}</span></div>
    <p class="lead">{html.escape(t["descripcion"])}</p>
    {video(t)}
{contenido}
    <div class="pager two">
      <a href="../cursos/{c["id"]}.html"><small>Volver al curso</small>← {html.escape(c["titulo"])}</a>
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
    (RAIZ / "cursos").mkdir(exist_ok=True)
    for c in CURSOS:
        (RAIZ / "cursos" / f"{c['id']}.html").write_text(version(pagina_curso(c)))
    (RAIZ / "apps").mkdir(exist_ok=True)
    for a in APPS:
        (RAIZ / "apps" / f"{a['id']}.html").write_text(version(pagina_app(a)))
    idx = RAIZ / "index.html"
    s = idx.read_text()
    s = re.sub(r'<nav class="side" id="side".*?</nav>', lambda m: menu(""), s, count=1, flags=re.S)
    s = re.sub(r'<footer class="foot">.*?</footer>', lambda m: pie(), s, count=1, flags=re.S)
    s = re.sub(r'<!-- cursos:inicio -->.*?<!-- cursos:fin -->', lambda m: bloque_cursos(), s, count=1, flags=re.S)
    s = re.sub(r'<!-- apps:inicio -->.*?<!-- apps:fin -->', lambda m: bloque_apps(), s, count=1, flags=re.S)
    s = re.sub(r'<!-- contacto:inicio -->.*?<!-- contacto:fin -->', lambda m: contacto(), s, count=1, flags=re.S)
    s = re.sub(r'<!-- seo:inicio -->.*?<!-- seo:fin -->', lambda m: seo(INICIO_TITULO, INICIO_DESCRIPCION, "", ""), s, count=1, flags=re.S)
    idx.write_text(version(s))
    # Mapa del sitio para Google y Bing
    urls = ([SITIO] + [f"{SITIO}cursos/{c['id']}.html" for c in CURSOS]
            + [f"{SITIO}tutoriales/{slug}.html" for slug in TUTORIALES]
            + [f"{SITIO}apps/{a['id']}.html" for a in APPS])
    (RAIZ / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    print("Generados:", ", ".join(TUTORIALES))

if __name__ == "__main__":
    main()
