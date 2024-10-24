
# Predição de Atividade Empresarial com Flask e Machine Learning

Este projeto utiliza Flask para construir uma aplicação web que faz predições sobre a situação cadastral de empresas com base em informações fornecidas por um formulário. O modelo de machine learning usado para as predições foi treinado anteriormente e está salvo em um arquivo `pipeline.pkl`.

A aplicação processa as informações fornecidas pelo usuário, faz a predição e retorna o resultado em uma interface simples.

## 📋 Tecnologias Utilizadas

- **Flask**: Framework web minimalista para Python.
- **Pandas**: Biblioteca poderosa para manipulação de dados.
- **Joblib**: Utilizada para carregar o modelo de machine learning treinado.
- **HTML/CSS/JavaScript**: Para a interface web e interação com o usuário.

## ⚙️ Funcionalidades

1. **Página Inicial**: Interface web simples que coleta dados da empresa para a predição.
2. **Predição**: Os dados fornecidos pelo usuário são enviados para o backend, processados, e o resultado é retornado com a predição sobre a situação cadastral da empresa.
3. **Modelo de Machine Learning**: Um modelo de machine learning treinado previamente, salvo no arquivo `pipeline.pkl`, é utilizado para fazer a predição.

## 🗂️ Estrutura do Projeto

```
.
├── app.py                 # Código principal do Flask
├── templates/
│   └── index.html         # Arquivo HTML com o formulário
├── pipeline.pkl           # Modelo de machine learning treinado
└── requirements.txt       # Dependências do projeto
```
- Os outros arquivos servem para colocar na AWS.

### Explicação dos Arquivos

- **app.py**: O arquivo principal que contém o backend da aplicação, responsável por processar as entradas e fazer a predição usando o modelo.
- **index.html**: O front-end da aplicação, onde o usuário insere os dados da empresa.
- **pipeline.pkl**: Arquivo que contém o modelo de machine learning previamente treinado.
- **requirements.txt**: Arquivo com as dependências necessárias para executar o projeto.

## 🚀 Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seuusuario/predicao-empresa.git
   cd predicao-empresa
   ```

2. **Crie um ambiente virtual e ative-o**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   .\venv\Scripts\activate    # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Certifique-se de ter o modelo de machine learning `pipeline.pkl` no diretório raiz do projeto.**

## 💻 Executando o Projeto

1. Para iniciar a aplicação Flask, execute o seguinte comando:
   ```bash
   python app.py
   ```

2. Acesse o aplicativo em seu navegador:
   ```
   http://localhost:5000
   ```

## 🎯 Como Usar

1. Abra o navegador e vá para `http://localhost:5000`.
2. Preencha o formulário com as seguintes informações:
   - **Razão Social**: Nome da empresa.
   - **Estado**: Estado da empresa.
   - **Município**: Município da empresa.
   - **Ano**: Ano da atividade.
   - **Tipo de Resíduo**: Tipo de resíduo gerado pela empresa.
   - **Método de Reciclagem**: Método de reciclagem utilizado.
   - **Quantidade**: Quantidade de resíduo gerado.
   - **Empresa Destinadora**: Empresa responsável por tratar o resíduo.

3. Após preencher os campos, clique em "Fazer Previsão".
4. A predição será feita e o resultado aparecerá na página.

## 🔧 Explicação do Código

### Rota `/`

- Esta rota carrega o template HTML `index.html`, que contém o formulário onde o usuário pode inserir os dados da empresa.

### Rota `/predict`

- Esta rota recebe os dados enviados via POST do formulário, prepara os dados em um DataFrame, e usa o modelo carregado para fazer a predição.
- O resultado da predição é então enviado de volta ao front-end via JSON.

### Modelo `pipeline.pkl`

- O modelo de machine learning foi previamente treinado e salvo no arquivo `pipeline.pkl` usando a biblioteca `joblib`. Ele é carregado no início da aplicação Flask e utilizado para fazer predições baseadas nos dados do formulário.

## 📊 Exemplo de Predição

Se o usuário preencher o formulário com os seguintes dados:
- Razão Social: "EMPRESA XYZ"
- Estado: "SP"
- Município: "São Paulo"
- Ano: "2024"
- Tipo de Resíduo: "Plástico"
- Método de Reciclagem: "Reprocessamento"
- Quantidade: "1500"
- Empresa Destinadora: "RECICLA S.A."

O modelo pode retornar a predição da situação cadastral da empresa, que será exibida como resultado na interface.

## 📦 Dependências

As dependências necessárias para rodar o projeto estão no arquivo `requirements.txt`. Você pode instalá-las com o comando:

```bash
pip install -r requirements.txt
```# IA_Web
