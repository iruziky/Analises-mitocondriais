# Utilidade
A partir de uma lista de pastas contendo anotações gênicas, esse algorítmo retorna uma tabela
Cada linha da tabela informa:
- Nome da pasta de origem da anotação
- Nome do gene
- Códon que inicia a sequência
- Anticódon (que finaliza)

Exemplo:</br>
Pygocentrus_nattereri,ATPase8,ATG,TAA</br>
Pygocentrus_nattereri,ATPase6,CTA,T--</br>
Pygocentrus_nattereri,COXIII,ATG,---</br>

Cada "-" representa um aminoácido que foi perdido no anticódon

# Requisito
- Você vai precisar fazer as anotações para suas espécies usando o MitoFish Annotator
- O MitoAnnotator gera uma pasta para cada espécie anotada
- Para funcionar com outros softwares de anotação, serão necessários alguns ajustes na identificação de alguns padrões

# Como usar
- Crie uma nova pasta e insira nela todas as pastas geradas pelo MitoAnnotator
- Edite o arquivo "Caminho da pasta.txt", inserindo o caminho da pasta que você criou no passe anterior
- OBS: Se estiver usando Windows, utilize o seguinte formato: C:\\<Caminho>\\<...>\\<Nome_da_pasta>
