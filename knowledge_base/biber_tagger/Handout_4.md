Handout 4

Biber tagger

O Biber Tagger é o etiquetador 'de facto' para Análise Multdimensional.
Ele funciona apenas com textos em inglês. Anota características
gramaticais e lexicais, mas não faz lematização. Foi criado em meados
dos anos 1980 por Douglas Biber. A versão mostrada abaixo é de meados
dos anos 2000. O etiquetador roda em Windows apenas. Seu acesso é muito
restrito. Ele não é disponibilizado pelo autor.

1.  Abra o programa

![](media/image1.png){width="4.0in" height="3.14in"}

2\. Selecione as opções desejadas. O default aparece selecionado abaixo.

![](media/image2.png){width="4.0in" height="3.18in"}

3\. Clique em Begin Tagging para escolher os textos para etiquetar. Os
textos devem estar no formato ASCII (txt). Word, PDF, html, etc. não
funcionam. Os arquivos txt não devem ter linhas muito compridas, nem
caracteres estranhos (i.e. que não sejam os caracteres constantes no
teclado norte-americano).

4\. Depois de escolher os textos, clique em OK para começar a
etiquetagem

![](media/image3.png){width="4.0in" height="3.19in"}

5\. O programa cria uma pasta chamada taggedfiles dentro da pasta onde
estão os textos para etiquetar. Nessa pasta são colocados os arquivos
etiquetados.

6\. Quando o programa terminar a etiquetagem, aparece uma mensagem
dizendo 'Finished Tagging'

![](media/image4.png){width="4.0in" height="3.16in"}

Abaixo segue exemplo de um texto etiquetado pelo Biber Tagger. Vide o
arquivo biber_tagger_codes.pdf para o *tagset* (relação das etiquetas)
do etiquetador. O arquivo etiquetado é apresentado itemizado
(*tokenized*), isto é, cada palavra em uma linha, como na maioria dos
etiquetadores.

Formato da etiqueta:

palavra \^xxx++++=palavra,

Onde:

  -----------------------------------------------------------------------
             Texto itemizado. A pontuação é deslocada para uma linha
             abaixo.
  ---------- ------------------------------------------------------------
             Espaço em branco que separa a palavra etiquetada da etiqueta

  \^         Início da etiqueta

  xxx        Etiqueta principal

  \+         Separador dos campos das etiquetas. Cada campo pode ter
             etiquetas secundárias (até 4)

  =          Fim da etiqueta

  palavra,   Sequência de caracteres conforme existe no texto fonto
  -----------------------------------------------------------------------

Texto original

ICLE-BR-FF-0062.1\>

**Some people defend that there is no longer place for dreaming** and

imagination in our modern world dominated by **science,** technology and

industrialization. The first step in order to agree or disagree with

this affirmative is to ask who are these people that defend this point
of

(\...)

+---------------------------+---------------+----------------+----------------+
| Texto etiquetado          | Etiqueta      | Significado da | Comentário     |
|                           |               | etiqueta       |                |
+===========================+===============+================+================+
| \<ICLE-BR-FF-0062.1\>     | Sem etiqueta  |                |                |
+---------------------------+---------------+----------------+----------------+
| Some \^dti++++=Some       | dti++++       | singular or    |                |
|                           |               | plural         |                |
|                           |               | determiner     |                |
|                           |               | (any, enough,  |                |
|                           |               | some)          |                |
+---------------------------+---------------+----------------+----------------+
| people \^nns++++=people   | nns++++       | plural noun +  |                |
|                           |               | nominalization |                |
+---------------------------+---------------+----------------+----------------+
| defend \^vb++++=defend    | vb++++        | base form of   |                |
|                           |               | verb,          |                |
|                           |               | excluding      |                |
|                           |               | verbs in       |                |
|                           |               | infinitive     |                |
|                           |               | clauses        |                |
|                           |               |                |                |
|                           |               | (uninflected   |                |
|                           |               | present tense, |                |
|                           |               | imperative)    |                |
+---------------------------+---------------+----------------+----------------+
| that \^dt+dem+++=that     | dt+dem++      | determiner +   | Erro! 'that' é |
|                           |               | demonstrative  | conjunção      |
|                           |               |                | subordinada.   |
|                           |               |                | Deveria ser    |
|                           |               |                | tht+vcmp+++    |
|                           |               |                |                |
|                           |               |                | that as        |
|                           |               |                | dependent      |
|                           |               |                | clause head +  |
|                           |               |                | verb           |
|                           |               |                | complement     |
+---------------------------+---------------+----------------+----------------+
| there \^ex+pex+++=there   | ex+pex+++     | existential    |                |
|                           |               | there          |                |
+---------------------------+---------------+----------------+----------------+
| is \^vbz+bez+vrb++=is     | vbz+bez+vrb++ | 3rd person     |                |
|                           |               | singular       |                |
|                           |               | verb + is +    |                |
|                           |               | auxiliary verb |                |
+---------------------------+---------------+----------------+----------------+
| no \^at++++=no            | at++++        | singular       |                |
|                           |               | indefinite     |                |
|                           |               | article        |                |
+---------------------------+---------------+----------------+----------------+
| longer \^rbr++++=longer   | rbr++++       | comparative    |                |
|                           |               | adverb         |                |
+---------------------------+---------------+----------------+----------------+
| place \^nn++++=place      | nn++++        | singular       |                |
|                           |               | common noun    |                |
+---------------------------+---------------+----------------+----------------+
| for \^in++++=for          | in++++        | preposition    |                |
+---------------------------+---------------+----------------+----------------+
| dreaming                  | xvbg+++xvbg+  | -ing form      | Não está no    |
| \^xvbg+++xvbg+=dreaming   |               |                | tagset         |
+---------------------------+---------------+----------------+----------------+
| \...                      |               |                |                |
+---------------------------+---------------+----------------+----------------+
| science                   | nn+nom+++     | singular noun, | Nominalização? |
| \^nn+nom+++=science,      |               | nominalization |                |
+---------------------------+---------------+----------------+----------------+
| , \^zz++++=EXTRAWORD      | zz++++        | letter of the  | Pontuação      |
|                           |               | alphabet       |                |
+---------------------------+---------------+----------------+----------------+

EXTRAWORD aparece como indicativo de um token itemizado que já aparece
na linha anterior.

Índice de acerto

Se considerarmos o erro de 'that' 1 erro em 12 tokens 92% de acerto

Se considerarmos também o erro de science 2 erros em 12 tokens 83% de
acerto
