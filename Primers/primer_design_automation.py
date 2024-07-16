from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import sys

def run_automation(fasta_path, driver):
    set_primer_parameters(driver)
    upload_fasta_file(fasta_path, driver)
    run_primer_search(driver)
    wait_for_element_appear(driver)

    forward_primers, reverse_primers = get_primer_results(driver)
    forward_index, reverse_index = get_index_results(driver)

    return forward_primers, reverse_primers, forward_index, reverse_index

def set_primer_parameters(driver):
    product_maximum_value = "200"
    product_maximum_xpath = '//*[@id="PRIMER_PRODUCT_MAX"]'
    put_in_input_field(product_maximum_value, product_maximum_xpath, driver)

    num_return_value = "5"
    num_return_xpath = '//*[@id="PRIMER_NUM_RETURN"]'
    put_in_input_field(num_return_value, num_return_xpath, driver)

def put_in_input_field(value, xpath, driver):
    input_field = driver.find_element("xpath", xpath)
    input_field.clear()
    input_field.send_keys(value)

def upload_fasta_file(fasta_path, driver):
    choose_file_xpath = '//*[@id="upl"]'
    choose_file_button = driver.find_element("xpath", choose_file_xpath)

    try:
        choose_file_button.send_keys(fasta_path)

    except Exception as e:
        print("Ocorreu um erro ao inserir o arquivo\n", "Encerrando a execução\n", "Error: ", e)
        sys.exit()

def run_primer_search(driver):
    get_primers_button_xpath = '//*[@id="searchForm"]/div[3]/div[1]/input'
    get_primers_button = driver.find_element("xpath", get_primers_button_xpath)
    get_primers_button.click()
    # Adicionar uma verificação se o blast está executando corretamente

def wait_for_element_appear(driver):
    lead_time_maximum = 1800
    wait = WebDriverWait(driver, lead_time_maximum)

    try:
        element_waited_xpath = '//*[@id="content"]/div/div[3]/button'
        wait.until(EC.presence_of_element_located(("xpath", element_waited_xpath)))

    except TimeoutException:
        print("Uma execução do blast demorou mais de 10 minutos e está sendo encerrada.\n", "Tente novamente mais tarde.\n")
        # É possível os dados inseridos estejam incorretos. Neste caso, essa exceção será acionada, mas não deveria
        sys.exit()
        
    except Exception as e:
        print("Ocorreu um erro:", str(e))
        sys.exit()

def get_primer_results(driver):
    forward_primers_xpaths = '//*[@id="alignments"]/div/table/tbody/tr[2]/td[1]'
    reverse_primers_xpaths = '//*[@id="alignments"]/div/table/tbody/tr[3]/td[1]'

    forward_primers = driver.find_elements("xpath", forward_primers_xpaths)
    reverse_primers = driver.find_elements("xpath", reverse_primers_xpaths)

    return forward_primers, reverse_primers

def get_index_results(driver):
    forward_index_xpaths = '//*[@id="alignments"]/div/table/tbody/tr[2]/td[9]'
    reverse_index_xpaths = '//*[@id="alignments"]/div/table/tbody/tr[3]/td[9]'

    forward_index = driver.find_elements("xpath", forward_index_xpaths)
    reverse_index = driver.find_elements("xpath", reverse_index_xpaths)

    return forward_index, reverse_index