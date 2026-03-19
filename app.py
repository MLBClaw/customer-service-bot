"""
Flask Web 服务 - 客服机器人 API
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from bot import CustomerServiceBot
import uuid
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# 初始化机器人
bot = CustomerServiceBot()

@app.route('/')
def index():
    """首页 - 聊天界面"""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """聊天接口"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not message:
            return jsonify({
                'success': False,
                'error': '消息不能为空'
            }), 400
        
        # 获取机器人回复
        result = bot.reply(message, session_id)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': result['message'],
            'intent': result['intent'],
            'confidence': result['confidence'],
            'suggestions': result['suggestions'],
            'action': result.get('action')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sessions/<session_id>', methods=['GET'])
def get_session_history(session_id):
    """获取会话历史"""
    try:
        session = bot.get_session(session_id)
        return jsonify({
            'success': True,
            'session_id': session_id,
            'history': session['history'],
            'created_at': session['created_at'],
            'last_active': session['last_active']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def clear_session(session_id):
    """清空会话"""
    try:
        bot.clear_session(session_id)
        return jsonify({
            'success': True,
            'message': '会话已清空'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    return jsonify({
        'success': True,
        'stats': bot.get_stats()
    })

@app.route('/api/knowledge', methods=['GET'])
def get_knowledge_base():
    """获取知识库（简化版）"""
    kb = {}
    for intent, data in bot.knowledge_base.items():
        if intent != 'fallback':
            kb[intent] = {
                'keywords': data.get('keywords', []),
                'sample_response': data['responses'][0] if data.get('responses') else ''
            }
    return jsonify({
        'success': True,
        'intents': list(kb.keys()),
        'knowledge_base': kb
    })

# 健康检查
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'service': 'customer-service-bot',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
