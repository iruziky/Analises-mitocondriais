import primer_design_automation
from selenium import webdriver

def main():
    fasta_path = 'C:\\Users\\Iruziky\\Desktop\\Analises-mitocondriais\\Primers\\teste.fasta'

    driver = webdriver.Chrome()

    primer_blast_url = 'https://www.ncbi.nlm.nih.gov/tools/primer-blast/'
    driver.get(primer_blast_url)

    forward_primers, reverse_primers, forward_index, reverse_index = primer_design_automation.run_automation(fasta_path, driver)

if __name__ == "__main__":
    main()