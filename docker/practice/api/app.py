from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Hello from Docker Compose!',
        'service': 'Python Flask API',
        'status': 'running'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/info')
def info():
    return jsonify({
        'name': 'Docker Compose 实践',
        'version': '1.0.0',
        'services': ['nginx', 'flask']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
