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