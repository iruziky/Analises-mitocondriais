from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def get_annotations(fasta_path, download_dir):
    # Configurando o navegador
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    prefs = {
        "download.default_directory": download_dir,
    }
    options.add_experimental_option("prefs", prefs)

    # Obtendo um navegador
    driver = webdriver.Chrome(options=options)

    # Configurando o tempo padrão de espera explícita
    wait = WebDriverWait(driver, 120)

    # Acessando o MitoFish Annotator
    driver.get("https://mitofish.aori.u-tokyo.ac.jp/annotation/input/")

    upload_file = os.path.abspath(fasta_path)

    # Certificando-se de que o arquivo existe
    if not os.path.exists(upload_file):
        print(f"Arquivo não encontrado: {upload_file}")
        return 0

    # Inserindo o arquivo no campo de input
    input_field = driver.find_element("xpath", '//*[@id="content"]/main/form/div[1]/div[1]/div/input')
    input_field.send_keys(upload_file)

    # Clicando no botão de gerar anotações
    driver.find_element("xpath", '//*[@id="content"]/main/form/div[2]/input').click()

    # Esperando o botão de resultados aparecer
    button_results = wait.until(EC.presence_of_element_located(("xpath", '//div/div[4]/p/a')))
    # Clicando no botão de resultados
    button_results.click()

    # Esperando um momento para a nova aba abrir
    time.sleep(2)

    # Obtendo todas as janelas abertas
    window_handles = driver.window_handles

    # Alternando para a nova aba (a última aberta)
    driver.switch_to.window(window_handles[-1])

    # Clicando no botão de fazer download
    driver.find_element("xpath", '//*[@id="content"]/main/div[3]/a').click()

    # Esperando o download ser concluído
    time.sleep(5)

    return 1