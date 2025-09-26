from flask import Flask, jsonify, request
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.utils.livro_dao import LivroDAO

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!!!!"

items = []

@app.route('/api/v1/scrapping/trigger', methods=['GET'])
def execute():
    from scripts.scrapping import Scrapping
    scrapper = Scrapping()
    try:
        qtde = scrapper.run()
        return jsonify({f"qtd livros importados": qtde}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    items.append(data)
    return jsonify(data), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    if 0 <= item_id < len(items):
        items[item_id] = data
        return jsonify(data)
    else:
        return jsonify({"error": "Item not found"}), 404

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if 0 <= item_id < len(items):
        removed_item = items.pop(item_id)
        return jsonify(removed_item)
    else:
        return jsonify({"error": "Item not found"}), 404
    
if __name__ == '__main__': 
    app.run(debug=True)
