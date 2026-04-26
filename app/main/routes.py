from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return jsonify({'mensagem': 'Bem-vindo ao E-commerce Flask!'})

@main_bp.route('/health')
def health_check():
    return jsonify({'status': 'ok', 'servidor': 'rodando'})