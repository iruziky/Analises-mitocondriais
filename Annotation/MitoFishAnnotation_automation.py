import navegation
import os

download_dir = "C:\\Users\\Iruziky\\Desktop\\Anotados - Novas Mitocôndrias"
fastas_dir = "\\Users\\Iruziky\\Desktop\\Arquivos Fasta"

# Criando o diretório de download se não existir
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Listando todos os arquivos fasta
fastas_list = os.listdir(fastas_dir)

for fasta_file in fastas_list:
    # Obtendo o caminho completo para o arquivo
    fasta_path = os.path.join(fastas_dir, fasta_file)
    # Separando o nome e a extensão do arquivo
    fasta_name, fasta_extension = os.path.splitext(fasta_file)

    try:
        if not navegation.get_annotations(fasta_path, download_dir):
            continue
    except:
        print("Ocorreu um erro ao obter os dados do arquivo\n", fasta_file)

    try:
        old_name = os.path.join(download_dir, "download.zip")
        new_name = os.path.join(download_dir, fasta_name + ".zip")
        os.rename(old_name, new_name)
    except:
        print("Ocorreu um erro ao tentar renomear o arquivo gerado como resultado\n \
              Limpe o diretório de resultados, insira seu caminho absoluto e tente novamente")
        exit()