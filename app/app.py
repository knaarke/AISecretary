import json
import requests
from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_db_connection():
    try:
        conn = sqlite3.connect('tasks.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def analyze_task(task):
    payload = {
        "model": "llama3.1:latest",
        "prompt": f"""You are an AI assistant that helps prioritize tasks and estimate the time required to complete them.
        
        Task: {task}
        
        Please respond in the following format:
        Priority: <high/medium/low>
        Estimated time: <time in hours/minutes>
        """
    }
    try:
        response = requests.post('http://localhost:11434/api/generate', json=payload, stream=True)
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to LLM server: {e}")
        return ""

    analysis = ""
    for line in response.iter_lines():
        if line:
            try:
                json_line = json.loads(line.decode('utf-8'))
                analysis += json_line.get("response", "")
            except json.JSONDecodeError as e:
                print(f"JSON decode error in analyze_task: {e}")

    print(f"Full analysis: {analysis}")
    return analysis

def parse_analysis_response(response):
    priority = "Unknown"
    estimated_time = "Unknown"
    
    if "Priority:" in response and "Estimated time:" in response:
        parts = response.split("\n")
        for part in parts:
            if part.startswith("Priority:"):
                priority = part.split("Priority:")[1].strip()
            elif part.startswith("Estimated time:"):
                estimated_time = part.split("Estimated time:")[1].strip()
    
    return priority, estimated_time

@app.route('/')
def home():
    return "Welcome to AISecretary!"

@app.route('/api/tasks', methods=['GET', 'POST'])
def manage_tasks():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    if request.method == 'POST':
        new_task = request.json
        analysis = analyze_task(new_task['name'])
        priority, estimated_time = parse_analysis_response(analysis)
        task = (new_task['name'], new_task.get('category', ''), new_task.get('details', ''), f"Priority: {priority}, Estimated time: {estimated_time}")
        try:
            conn.execute('INSERT INTO tasks (name, category, details, analysis) VALUES (?, ?, ?, ?)', task)
            conn.commit()
        except sqlite3.Error as e:
            conn.close()
            return jsonify({'error': f'Database error: {e}'}), 500
        conn.close()
        return jsonify(new_task), 201
    else:
        tasks = conn.execute('SELECT * FROM tasks').fetchall()
        conn.close()
        return jsonify([dict(row) for row in tasks])

@app.route('/api/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_task(task_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if task is None:
        conn.close()
        return jsonify({'error': 'Task not found'}), 404

    if request.method == 'GET':
        conn.close()
        return jsonify(dict(task))
    elif request.method == 'PUT':
        updated_task = request.json
        try:
            conn.execute('UPDATE tasks SET name = ?, category = ?, details = ? WHERE id = ?',
                         (updated_task.get('name', task['name']),
                          updated_task.get('category', task['category']),
                          updated_task.get('details', task['details']),
                          task_id))
            conn.commit()
        except sqlite3.Error as e:
            conn.close()
            return jsonify({'error': f'Database error: {e}'}), 500
        conn.close()
        return jsonify(updated_task)
    elif request.method == 'DELETE':
        try:
            conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
        except sqlite3.Error as e:
            conn.close()
            return jsonify({'error': f'Database error: {e}'}), 500
        conn.close()
        return '', 204

@app.route('/api/tasks/analyze', methods=['POST'])
def analyze_task_route():
    task = request.json.get('name', '')
    analysis_result = analyze_task(task)
    priority, estimated_time = parse_analysis_response(analysis_result)
    return jsonify({'priority': priority, 'estimated_time': estimated_time})

if __name__ == '__main__':
    conn = get_db_connection()
    if conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            category TEXT,
                            details TEXT,
                            analysis TEXT
                        )''')
        conn.close()
    app.run(debug=True)
