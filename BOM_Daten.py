import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Pfad zur CSV-Datei
csv_file_path = 'C:/Users/Basti/Downloads/FSE_CBOM_team349_v20240904_1736.csv'

# URL der Login-Seite
login_url = 'https://www.formulastudent.de/login/?L=0&redirect_url=%2Ffsg%2F'

# Login-Daten
username = 'basolbac'
password = 'Pa!Simson18S51'

# URL der Ziel-Website nach dem Login
target_url = 'https://www.formulastudent.de/teams/fse/details/bom/tid/349/'

# CSV-Datei einlesen
data = pd.read_csv(csv_file_path)

# CSV-Datei einlesen
data = pd.read_csv(csv_file_path)

# WebDriver starten (z.B. für Firefox)
driver = webdriver.Firefox()

try:
    # Login-Seite öffnen
    driver.get(login_url)

    # Warte auf das Laden der Login-Seite
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'user')))
    except TimeoutException:
        print("Timeout: Username field not found!")
        driver.save_screenshot('error_screenshot.png')
        driver.quit()
        exit()

    # Benutzername eingeben
    driver.find_element(By.ID, 'user').send_keys(username)

    # Passwort eingeben
    driver.find_element(By.ID, 'pass').send_keys(password)

    # Login-Button klicken
    driver.find_element(By.NAME, 'submit').click() # NAME oder ID muss unterschieden werden mittels Website-Ansicht

    # Warte, bis die Zielseite nach dem Login geladen ist
    WebDriverWait(driver, 5) #.until(EC.url_to_be(target_url))
    
    driver.get(target_url)
    
    wait = WebDriverWait(driver, 10)

    # Durch jede Zeile in der CSV-Datei iterieren
    for index, row in data.iterrows():
        # Schritt 1: Klicken auf "Add Part"
        add_part_button = driver.find_element(By.XPATH, "./html/body/div[1]/div/div/div[3]/div[2]/div[2]/div[2]/div[2]/div/div[1]/button[1]")
        add_part_button.click()

        # Schritt 2: System auswählen (Dropdown oder Liste)
        system_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'system_dropdown_id')))
        system_dropdown.click()

        # System aus der CSV auswählen
        system_option = driver.find_element(By.XPATH, f"//option[text()='{row['System']}']")
        system_option.click()

        # Schritt 3: Assembly auswählen (Dropdown oder Liste)
        assembly_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'assembly_dropdown_id')))
        assembly_dropdown.click()

        # Assembly aus der CSV auswählen
        assembly_option = driver.find_element(By.XPATH, f"//option[text()='{row['Assembly']}']")
        assembly_option.click()

        # Schritt 4: Part auswählen (Dropdown oder Liste)
        part_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'part_dropdown_id')))
        part_dropdown.click()

        # Part aus der CSV auswählen
        part_option = driver.find_element(By.XPATH, f"//option[text()='{row['Part']}']")
        part_option.click()

        # Schritt 5: Make or Buy auswählen (Checkbox)
        make_or_buy = row['MakeOrBuy']
        if make_or_buy.lower() == 'make':
            driver.find_element(By.ID, 'make_checkbox_id').click()
        elif make_or_buy.lower() == 'buy':
            driver.find_element(By.ID, 'buy_checkbox_id').click()

        # Schritt 6: Comments und Quantity ausfüllen
        driver.find_element(By.ID, 'comments_field_id').send_keys(str(row['Comments']))
        driver.find_element(By.ID, 'quantity_field_id').send_keys(str(row['Quantity']))

        # Formular absenden (z.B. Save oder Submit klicken)
        submit_button = driver.find_element(By.ID, 'submit_button_id')
        submit_button.click()

        # Optional: Warten auf das Nachladen der Seite oder Bestätigung
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'add_part_button_id')))

finally:
    # WebDriver schließen
    driver.quit()