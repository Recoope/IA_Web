from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
from sqlalchemy import create_engine
import psycopg

app = Flask(__name__)

# Carregar o modelo previamente treinado
modelo = joblib.load('pipeline.pkl')

# Carregar o DataFrame uma vez para reutilizá-lo nas rotas
df = pd.read_excel('C:/Users/henriquelucareli-ieg/Desktop/Recoope/Tudo/Analise Exploratoria/base_empresas_reciclagem_IA.xlsx')

@app.route('/')
def home():
    estado = df['Estado'].unique()
    municipio = df['Município'].unique()
    tipo = df['Tipo de Resíduo'].unique()
    metodo_reciclagem = df['Método de Reciclagem'].unique()

    return render_template('index.html', estado=estado.tolist(), municipio=municipio.tolist(), tipo=tipo.tolist(), metodo_reciclagem=metodo_reciclagem.tolist())

# Nova rota para obter os municípios com base no estado selecionado
@app.route('/get_municipios', methods=['POST'])
def get_municipios():
    estado_selecionado = request.json.get('estado')

    # Filtrar os municípios com base no estado selecionado
    municipios = df[df['Estado'] == estado_selecionado]['Município'].unique().tolist()

    return jsonify(municipios)

@app.route('/predict', methods=['POST'])
def predict():
    estado = request.form.get('estado')
    municipio = request.form.get('municipio')
    ano = request.form.get('ano')
    tipo_residuo = request.form.get('tipo_residuo')
    metodo_reciclagem = request.form.get('metodo_reciclagem')
    quantidade = request.form.get('quantidade')
    unidade_media = 'kilogramas'

    # Preparar os dados para predição
    dados_entrada = [[
        estado, municipio, ano, tipo_residuo,
        metodo_reciclagem, quantidade, unidade_media
    ]]

    colunas = ['Estado', 'Município', 'Ano', 'Tipo de Resíduo', 'Método de Reciclagem', 'Quantidade', 'Unidade de Medida']
    dados_entrada_df = pd.DataFrame(dados_entrada, columns=colunas)

    # Fazer a predição
    resultado = modelo.predict(dados_entrada_df)

    dados_entrada_df['Resultado'] = resultado

    print('Começando===============================================')

    # Conectar ao banco de dados e salvar o DataFrame
    try:
        conn = psycopg.connect("postgres://avnadmin:AVNS_DAFAJWqxMl1ba9hBbcZ@recoop-germinare-9764.h.aivencloud.com:16983/IA?sslmode=require")
        print("Conexão estabelecida com sucesso!")

        # Configurar a conexão com o banco de dados usando SQLAlchemy
        engine = create_engine("postgresql+psycopg://avnadmin:AVNS_DAFAJWqxMl1ba9hBbcZ@recoop-germinare-9764.h.aivencloud.com:16983/IA?sslmode=require")

        # Salvar o DataFrame no banco de dados
        dados_entrada_df.to_sql('Respostas', con=engine, if_exists='append', index=False)
        print("DataFrame salvo com sucesso!")

    except psycopg.OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    except Exception as e:
        print(f"Erro ao salvar o DataFrame: {e}")
    finally:
        conn.close()

    return jsonify({'resultado': resultado[0]})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')