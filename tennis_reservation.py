from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

USERNAME = "JECHAP"
PASSWORD = "238P"
PARTENAIRE = "Aurélien LANGE"

URL_LOGIN = "https://www.adsltennis.fr/5.11.00/"
URL_RESERVATION = "https://www.adsltennis.fr/5.11.00/reservation.php"

def create_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

def get_disponibilites():
    driver = create_driver()
    driver.get(URL_LOGIN)
    time.sleep(1)

    driver.find_element(By.NAME, "login").send_keys(USERNAME)
    driver.find_element(By.NAME, "mdp").send_keys(PASSWORD)
    driver.find_element(By.NAME, "valider").click()
    time.sleep(2)

    driver.get(URL_RESERVATION)
    time.sleep(2)

    slots = driver.find_elements(By.XPATH, "//td[contains(@style, 'green') and contains(text(), 'Simple')]")
    dispo = [slot.text for slot in slots]
    driver.quit()
    return {"disponibles": dispo}

def reserver_creneau(jour, heure):
    driver = create_driver()
    driver.get(URL_LOGIN)
    time.sleep(1)

    driver.find_element(By.NAME, "login").send_keys(USERNAME)
    driver.find_element(By.NAME, "mdp").send_keys(PASSWORD)
    driver.find_element(By.NAME, "valider").click()
    time.sleep(2)

    driver.get(URL_RESERVATION)
    time.sleep(2)

    creneaux = driver.find_elements(By.XPATH, f"//td[contains(text(), 'Simple') and contains(text(), '{jour}') and contains(text(), '{heure}')]")
    if not creneaux:
        driver.quit()
        return {"status": "fail", "message": "Créneau non trouvé"}

    creneaux[0].click()
    time.sleep(1)

    menu = driver.find_element(By.XPATH, "//select")
    for option in menu.find_elements(By.TAG_NAME, "option"):
        if PARTENAIRE in option.text:
            option.click()
            break

    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@value='Valider la réservation']").click()
    driver.quit()
    return {"status": "success", "message": f"Réservation faite pour {jour} à {heure} avec {PARTENAIRE}"}