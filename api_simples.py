from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama
import os

app = Flask(__name__)
CORS(app)  # Permite que sites externos acessem a API

print("🤖 Iniciando API do Agente Universal...")

@app.route('/')
def home():
    return """
    <h1>🤖 API do Agente Universal</h1>
    <p>API funcionando perfeitamente!</p>
    <p><strong>Endpoints disponíveis:</strong></p>
    <ul>
        <li><code>GET /health</code> - Verificar status</li>
        <li><code>POST /chat</code> - Conversar com a IA</li>
        <li><code>POST /pesquisar</code> - Pesquisar um assunto</li>
    </ul>
    """

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "online",
        "mensagem": "API funcionando perfeitamente!",
        "versao": "1.0"
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Pega a mensagem do usuário
        dados = request.json
        mensagem = dados.get('mensagem', 'Olá')
        
        print(f"💬 Recebida mensagem: {mensagem}")
        
        # Usa o Ollama para gerar resposta
        resposta = ollama.generate(model='gemma3n:e2b', prompt=mensagem)
        
        return jsonify({
            "sucesso": True,
            "resposta": resposta['response'],
            "modelo": "gemma3n:e2b"
        })
        
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "erro": str(e)
        }), 500

@app.route('/pesquisar', methods=['POST'])
def pesquisar():
    try:
        dados = request.json
        assunto = dados.get('assunto', 'tecnologia')
        
        prompt = f"""
        Pesquise e explique sobre: {assunto}
        
        Forneça:
        - Explicação clara e simples
        - 3 pontos principais
        - 2 curiosidades interessantes
        - 1 aplicação prática
        
        Seja direto e informativo.
        """
        
        resposta = ollama.generate(model='llama3', prompt=prompt)
        
        return jsonify({
            "sucesso": True,
            "assunto": assunto,
            "resultado": resposta['response']
        })
        
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "erro": str(e)
        }), 500

if __name__ == '__main__':
    print("🌐 API rodando em: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)