import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os

BASE_URL = "https://www.tecnoempleo.com/ofertas-trabajo/?te=data+analyst&pr=231"

# Simulación de un navegador web para evitar bloqueos por parte del servidor
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9"
}

# Configurar una sesión con reintentos
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1,  # tiempo de espera entre reintentos
    status_forcelist=[429, 500, 502, 503, 504],
    raise_on_status=False
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)

def scrape_page(url):
    try:
        response = session.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Lanza un error si el status code no es 200
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    offers = []

    # Buscar todas las tarjetas de oferta
    cards = soup.find_all("div", class_="oferta")

    if not cards:
        print("No se encontraron ofertas en la página. Puede que haya cambiado el HTML.")

    for card in cards:
        title = card.find("h2", class_="titulo").text.strip() if card.find("h2", class_="titulo") else None
        company = card.find("div", class_="nombre-empresa").text.strip() if card.find("div", class_="nombre-empresa") else None
        location = card.find("div", class_="localidad").text.strip() if card.find("div", class_="localidad") else None
        date = card.find("span", class_="fecha").text.strip() if card.find("span", class_="fecha") else None
        
        offer = {
            "Título": title,
            "Empresa": company,
            "Ubicación": location,
            "Fecha de publicación": date,
        }
        offers.append(offer)

    return offers

if __name__ == "__main__":
    offers_data = []

    # Crear la carpeta 'data/raw' si no existe
    os.makedirs("data/raw", exist_ok=True)

    print("Iniciando scrapeo...")
    offers_data.extend(scrape_page(BASE_URL))
    
    # Dormir 2 segundos (aunque sea 1 sola página, buena práctica)
    time.sleep(2)

    df = pd.DataFrame(offers_data)
    df.to_csv("data/raw/ofertas_tecnoempleo.csv", index=False, encoding="utf-8-sig")
    
    print(f"Se extrajeron {len(df)} ofertas de empleo.")
