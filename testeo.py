from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

# Iniciar sesión en Instagram
def login_to_instagram(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "username")))
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

    # Esperar a que cargue el feed
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//nav")))
    time.sleep(2)

# Enviar mensaje a una conversación ya existente
def send_messages(driver, target_username, message, num_messages):
    # Ir a la bandeja de entrada de mensajes
    driver.get("https://www.instagram.com/direct/inbox/")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Mensajes')]")))
    time.sleep(3)

    # Buscar conversación por nombre de usuario
    try:
        convo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//div[text()='{target_username}']"))
        )
        convo.click()
    except:
        print(f"No se encontró una conversación existente con '{target_username}'.")
        return

    # Esperar y enviar mensajes
    for _ in range(num_messages):
        msg_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "textarea"))
        )
        msg_box.send_keys(message)
        msg_box.send_keys(Keys.RETURN)
        time.sleep(2)

# Pedir datos al usuario
target_username = input("👤 Usuario destino (debe haber conversación previa): ")
your_username = input("🔐 Tu usuario: ")
your_password = input("🔑 Tu contraseña: ")
num_messages = int(input("💬 Nº de mensajes a enviar: "))
message = input("✉️ Mensaje: ")

# Configuración del navegador
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=chrome_options)

try:
    login_to_instagram(driver, your_username, your_password)
    send_messages(driver, target_username, message, num_messages)
finally:
    time.sleep(5)
    driver.quit()
