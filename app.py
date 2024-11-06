from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
from sqlalchemy import create_engine
import psycopg

app = Flask(__name__)
global_id = 1

# Carregar o modelo previamente treinado
modelo = joblib.load('pipeline.pkl')

# Carregar o DataFrame uma vez para reutilizá-lo nas rotas
df = pd.read_excel('base_empresas_reciclagem_IA.xlsx')

# Função para obter o próximo ID
def obter_proximo_id():
    # Conexão com o banco de dados
    conn = psycopg.connect("postgres://avnadmin:AVNS_DAFAJWqxMl1ba9hBbcZ@recoop-germinare-9764.h.aivencloud.com:16983/IA?sslmode=require")
    cursor = conn.cursor()
    
    # Obter o último ID e adicionar 1
    cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM \"Respostas\"")
    proximo_id = cursor.fetchone()[0]
    
    # Fechar a conexão
    conn.close()
    return proximo_id

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
    id= obter_proximo_id()
    estado = request.form.get('estado')
    municipio = request.form.get('municipio')
    ano = request.form.get('ano')
    tipo_residuo = request.form.get('tipo_residuo')
    metodo_reciclagem = request.form.get('metodo_reciclagem')
    quantidade = request.form.get('quantidade')
    unidade_media = 'kilogramas'

    # Preparar os dados para predição
    dados_entrada = [[
        id, estado, municipio, ano, tipo_residuo,
        metodo_reciclagem, quantidade, unidade_media
    ]]

    colunas = ['id','Estado', 'Município', 'Ano', 'Tipo de Resíduo', 'Método de Reciclagem', 'Quantidade', 'Unidade de Medida']
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

@app.route('/update_resposta', methods=['POST'])
def update_resposta():
    try:

        # Lógica para atualização do status
        conn = psycopg.connect("postgres://avnadmin:AVNS_DAFAJWqxMl1ba9hBbcZ@recoop-germinare-9764.h.aivencloud.com:16983/IA?sslmode=require")
        cursor = conn.cursor()
        
        cursor.execute("SELECT MAX(id) FROM \"Respostas\"")
        max_id = cursor.fetchone()[0]

        if max_id:
            cursor.execute("""
                UPDATE \"Respostas\"
                SET \"Resultado\" = CASE 
                    WHEN \"Resultado\" = 'Ativa' THEN 'Encerrado' 
                    WHEN \"Resultado\" = 'Encerrado' THEN 'Ativa' 
                    ELSE \"Resultado\" 
                END
                WHERE id = %s
            """, (max_id,))
            
            conn.commit()
            return jsonify({'mensagem': 'Resposta confirmada com sucesso!'})

        else:
            return jsonify({'mensagem': 'Nenhum registro encontrado para atualização.'})

    except Exception as e:
        print(e)
        return jsonify({'mensagem': f'Erro ao confirmar resposta: {e}'})
    
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')