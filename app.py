from flask import Flask, request, jsonify
from bot.bot_logic import process_with_bot

app = Flask(__name__)

@app.route('/hi', methods=['POST'])
def bye():
	return "bye"
	
@app.route('/bot', methods=['POST'])
def bot_endpoint():
    input_data = request.json
    user_input = input_data['message']
    response = process_with_bot(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
