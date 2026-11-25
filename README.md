# Simone - Simulation One

Esse é o meu projeto pessoal para utilizar Large Language Models (LLMs) no dia a dia, e o meu primeiro projeto de uso real de inteligência Artificial é a `Simone`, uma ferramenta local para auxiliar na revisão e análise de textos.

## Por que Simone?

Simone é um filme de 2002 estrelado pelo glorioso Al Pacino, no qual um cineasta cria uma artista virtual e, com ela, alcança grande sucesso, utilizando diversos artifícios para convencer o público de que ela é uma pessoa real.

O nome da artista? SIMONE, que é um acrônimo de `SIMulation ONE`, o nome original no cartaz é `S1MONE`.

E como está sendo o meu primeiro projeto de uso real de Inteligência Artificial, mesmo de uma forma simples, resolvi colocar o nome de Simone, em homenagem.

## Objetivo

O projeto utiliza modelos de linguagem executados localmente para auxiliar na revisão de textos, buscando corrigir problemas gramaticais e melhorar a escrita sem depender de serviços externos de Inteligências Artificial.

## Requisitos

Antes de instalar a Simone, é necessário ter:

* Python compatível com a versão exigida pelo projeto.
* Poetry para gerenciamento de dependências.
* Ollama para executar os modelos de linguagem localmente.

## Como instalar

1. Instale o Ollama.

Instale o Ollama seguindo as instruções disponíveis no site oficial: [https://ollama.com](https://ollama.com)

1. Baixe o modelo

A Simone utiliza, por padrão, o modelo llama3.2:3b

Para baixá-lo, execute:

```bash
ollama pull llama3.2:3b
```

Certifique-se de que o Ollama esteja funcionando antes de utilizar a Simone.

3. Clone o repositório

Clone o repositório e entre na pasta do projeto:

```bash
git clone <URL_DO_PROJETO>
cd projeto-simone
```

4. Instale as dependências

```bash
poetry install
```

## Executando a Simone

Após a instalação, a Simone pode ser executada pelo Poetry:

```bash
poetry run simone
```

## Configuração

A Simone utiliza as seguintes configurações padrão:

| Configuração      | Valor padrão          |
|:------------------|:----------------------|
| Servidor Ollama   | http://127.0.0.1:1134 |
| Modelo            | llama3.2:3b           |
| Temperatura       | 0.1                   |
| Limite de geração | 1024 tokens           |

## Desenvolvimento

Para contribuir com o desenvolvimento do projeto ou realizar alterações no código, instale as dependências de desenvolvimento utilizando o Poetry.

Os testes podem ser executados com:

```bash
poetry run pytest
```

