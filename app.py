from flask import Flask, request, jsonify, render_template, send_file
import numpy as np
import io
import base64
from PIL import Image
from models.game_logic import LunarLander
from models.ai import LunarLanderAI

app = Flask(__name__)

lunar_lander = LunarLander()
lunar_lander_ai = LunarLanderAI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game', methods=['GET'])
def new_game():
    lunar_lander.reset()
    img = lunar_lander.generate_image()
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    return jsonify({'image': img_base64})

@app.route('/step', methods=['POST'])
def step():
    try:
        action = request.get_json()['action']
        state = lunar_lander.get_state()
        next_state, reward, done = lunar_lander.step(action)
        
        lunar_lander_ai.remember(state, action, reward, next_state, done)
        lunar_lander_ai.train(batch_size=32)

        img = lunar_lander.generate_image()
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        return jsonify({
            'image': img_base64,
            'reward': reward,
            'done': done
        })
    except Exception as e:
        print(f"Error in /step: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/ai_step', methods=['POST'])
def ai_step():
    try:
        state = np.expand_dims(lunar_lander.get_state(), axis=0)
        action = np.argmax(lunar_lander_ai.predict(state)[0])  # AI decides the action
        next_state, reward, done = lunar_lander.step(action)
        lunar_lander_ai.remember(state, action, reward, next_state, done)
        lunar_lander_ai.train(batch_size=32)

        img = lunar_lander.generate_image()
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        return jsonify({
            'image': img_base64,
            'reward': reward,
            'done': done
        })
    except Exception as e:
        print(f"Error in /ai_step: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
