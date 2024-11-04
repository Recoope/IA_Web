# 📊 Projeto Flask de Previsão de Reciclagem com Machine Learning

Este projeto é uma aplicação web construída com Flask que utiliza um modelo de machine learning para realizar previsões relacionadas à reciclagem. Ele permite aos usuários prever a quantidade de resíduos recicláveis com base em parâmetros como estado, município, tipo de resíduo e método de reciclagem, e salva o resultado em um banco de dados PostgreSQL.

---

## 🚀 Funcionalidades

- **Carregamento de dados**: Importa informações de um arquivo Excel para exibir dados de estado, município, tipo de resíduo e método de reciclagem na interface.
- **Predições com Machine Learning**: Usa um modelo pré-treinado (carregado com `joblib`) para realizar previsões de quantidade reciclável.
- **Filtros inteligentes**: Filtra e exibe municípios com base no estado selecionado.
- **Armazenamento de previsões**: Salva os resultados das previsões em um banco de dados PostgreSQL.

---

## 📂 Estrutura do Projeto

- **`app.py`**: Arquivo principal da aplicação Flask.
- **`pipeline.pkl`**: Arquivo com o modelo de machine learning previamente treinado.
- **`base_empresas_reciclagem_IA.xlsx`**: Base de dados com informações iniciais para preenchimento das opções na interface.
- **`templates/index.html`**: Template HTML principal para o frontend da aplicação.

---

## 📋 Pré-requisitos

Certifique-se de instalar os seguintes pacotes antes de executar a aplicação:

- Python 3.7+
- Flask
- Pandas
- Joblib
- SQLAlchemy
- Psycopg2-binary
- Outros pacotes listados no arquivo `requirements.txt`

---

## 🔧 Configuração

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt

3. Configure os arquivos necessários:

Coloque o arquivo do modelo pipeline.pkl e o arquivo Excel base_empresas_reciclagem_IA.xlsx na pasta do projeto.
Configure o banco de dados PostgreSQL:

No código, substitua as informações de conexão do banco pelo suas credenciais do seu banco de dados, se necessário.

4. ▶️ Como Executar   
- No terminal, inicie a aplicação com o seguinte comando:

   ```bash
   python app.py
Acesse a aplicação no navegador em: http://localhost:5000

5.🌐 Endpoints da API
/: Página inicial com filtros e formulário de entrada para previsão.
/get_municipios (POST): Retorna os municípios filtrados pelo estado selecionado.

/predict (POST): Recebe os parâmetros do formulário, realiza a previsão com o modelo de machine learning, salva o resultado no banco de dados e retorna o resultado.

6.🧑‍🏫 Exemplo de Uso
Selecione o estado, município, ano, tipo de resíduo e método de reciclagem na página inicial.
Insira a quantidade do resíduo a ser reciclado.
Clique em "Prever" para ver o resultado e salvar os dados no banco de dados.

7.🗄️ Estrutura do Banco de Dados
O banco de dados PostgreSQL armazena as previsões feitas pelo modelo na tabela Respostas com as seguintes colunas:

-Estado: Estado selecionado pelo usuário.

- Município: Município selecionado pelo usuário.

- Ano: Ano especificado na previsão.

- Tipo de Resíduo: Tipo de resíduo selecionado.

- Método de Reciclagem: Método de reciclagem escolhido.

- Quantidade: Quantidade especificada para o resíduo.

- Unidade de Medida: Unidade padrão (kilogramas).

- Resultado: Resultado da previsão.

⚙️ Observações
A conexão com o banco de dados é gerenciada pela biblioteca psycopg2, e o SQLAlchemy é utilizado para integração com o PostgreSQL.

O modelo de machine learning é carregado uma única vez no início da aplicação, otimizando o desempenho.

Para melhorar a segurança, recomenda-se armazenar as credenciais do banco de dados em variáveis de ambiente.