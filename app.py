from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://parallelum.com.br/fipe/api/v1/carros"

@app.route('/', methods=['GET', 'POST'])
def index():
    marcas = requests.get(f"{BASE_URL}/marcas").json()

    preco_veiculo = None
    erro = None
    veiculo = None
    modelos = []
    anos = []

    if request.method == 'POST':
        marca_id = request.form.get('marca')
        modelo_id = request.form.get('modelo')
        ano_id = request.form.get('ano')

        if marca_id and modelo_id and ano_id:
            preco_response = requests.get(f"{BASE_URL}/marcas/{marca_id}/modelos/{modelo_id}/anos/{ano_id}")

            if preco_response.status_code == 200:
                preco_dados = preco_response.json()
                preco_veiculo = preco_dados.get("Valor", "Preço não disponível")
                veiculo = preco_dados.get("Modelo", "Modelo não encontrado")
            else:
                erro = "Erro ao buscar preço do veículo."
        else:
            erro = "Por favor, selecione marca, modelo e ano."

    return render_template('index.html', marcas=marcas, preco_veiculo=preco_veiculo, veiculo=veiculo, erro=erro)

@app.route('/modelos/<marca_id>')
def get_modelos(marca_id):
    response = requests.get(f"{BASE_URL}/marcas/{marca_id}/modelos")

    if response.status_code == 200:
        return jsonify(response.json()['modelos'])
    else:
        return jsonify({"erro": "Erro ao carregar modelos"}), 500

@app.route('/anos/<marca_id>/<modelo_id>')
def get_anos(marca_id, modelo_id):
    response = requests.get(f"{BASE_URL}/marcas/{marca_id}/modelos/{modelo_id}/anos")

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"erro": "Erro ao carregar anos"}), 500

if __name__ == '__main__':
    app.run(debug=True)
