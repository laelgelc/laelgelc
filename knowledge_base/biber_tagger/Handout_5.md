Handout 5

Biber Tag Count

O programa Biber Tag Count é um processador de textos etiquetados pelo
Biber Tagger, criado por Douglas Biber. Esse programa não é
disponibilizado ao público. Ele possui as seguintes funções principais:

\(1\) identificar características linguísticas baseadas no texto
etiquetado. Para tanto, ele pode renomear ou combinar etiquetas para
chegar a uma característica linguística. Por exemplo, o TagCount tem uma
característica linguística chamada 'all adjectives', que não existe nas
etiquetas do Biber Tagger. Para chegar a ela, o TagCount soma os vários
tipos de adjetivo identificados separadamente pelo Biber Tagger:

![](media/image1.png){width="6.263888888888889in" height="1.4875in"}

\(2\) Contar a ocorrência das características linguísticas em cada
arquivo;

\(3\) Normalizar essas contagens por mil;

\(4\) Calcular os escores de fator de cada texto em cada uma das cinco
dimensões de variação de registro identificadas por Biber (1988).

\(5\) Criar um arquivo de output em que as frequências normalizadas por
mil das características linguísticas de cada texto são registradas.

A versão mostrada abaixo é ETSCountTags. Essa versão identifica **132
características**. O software roda apenas em Windows.

Ao iniciar o programa, aparece a tela abaixo:

![](media/image2.png){width="4.0in" height="2.06in"}

Em seguida, clique em 'Click here to begin (select input)'. Selecione a
pasta e os arquivos. Lembre-se que os arquivos devem ter sido
etiquetados pelo Biber Tagger. Se você não mudou a pasta de textos
etiquetados, ela deve se chamar taggedfiles e estará na mesma pasta dos
arquivos sem etiquetar.

![](media/image3.png){width="4.0in" height="2.44in"}

Em seguida, clique em OK. Na tela seguinte, clique em 'Click here to
continue' para escolher o nome do arquivo e a pasta onde será gravado o
arquivo de saída, com as contagens.

![](media/image4.png){width="4.0in" height="2.03in"}

Escolha a pasta e digite o nome do arquivo que terá as contagens. Por
exemplo, bricle_counts.txt

![](media/image5.png){width="4.0in" height="2.99in"}

Depois clique em Open para rodar o programa. Se der certo, quando
terminar, o programa avisa dizendo 'SUCESS!! FINISHED PROCESSING'.

![](media/image6.png){width="4.0in" height="2.05in"}

O programa cria dois arquivos: um com as contagens e outro com o corpus
etiquetado todo junto em apenas um arquivo (redundante, pois o corpus
etiquetado já existe). O arquivo principal é o que contem as contagens.
Ele tem o nome que você escolheu; nesse caso, bricle_counts.txt Este é
um arquivo txt que pode ser aberto em qualquer editor de texto.

Segue abaixo um trecho do arquivo de contagens bricle_counts.txt:

![](media/image7.png){width="6.263888888888889in"
height="3.402083333333333in"}

Esse arquivo é composto por registros e campos. Cada registro
corresponde a um texto do corpus. Cada registro é uma sequência de 12
linhas. Dentro de cada registro há uma série de campos. Na primeira
linha do registro, há quatro campos. Nas dez linhas seguintes, há 15
campos em cada linha. E na última linha, há dez campos. No total,
portanto há 164 campos. No entanto, 32 desses campos são sempre zero,
porque essa versão do TagCount não utiliza esses campos. Portanto, há
132 campos preenchidos.

Esse formato é empregado originalmente pelo programa SAS de análise
estatística. Esse formato não é uma planilha!

Vide o arquivo tagcounts_codes.doc para uma explicação dos campos dos
registros.
