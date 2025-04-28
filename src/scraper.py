import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.tecnoempleo.com/ofertas-trabajo/?te=data+analyst&pr=231"

def scrape_page(url):
    # Configuraciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    driver.get(url)

    # Esperar hasta que aparezcan las ofertas (máximo 15 segundos)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "oferta"))
        )
        print("Ofertas cargadas correctamente.")
    except:
        print("No se encontraron ofertas después de esperar.")

    #Aquí IMPRIMIMOOOOSS parte del HTML para diagnosticar:
    print(driver.page_source[:3000]) # Imprime los primeros 3000 caracteres del HTML

    offers = []

    cards = driver.find_elements(By.CLASS_NAME, "oferta")

    for card in cards:
        try:
            title = card.find_element(By.CLASS_NAME, "titulo").text.strip()
        except:
            title = None
        try:
            company = card.find_element(By.CLASS_NAME, "nombre-empresa").text.strip()
        except:
            company = None
        try:
            location = card.find_element(By.CLASS_NAME, "localidad").text.strip()
        except:
            location = None
        try:
            date = card.find_element(By.CLASS_NAME, "fecha").text.strip()
        except:
            date = None
        
        offer = {
            "Título": title,
            "Empresa": company,
            "Ubicación": location,
            "Fecha de publicación": date,
        }
        offers.append(offer)

    driver.quit()
    return offers

if __name__ == "__main__":
    print("Iniciando scrapeo con Selenium...")
    offers_data = []

    offers_data.extend(scrape_page(BASE_URL))

    df = pd.DataFrame(offers_data)
    df.to_csv("data/raw/ofertas_tecnoempleo.csv", index=False)

    print(f"Se extrajeron {len(df)} ofertas de empleo.")
    print("Scrapeo finalizado.")