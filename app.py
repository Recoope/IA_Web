from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Carregar o modelo previamente treinado
modelo = joblib.load('pipeline.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Capturar os dados do formulário
    razao_social = request.form.get('razao_social').upper()
    estado = request.form.get('estado').upper()
    municipio = request.form.get('municipio').upper()
    ano = request.form.get('ano').upper()
    tipo_residuo = request.form.get('tipo_residuo')
    metodo_reciclagem = request.form.get('metodo_reciclagem')
    quantidade = request.form.get('quantidade')
    unidade_medida = 'kilogramas' # request.form.get('unidade_medida')
    empresa_destinadora = request.form.get('empresa_destinadora').upper()

    # Preparar os dados para predição
    dados_entrada = [[
        razao_social, estado, municipio, ano, tipo_residuo,
        metodo_reciclagem, quantidade, unidade_medida, empresa_destinadora
    ]]

    colunas = [
        'Razão Social', 'Estado', 'Município', 'Ano', 'Tipo de Resíduo',
        'Método de Reciclagem', 'Quantidade', 'Unidade de Medida', 'Empresa Destinadora do Resíduo'
    ]
    dados_entrada_df = pd.DataFrame(dados_entrada, columns=colunas)

    # Fazer a predição
    resultado = modelo.predict(dados_entrada_df)

    print("Resultado da predição:", resultado)

    # Adicionar a situação cadastral ao DataFrame
    dados_entrada_df['Situação Cadastral'] = resultado

    # Retornar o resultado da predição
    return jsonify({'resultado': resultado[0]})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')