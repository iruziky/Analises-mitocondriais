import os
import pandas as pd

def searchGenesFile(nameFiles):
    for nameFile in nameFiles:
        if "_genes.fa" in nameFile or "_genes.fasta" in nameFile:
            return(nameFile)

def readFile(targetFilePath):
    with open(targetFilePath, 'r') as file:
        targetFile = file.read() 
        
        sequences = targetFile.split(">")
    return sequences

def searchGeneSequences(sequences):
    genes = list()

    for sequence in sequences:
        if not "RNA" in sequence and len(sequence) > 10:
            genes.append(sequence)

    return(genes)

def getStopCodon(geneCleam):
    lengthSequence = len(geneCleam)

    restByThree = lengthSequence % 3
    if restByThree == 0:
        stopCodon = geneCleam[-3:]
    
    elif restByThree == 1:
        stopCodon = "-" + geneCleam[-2:]

    elif restByThree == 2:
        stopCodon = "--" + geneCleam[-1]

    return stopCodon

def writerLog(text):
    with open('StopCodon Analysis\\logAnaliseCodons.txt', 'a') as file:
        file.write(text)


defaultDirPath = open('StopCodon Analysis\\Caminho_da_pasta.txt').read()
subDirs = os.listdir(defaultDirPath)

writerLog("---------------------------------------------------------\n")

quantitydeGenes = list()

dataFrame = pd.DataFrame(columns=["Specie", "Gene", "Codon", "stopCodon"])

for subDir in subDirs:
    subDirPath = os.path.join(defaultDirPath, subDir)
    nameFiles = os.listdir(subDirPath)

    if not nameFiles:
        writerLog(f"A pasta {subDir} está vazia \n")
        continue

    targetFileName = searchGenesFile(nameFiles)

    if not targetFileName:
        writerLog(f'A pasta {subDir} não possui um arquivo que tenha "_genes.fa" no nome \n')
        continue

    targetFilePath = os.path.join(subDirPath, targetFileName)

    sequences = readFile(targetFilePath)
    
    genes = searchGeneSequences(sequences)
    quantitydeGenes.append(len(genes))

    for gene in genes:
        spaceIndex = gene.index(" ")

        gene = gene.replace("\n", "")

        startIndex = gene.index(")") + 1

        nameGene = gene[:spaceIndex]
        startCodon = gene[startIndex:startIndex + 3]

        geneCleam = gene[startIndex:]

        stopCodon = getStopCodon(geneCleam)

        new_data = {'Specie': subDir, 'Gene': nameGene, 'Codon':startCodon, 'stopCodon': stopCodon}

        new_data_df = pd.DataFrame([new_data])

        dataFrame = pd.concat([dataFrame, new_data_df], ignore_index=True)

writerLog(f"Quantidades de genes encontrados em seus arquivos: {set(quantitydeGenes)}\nVerifique se esse número condiz com seus dados\n")
writerLog("---------------------------------------------------------\n\n")

dataFrame.to_csv("StopCodon Analysis\\Tabela_Resultado.csv")

print("\nUm arquivo de log foi gerado\n")