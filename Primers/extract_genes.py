import os
import shutil

def main():
    default_path = 'C:\\Users\\Iruziky\\Desktop\\genes'
    results_path = 'C:\\Users\\Iruziky\\Desktop\\Extrair Genes'
    wanted_genes_names = ["COXI", "16S"]

    try:
        create_result_folders(wanted_genes_names, results_path)

        genes_files_names = os.listdir(default_path)

        for genes_file_name in genes_files_names:
            genes_file_path = os.path.join(default_path, genes_file_name)

            genes_file = read_file(genes_file_path)
            genes = genes_file.split(">")

            wanted_genes = get_wanted_genes(genes, wanted_genes_names)

            save_wanted_genes(wanted_genes, genes_file_name, results_path)
    except Exception as e:
        print(e)

def create_result_folders(wanted_genes_names, default_path):
    for wanted_gene_name in wanted_genes_names:
        folder_path = os.path.join(default_path, wanted_gene_name)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        os.mkdir(folder_path)

def read_file(genes_file_path):
    with open(genes_file_path, "r") as file:
        result = file.read()
        return result

def get_wanted_genes(genes, wanted_genes_names):
    results = list()
    for gene in genes:
        if not gene:
            continue

        gene_name = extract_gene_name(gene)

        if not gene_name:
            return 0
        
        if gene_name in wanted_genes_names:
            results.append(gene)
    return results

def extract_gene_name(gene):
    lines = gene.split("\n")
    first_line = lines[0]

    space_index = first_line.index(" ")
    gene_name = first_line[:space_index]
    return gene_name

def save_wanted_genes(wanted_genes, genes_file_name, results_path):
    for wanted_gene in wanted_genes:
        gene_name = extract_gene_name(wanted_gene)

        wanted_gene_file_path = os.path.join(results_path, gene_name, genes_file_name)
        with open(wanted_gene_file_path, "w") as file:
            file.write(">" + wanted_gene)

if __name__ == "__main__":
    main()