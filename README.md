# Sistema de Gerenciamento de Biblioteca

# Daniel Rocha de Carvalho
# 251-002040
# Tema: Gerenciamento de Biblioteca
---

Projeto final de Estruturas de Dados (Tema 5). É um sistema de terminal em Python que controla leitores, reservas de livros, devoluções e a organização do acervo, usando Lista, Fila, Pilha e Árvore.

## Como executar

Precisa apenas do Python 3 instalado (nenhuma biblioteca externa).

```
python main.py
```

Em alguns sistemas o comando é `python3 main.py`.

O sistema começa vazio. Use as opções 5 e 6 do menu principal para salvar e carregar os dados. Os dados ficam no arquivo `dados_sistema.txt`, criado na mesma pasta do `main.py`.

## Menu

|Opção|O que faz|
|-|-|
|1|Leitores (cadastrar, listar, atualizar, remover)|
|2|Fila de reservas (reservar, listar, atender, corrigir título)|
|3|Pilha de devolvidos (registrar, ver topo, listar, corrigir topo, guardar na estante)|
|4|Acervo (inserir, listar, buscar, renomear, remover áreas)|
|5|Salvar dados|
|6|Carregar dados|
|0|Sair (pergunta se quer salvar)|

## Por que cada estrutura

**Lista (cadastro de leitores).** O cadastro precisa de acesso por chave (a matrícula), de listagem completa e de alterações e remoções em qualquer posição. Uma lista de dicionários resolve isso bem, e a ordem de cadastro é mantida. Fila e pilha não servem aqui, porque restringem o acesso a uma das pontas.

**Fila (reservas de exemplares).** Quem reservou primeiro deve ser atendido primeiro. Isso é FIFO: a reserva entra no fim e a próxima a ser atendida sai do início. Usei `collections.deque`, porque `popleft()` é feito em tempo constante, enquanto `pop(0)` em uma lista precisaria deslocar todos os elementos.

**Pilha (livros devolvidos no balcão).** Os livros devolvidos vão sendo empilhados no balcão, e o funcionário pega primeiro o que está em cima. Isso é LIFO: o último a chegar é o primeiro a ser triado. Usei uma lista comum com `append()` para empilhar e `pop()` para desempilhar, sempre no final, que é o topo.

**Árvore (áreas do conhecimento).** O acervo é hierárquico por natureza (área, subárea, tema), com níveis de profundidade diferentes. Implementei com dicionários aninhados, em que cada chave é uma área e o valor é outro dicionário com as subáreas. Assim, inserir, buscar e percorrer a hierarquia é natural, e não é preciso decidir a profundidade antes.

## Regras de negócio

* Só é possível reservar ou registrar devolução para leitor cadastrado.
* Um leitor com reserva na fila não pode ser removido.
* Um leitor não entra duas vezes na fila para o mesmo livro.
* Ao remover uma área da árvore que tem subáreas, o sistema pede confirmação.

## Formato do arquivo `dados\\\\\\\_sistema.txt`

Uma linha por registro, começando pelo identificador da estrutura e com campos separados por `|`:

```
LISTA|matricula|nome|curso
FILA|matricula|titulo
PILHA|titulo|matricula
ARVORE|area|subarea|tema
```

Detalhes da gravação:

* A fila é gravada do início para o fim, e a pilha da base para o topo. Assim, ao carregar, a ordem original é reconstruída.
* Na árvore, cada linha `ARVORE` guarda o caminho até uma folha. Os nós intermediários são recriados ao carregar.
* O caractere `|` digitado pelo usuário é trocado por `-` para não quebrar o formato.
* Linhas fora do padrão são ignoradas ao carregar, e o sistema avisa quantas foram.

