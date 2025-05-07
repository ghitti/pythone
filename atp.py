from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

chrome_driver_path = r"C:\tools\WebDriver\bin\chromedriver.exe"
s = Service(chrome_driver_path)
driver = webdriver.Chrome(service=s)

# Imposta le opzioni di visualizzazione di Pandas

pd.set_option('display.max_rows', None)             # Nessun limite di righe
pd.set_option('display.width', None)                # Larghezza a terminale
pd.set_option('display.colheader_justify', 'left')  # Allinea intestazioni

try:
    url = "https://live-tennis.eu/it/classifica-atp-live"
    driver.get(url)

    # Aspetta che la tabella venga caricata
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "u868"))
    )

    table = driver.find_element(By.ID, "u868")
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Trova la riga con class="tbhead" e usa i <td> come intestazioni
    header = []
    for row in rows:
        if "tbhead" in row.get_attribute("class"):
            header = [cell.text.strip() for cell in row.find_elements(By.TAG_NAME, "td")]
            break

    # Leggi tutte le righe successive
    data = []
    start_collecting = False
    for row in rows:
        if "tbhead" in row.get_attribute("class"):
            start_collecting = True
            continue
        if start_collecting:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) == len(header):  
                data.append([col.text.strip() for col in cols])

    # Crea il DataFrame
    df = pd.DataFrame(data, columns=header)
    print(df).to_string(index=False)

except Exception as e:
    print("Errore:", e)

finally:
    driver.quit()