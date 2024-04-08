# sprint-01-bak
 BackEnd Python para um MVP de Arvore Genealogica

##
O objetivo da Api é estruturar uma cadeia hierárquica para uma árvore genealógica,
através de endpoints GET, POST, PUT e DELETE.

O projeto foi desenvolvido em Python e banco de dados SQLLite fazendo uso do 
conhecimento adquirido no curso. Consiste em apenas uma tabela, que faz uso de 
um AUTO-REELACIONAMENTO, técnica comumente usada em modelagem 
de dados para estruturar informações hierárquicas ou de árvore,  
como em uma estrutura de árvore genealógica, organograma de uma empresa, 
ou categorias em uma hierarquia.

## Como executar 
Será necessário ter todas as libs python listadas no `requirementos.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirementos.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirementos.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```
para rodar o projeto:
http://127.0.0.1:5000
http://10.81.234.195:5000

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
