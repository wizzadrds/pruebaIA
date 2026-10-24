"""Lectura limitada de páginas web para el proyecto AgenteIA.

Módulo experimental independiente. No ejecuta JavaScript ni procesa instrucciones
de la página como instrucciones del agente.
"""
from __future__ import annotations

import ipaddress
import re
import socket
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

import requests

MAX_BYTES_PAGINA_WEB = 1_000_000
MAX_CARACTERES_PAGINA_WEB = 20_000
MAX_REDIRECCIONES_WEB = 5
TIMEOUT_CONEXION = 5
TIMEOUT_LECTURA = 15
USER_AGENT = "AgenteIA/1.0 (lector web local)"


class _ExtractorTextoHTML(HTMLParser):
    """Extrae texto visible básico sin ejecutar scripts."""
    _IGNORAR = {"script", "style", "noscript", "svg", "template"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.partes: list[str] = []
        self._pila: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in self._IGNORAR:
            self._pila.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in self._IGNORAR:
            for indice in range(len(self._pila) - 1, -1, -1):
                if self._pila[indice] == tag:
                    del self._pila[indice:]
                    break

    def handle_data(self, data: str) -> None:
        if not self._pila:
            texto = " ".join(data.split())
            if texto:
                self.partes.append(texto)


def _validar_url_publica(url: str) -> str:
    """Valida esquema, puerto y todas las IP resueltas del host."""
    if not isinstance(url, str) or not url.strip() or len(url) > 2000:
        raise ValueError("URL vacía o demasiado larga.")

    partes = urlsplit(url.strip())
    esquema = partes.scheme.lower()
    if esquema not in {"http", "https"}:
        raise ValueError("Solo se permiten URLs HTTP o HTTPS.")
    if not partes.hostname or partes.username is not None or partes.password is not None:
        raise ValueError("La URL debe tener un host y no incluir credenciales.")
    try:
        puerto = partes.port
    except ValueError as error:
        raise ValueError("Puerto de URL no válido.") from error
    if puerto not in (None, 80, 443):
        raise ValueError("Solo se permiten los puertos 80 y 443.")

    host = partes.hostname.rstrip(".").lower()
    if host == "localhost" or host.endswith(".localhost") or host.endswith(".local"):
        raise ValueError("Se rechazan nombres de host locales.")

    try:
        direcciones = [ipaddress.ip_address(host.strip("[]"))]
    except ValueError:
        try:
            resultados_dns = socket.getaddrinfo(
                host, puerto or (443 if esquema == "https" else 80),
                type=socket.SOCK_STREAM,
            )
        except socket.gaierror as error:
            raise ValueError("No se pudo resolver el host.") from error
        direcciones = []
        for dato in resultados_dns:
            try:
                direcciones.append(ipaddress.ip_address(dato[4][0].split("%")[0]))
            except ValueError as error:
                raise ValueError("El DNS devolvió una dirección no válida.") from error

    if not direcciones or any(not ip.is_global for ip in direcciones):
        raise ValueError("Se rechaza el host porque no todas sus IP son públicas.")
    return url.strip()


def leer_pagina_web(url: str) -> dict[str, str]:
    """Descarga texto HTML/plain de una URL pública y devuelve URL final y texto.

    Las redirecciones se procesan manualmente y cada destino se vuelve a validar.
    Nota: la validación DNS previa no elimina por completo el riesgo de DNS rebinding.
    Para uso adversarial, ejecutar tras un proxy de salida con bloqueo de redes privadas.
    """
    url_actual = _validar_url_publica(url)
    sesion = requests.Session()
    sesion.trust_env = False
    cabeceras = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,text/plain;q=0.9",
    }

    try:
        for salto in range(MAX_REDIRECCIONES_WEB + 1):
            _validar_url_publica(url_actual)
            respuesta = sesion.get(
                url_actual,
                headers=cabeceras,
                timeout=(TIMEOUT_CONEXION, TIMEOUT_LECTURA),
                allow_redirects=False,
                stream=True,
            )
            try:
                if respuesta.is_redirect or respuesta.is_permanent_redirect:
                    destino = respuesta.headers.get("Location")
                    if not destino:
                        raise ValueError("Redirección sin cabecera Location.")
                    if salto == MAX_REDIRECCIONES_WEB:
                        raise ValueError("Se superó el límite de redirecciones.")
                    url_actual = urljoin(url_actual, destino)
                    continue

                respuesta.raise_for_status()
                tipo = respuesta.headers.get("Content-Type", "").lower()
                es_texto_plano = tipo.startswith("text/plain")
                if not (
                    tipo.startswith("text/html")
                    or "application/xhtml+xml" in tipo
                    or es_texto_plano
                ):
                    raise ValueError("La URL no devuelve HTML ni texto plano.")

                longitud = respuesta.headers.get("Content-Length")
                if longitud:
                    try:
                        tamano_declarado = int(longitud)
                    except ValueError as error:
                        raise ValueError("Content-Length no válido.") from error
                    if tamano_declarado < 0 or tamano_declarado > MAX_BYTES_PAGINA_WEB:
                        raise ValueError("La página supera el límite de descarga.")

                bloques = []
                total = 0
                for bloque in respuesta.iter_content(chunk_size=16384):
                    if not bloque:
                        continue
                    total += len(bloque)
                    if total > MAX_BYTES_PAGINA_WEB:
                        raise ValueError("La página supera el límite de descarga.")
                    bloques.append(bloque)

                codificacion = respuesta.encoding or "utf-8"
                documento = b"".join(bloques).decode(codificacion, errors="replace")
            finally:
                respuesta.close()

            if es_texto_plano:
                texto = documento
            else:
                extractor = _ExtractorTextoHTML()
                extractor.feed(documento)
                extractor.close()
                texto = "\n".join(extractor.partes)

            texto = re.sub(r"\n{3,}", "\n\n", texto).strip()
            if not texto:
                raise ValueError("La página no contiene texto legible.")
            return {
                "url": url_actual,
                "texto": texto[:MAX_CARACTERES_PAGINA_WEB],
            }

        raise ValueError("No se pudo completar la lectura.")
    finally:
        sesion.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Lee texto de una página web pública.")
    parser.add_argument("url", help="URL HTTP/HTTPS pública")
    args = parser.parse_args()
    resultado = leer_pagina_web(args.url)
    print("URL final:", resultado["url"])
    print("Texto leído:")
    print(resultado["texto"])
