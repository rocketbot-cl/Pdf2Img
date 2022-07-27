# Pdf2Img
  
Módulo para realizar ações com um arquivo pdf  

*Read this in other languages: [English](Manual_Pdf2Img.md), [Portugues](Manual_Pdf2Img.pr.md), [Español](Manual_Pdf2Img.es.md).*
  
## Como instalar este módulo
  
__Baixe__ e __instale__ o conteúdo na pasta 'modules' no caminho do Rocketbot  



## Descrição do comando

### Converter para JPG
  
Converter cada folha de um arquivo pdf para o formato jpg
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Inserir PDF|Localização da pasta onde se encontra o PDF a converter para JPG|arquivo.pdf|
|Caminho e nome do arquivo jpg para salvar|Local e nome do arquivo jpg a ser salvo. Se o pdf contiver mais de uma folha, o número da folha será adicionado aos arquivos|C:/Users/User/Desktop/imagem.jpg|
|Resultado|Variável onde será armazenado True ou False dependendo se o módulo foi capaz de executar a ação|variável|

### Adicionar imagem ao PDF
  
Adiciona uma imagem a um PDF na página e as coordenadas inseridas.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Inserir PDF|Arquivo PDF ao qual a imagem será adicionada|arquivo.pdf|
|arquivo JPG|Arquivo jpg que será adicionado ao pdf|path/imagem.jpg|
|Página|Número da página do pdf onde a imagem será adicionada|3|
|Coordenadas|Coordenadas da página pdf onde a imagem será colocada. Se forem colocadas coordenadas maiores que o tamanho da página, a imagem não poderá ser exibida.|150,340|
|PDF de saída|Número da página do pdf onde a imagem será adicionada|path/novo_arquivo.pdf|
|Resultado|Variável onde será armazenado True ou False dependendo se o módulo foi capaz de executar a ação|variável|

### Cortar imagem de PDF
  
Crie uma imagem a partir das coordenadas atribuídas.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Inserir PDF|Arquivo PDF que será usado no módulo|arquivo.pdf|
|imagem jpg|Caminho e nome que a imagem jpg extraída do pdf terá|path/imagen.jpg|
|Página|Número da página do pdf de onde a imagem será obtida|3|
|Coordenadas de início|Coordenadas de onde a imagem será obtida|0,0|
|Coordenadas finais|Coordenadas para onde a imagem será obtida|1000,1000|
