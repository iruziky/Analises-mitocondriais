import primer_scraping
import manager_fasta
import log

from selenium import webdriver

import os
from datetime import datetime
import pandas

def main():
    manager_fasta.default_warning()

    paths_file_path = 'C:\\Users\\Iruziky\\Desktop\\Analises-mitocondriais\\Primers\\default_path.txt'
    default_paths = open_paths_file(paths_file_path)

    driver = webdriver.Chrome()
    primer_blast_url = 'https://www.ncbi.nlm.nih.gov/tools/primer-blast/'

    for default_path in default_paths:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data_frame_name = f"Results_{timestamp}.csv"

        columns = ["specie_name", "forward_primers", "forward_index", "reverse_primers", "reverse_index"]
        data_frame = pandas.DataFrame(columns=columns)

        fastas = os.listdir(default_path)
        for fasta in fastas:
            name, extension = get_file_extension(fasta)
            if not extension:
                continue

            fasta_path = os.path.join(default_path, fasta)

            if not manager_fasta.verify_quantity_contigs(fasta_path):
                manager_fasta.get_first_contig(fasta_path)
            elif manager_fasta.verify_quantity_contigs(fasta_path) == -1:
                continue

            driver.get(primer_blast_url)
            forward_primers, reverse_primers, forward_index, reverse_index = primer_scraping.run_automation(fasta_path, driver)

            if not forward_primers:
                continue
            
            data_frame = log_data(name, data_frame, data_frame_name, forward_primers, reverse_primers, forward_index, reverse_index)

def open_paths_file(paths_file_path):
    with open(paths_file_path, "r") as file:
        paths_file = file.read()
        paths = paths_file.split("\n")
    return paths

def get_file_extension(file):
    fasta_extensions = [".fasta", ".fa", ".fna"]
    name, extension = os.path.splitext(file)

    if not extension in fasta_extensions:
        log.writerLog(f"A extensão do arquivo {file} não condiz com a de um arquivo fasta\n")
        return 0
    return name, extension

def log_data(name, data_frame, data_frame_name, forward_primers, reverse_primers, forward_index, reverse_index):
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
        data_frame.to_csv(data_frame_name, index=False)

    except Exception as e:
        log.writerLog(f"Ocorreu um erro ao processar os dados para o arquivo {name}\n {e} \nIgnorando e passando para o próximo\n")
    
    return data_frame

if __name__ == "__main__":
    main()