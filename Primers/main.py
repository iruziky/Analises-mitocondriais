import primer_design_automation
import manager_fasta

from selenium import webdriver

import os
import pandas

def main():
    default_path = open('C:\\Users\\Iruziky\\Desktop\\Analises-mitocondriais\\Primers\\default_path.txt').read()
    fastas = os.listdir(default_path)

    driver = webdriver.Chrome()
    primer_blast_url = 'https://www.ncbi.nlm.nih.gov/tools/primer-blast/'

    columns = ["specie_name", "forward_primers", "forward_index", "reverse_primers", "reverse_index"]
    data_frame = pandas.DataFrame(columns=columns)

    manager_fasta.default_warning()

    for fasta in fastas:
        name, extension = get_file_extension(fasta)
        if not extension:
            continue

        fasta_path = os.path.join(default_path, fasta)

        if not manager_fasta.verify_quantity_contigs(fasta_path):
            manager_fasta.get_first_contig(fasta_path)

        driver.get(primer_blast_url)
        forward_primers, reverse_primers, forward_index, reverse_index = primer_design_automation.run_automation(fasta_path, driver)
        
        log_data(name, data_frame, forward_primers, reverse_primers, forward_index, reverse_index)

def get_file_extension(file):
    fasta_extensions = [".fasta", ".fa", ".fna"]
    name, extension = os.path.splitext(file)

    if not extension in fasta_extensions:
        print(f"A extensão do arquivo {file} não condiz com a de um arquivo fasta")
        return 0
    return name, extension

def log_data(name, data_frame, forward_primers, reverse_primers, forward_index, reverse_index):
    try:
        column_specie_name = [name] * 5
        new_columns = pandas.DataFrame({
            'specie_name': column_specie_name,
            'forward_primers': forward_primers,
            'forward_index': forward_index,
            'reverse_primers': reverse_primers,
            'reverse_index': reverse_index
        })
        data_frame = pandas.concat([data_frame, new_columns])
        data_frame.to_csv("Result_test.csv", index=False)

    except Exception as e:
            print(f"Ocorreu um erro ao processar os dados para o arquivo {name}\n",
                  "Ignorando arquivo e passando para o próximo\n")

if __name__ == "__main__":
    main()