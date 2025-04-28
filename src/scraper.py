import pandas as pd
import requests
from bs4 import BeautifulSoup
import time


BASE_URL = "https://www.tecnoempleo.com/ofertas-trabajo/?te=data+analyst&pr=231"

#Simulación de un navegador web para evitar bloqueos por parte del servidor
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def scraper_page(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    
    offers = []

    # Buscar todas las tarjetas de oferta
    cards = soup.find_all("div", class_="oferta")

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