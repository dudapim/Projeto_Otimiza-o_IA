# Usa a imagem oficial do Python (usaremos a base 3.14 para bater com o seu)
FROM python:3.14-slim

# Cria e define a pasta de trabalho dentro do "computador virtual" do Docker
WORKDIR /app

# Copia o nosso arquivo de bibliotecas para dentro do Docker
COPY requirements.txt .

# Pede para o Docker instalar as bibliotecas exatas que você salvou
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do seu projeto (pasta src, etc.) para dentro do Docker
COPY . .

# Diz qual comando o Docker deve rodar quando for iniciado
CMD ["python", "src/main.py"]