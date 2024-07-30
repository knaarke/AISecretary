from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tasks = []

@app.route('/')
def home():
    return "Welcome to AISecretary!"

@app.route('/api/tasks', methods=['GET', 'POST'])
def manage_tasks():
    if request.method == 'POST':
        new_task = request.json
        tasks.append(new_task)
        return jsonify(new_task), 201
    else:
        return jsonify(tasks)

@app.route('/api/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    if request.method == 'GET':
        return jsonify(task)
    elif request.method == 'PUT':
        updated_task = request.json
        task.update(updated_task)
        return jsonify(task)
    elif request.method == 'DELETE':
        tasks.remove(task)
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)
