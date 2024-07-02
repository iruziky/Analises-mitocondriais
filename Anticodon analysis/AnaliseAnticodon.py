import os
import pandas as pd

# Receba ume lista de nomes e retorna o nome do arquivo que contém os genes e transcritos
def searchGenesFile(nameFileLs):
    for nameFile in nameFileLs:
        # Buscando pelo arquivo que contém este padrão em seu nome
        if "_genes.fa" in nameFile or "_genes.fasta" in nameFile:
            return(nameFile)

# Lendo um arquivo e separando cada sequencia fasta nele contido
def readFile(targetFilePath):
    # Abrindo o arquivo alvo no modo leitura
    with open(targetFilePath, 'r') as file:
        targetFile = file.read() 
        
        # Separando o arquivo em cada sequência, as quais começam com ">"
        sequenceLs = targetFile.split(">")
    return sequenceLs

# Recebe uma lista de sequências nucleotídicas e retorna apenas as que são genes
def searchGenesSequences(sequenceLs):
    # Lista que será retornada como resultado
    genesLs = list()

    # Iterando sobre as sequências
    for sequence in sequenceLs:
        # Identificando se a sequência é um gene
        if not "RNA" in sequence and len(sequence) > 10:
            genesLs.append(sequence)
    
    # OBS: A condição len(sequence) > 10 é apenas para verificar se a sequência não está vazia
    # Lembrando que sequence inclui o cabeçalho (> ND1 ...) e seus aminoácidos 

    return(genesLs)

# Identificando se o anticodon está completo, ou qual aminoácido falta nele
def identifyAntiCodon(lastCodon):
    if (lastCodon in antiCodons):
        pass
    elif (lastCodon[-3] == "T"):
        if (lastCodon[-2] == "A"):
            lastCodon = "TA-"
        else:
            lastCodon = "T--"
    else:
        lastCodon = "---"
    
    return lastCodon

# Recebe um texto e escreve em um arquivo chamado log
def writerLog(text):
    with open('log_Analise_Anticodon.txt', 'a') as file:
        file.write(text)

# Informe o diretório pai, onde os outros diretórios estarão contidos
defaultDirPath = open('Caminho da pasta.txt').read()
# Obtendo os NOMES das pastas contidas no diretório pai
subDirLs = os.listdir(defaultDirPath)

writerLog("---------------------------------------------------------\n")

# Lista para armazenar as quantidades de genes em cada arquivo
qtGenesLs = list()

df = pd.DataFrame(columns=["Specie", "Gene", "Codon", "Anticodon"])

antiCodons = ["TAA", "TAG", "AGG", "AGA"]

# Iterando sobre os diretórios filhos
for subDir in subDirLs:
    # Obtendo o caminho completo da pasta filha
    subDirPath = os.path.join(defaultDirPath, subDir)
    # Obtendo o nome de todos arquivos contidos na pasta filha
    nameFileLs = os.listdir(subDirPath)

    # Verificando se a pasta está vazia
    if not nameFileLs:
        writerLog(f"A pasta {subDir} está vazia \n")
        continue

    # Toda manipulação de texto será feita sobre este arquivo
    targetFileName = searchGenesFile(nameFileLs)

    # Verificando se o arquivo alvo foi encontrado
    if not targetFileName:
        writerLog(f'A pasta {subDir} não possui um arquivo que tenha "_genes.fa" no nome \n')
        continue

    # Obtendo o caminho completo para o arquivo alvo
    targetFilePath = os.path.join(subDirPath, targetFileName)

    # Separando cada sequencia fasta contida no arquivo
    sequenceLs = readFile(targetFilePath)
    
    # Obtendo apenas as sequências de genes
    genesLs = searchGenesSequences(sequenceLs)
    # Registrando a quantidade de genes
    qtGenesLs.append(len(genesLs))

    # Obtendo os dados requisitados para cada sequência gênica
    for gene in genesLs:
        # Encontrando o primeiro " "
        spaceIndex = gene.index(" ")

        # Removendo as quebras de linha
        gene = gene.replace("\n", "")

        # Posição onde os nucleotídeos começam a serem listados
        startIndex = gene.index(")") + 1

        # Nome do gene
        nameGene = gene[:spaceIndex]
        # Primeiro códon
        startCodon = gene[startIndex:startIndex + 3]
        # último códon
        lastCodon = gene[-3:]

        antiCodon = identifyAntiCodon(lastCodon)

        # Criando um dicionário para uma nova linha
        new_data = {'Specie': subDir, 'Gene': nameGene, 'Codon':startCodon, 'Anticodon': antiCodon}

        # Convertendo o dicionário em um DataFrame
        new_data_df = pd.DataFrame([new_data])

        # Adicionando a nova linha ao DataFrame
        df = pd.concat([df, new_data_df], ignore_index=True)

writerLog(f"Quantidades de genes encontrados em seus arquivos: {set(qtGenesLs)}\nVerifique se esse número condiz com seus dados\n")
writerLog("---------------------------------------------------------\n\n")

# Salvando resultado
df.to_csv("Tabela_Resultado.csv")

print("\nUm arquivo de log foi gerado\n")