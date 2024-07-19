import log
import sys

def default_warning():
    print("\nATENÇÃO: Caso seus arquivos fasta possuam mais de uma contig, este programa irá sobrescrevê-los, resultando em arquivos contendo apenas sua primeira contig\n",
          "É INDISPENSÁVEL realizar um backup de seus fastas antes de executar este programa\n")
    response = input('Digite "sim" para confirmar:\n>> ')
    if not response == "sim":
        print("Encerrando a execução\n")
        sys.exit()

def verify_quantity_contigs(fasta_path):
    with open(fasta_path, "r") as file:
        fasta = file.read()
        contigs = fasta.split(">")
    count_contigs = len(contigs)

    if count_contigs > 2:
        return 0
    elif count_contigs < 2:
        log.writerLog(f"O arquivo fasta {fasta_path} não possui nenhuma contig\n")
        return -1
    return 1

def get_first_contig(fasta_path):
    first_contig = get_contig(fasta_path)
    save_fasta_formated(fasta_path, first_contig)

def get_contig(fasta_path):
    with open(fasta_path, "r") as file:
        contigs = file.read()
        first_contig = contigs.split(">")
    
    return ">" + first_contig[1]

def save_fasta_formated(fasta_path, first_contig):
    with open(fasta_path, "w") as file:
        file.write(first_contig)