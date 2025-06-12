from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Path to the local ChromeDriver executable
chrome_driver_path = r"C:\tools\WebDriver\bin\chromedriver.exe"

# Start the driver service and launch Chrome
s = Service(chrome_driver_path)
driver = webdriver.Chrome(service=s)

# Configure Pandas output options
pd.set_option('display.max_rows', None)             # show all rows
pd.set_option('display.width', None)                # use full terminal width
pd.set_option('display.colheader_justify', 'left')  # left align headers

try:
    # Page containing the live ATP ranking
    url = "https://live-tennis.eu/it/classifica-atp-live"
    driver.get(url)

    # Wait for the table to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "u868"))
    )

    # Grab all table rows
    table = driver.find_element(By.ID, "u868")
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Header row has class="tbhead"; use its <td> cells as column headers
    header = []
    for row in rows:
        if "tbhead" in row.get_attribute("class"):
            header = [cell.text.strip() for cell in row.find_elements(By.TAG_NAME, "td")]
            break

    # Collect remaining rows as table data
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

    # Create the DataFrame and print it
    df = pd.DataFrame(data, columns=header)
    print(df).to_string(index=False)

except Exception as e:
    # Basic error handling
    print("Errore:", e)

finally:
    # Always close the browser
    driver.quit()
