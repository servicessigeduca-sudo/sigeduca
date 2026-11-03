"""Obtiene suscriptores, vistas y número de videos del canal de YouTube.

Lo ejecuta a diario la acción .github/workflows/estadisticas-youtube.yml y
deja el resultado en assets/datos/canal.json, que la portada lee para mostrar
las cifras. Usa la API de YouTube si existe el secreto YOUTUBE_API_KEY; si no,
lee la página pública del canal.
"""
import datetime, json, os, pathlib, re, sys, urllib.request

HANDLE = "SIG_EDUCA"
SALIDA = pathlib.Path(__file__).resolve().parent.parent / "assets/datos/canal.json"
UA = {"User-Agent": "Mozilla/5.0 (compatible; sigeduca-stats/1.0)", "Accept-Language": "en-US,en;q=0.8"}


def leer(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def con_api(clave):
    url = ("https://www.googleapis.com/youtube/v3/channels?part=statistics"
           f"&forHandle={HANDLE}&key={clave}")
    est = json.loads(leer(url))["items"][0]["statistics"]
    return {"suscriptores": int(est["subscriberCount"]), "vistas": int(est["viewCount"]),
            "videos": int(est["videoCount"])}


def numero(texto):
    """'1.23K subscribers' -> 1230 ; '45,678 views' -> 45678"""
    m = re.search(r"([\d.,]+)\s*([KMB])?", texto)
    if not m:
        return None
    n, suf = m.group(1), m.group(2)
    if suf:
        return round(float(n.replace(",", "")) * {"K": 1e3, "M": 1e6, "B": 1e9}[suf])
    return int(re.sub(r"[.,]", "", n))


def con_pagina():
    html = leer(f"https://www.youtube.com/@{HANDLE}/about")
    if os.environ.get("DEPURAR"):
        for k in ["subscriber", "viewCount", " views", "videoCount", " videos"]:
            for m in list(re.finditer(re.escape(k), html))[:4]:
                print(k, "=>", html[max(0, m.start()-120):m.end()+60].replace("\n", " "))
    datos = {}
    # Datos del recuadro "Acerca de" del propio canal (valores de texto plano;
    # los de canales recomendados vienen como objetos y no coinciden).
    for clave, patron in [("suscriptores", r'"subscriberCountText":"([^"]+)"'),
                          ("vistas", r'"viewCountText":"([^"]+)"'),
                          ("videos", r'"videoCountText":"([^"]+)"')]:
        m = re.search(patron, html)
        if m:
            datos[clave] = numero(m.group(1))
    if "suscriptores" not in datos:
        raise RuntimeError("No se encontraron las cifras en la página del canal")
    return datos


def main():
    clave = os.environ.get("YOUTUBE_API_KEY", "").strip()
    datos = con_api(clave) if clave else con_pagina()
    anterior = json.loads(SALIDA.read_text()) if SALIDA.exists() else {}
    sin_fecha = {k: v for k, v in anterior.items() if k != "actualizado"}
    if sin_fecha == datos:
        print("Sin cambios:", datos)
        return
    datos["actualizado"] = datetime.date.today().isoformat()
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(datos, ensure_ascii=False) + "\n")
    print("Actualizado:", datos)


if __name__ == "__main__":
    sys.exit(main())
