# Projeto de Otimização e Inteligência Artificial

Projeto de iniciação científica da UFES sobre otimização e Inteligência Artificial.

## 1. Versões Utilizadas
- **Linguagem:** Python 3.14
- **Docker:** Imagem base `python:3.14-slim`

## 2. Dependências
As bibliotecas externas e pacotes matemáticos necessários para este projeto estão listados no arquivo `requirements.txt`. As principais ferramentas utilizadas são:
- `numpy` (Para cálculos matemáticos e matrizes)
- `pandas` (Para manipulação de dados e planilhas)
- `scipy` (Para os algoritmos de otimização)
- `matplotlib` (Para geração de gráficos)

## 3. Instalação do Ambiente

Para preparar o projeto no seu computador, escolha uma das opções abaixo:

**Opção A: Usando Ambiente Virtual (Local)**
1. Crie o ambiente virtual: `python -m venv .venv`
2. Ative o ambiente: `.venv\Scripts\Activate.ps1` (no Windows)
3. Instale as bibliotecas: `pip install -r requirements.txt`

**Opção B: Usando Docker**
1. Construa a imagem isolada: `docker build -t projeto-ia .`

## 4. Execução do Projeto

Após a instalação, para rodar o código principal, utilize os comandos:

**Se estiver usando a execução local:**
```bash
python src/main.py

docker run --rm projeto-ia
