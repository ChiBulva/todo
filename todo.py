from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to the Todo List Application</h1>"

@app.route('/todo')
def todo_lists():
    todo_lists = os.listdir('./static/json/tdl')
    todo_lists = [os.path.splitext(file)[0] for file in todo_lists if file.endswith('.json')]
    return render_template('todo_lists.html', todo_lists=todo_lists)

@app.route('/todo/<string:todo_list>')
def todo(todo_list):
    with open(f'./static/json/tdl/{todo_list}.json', 'r') as file:
        tasks = json.load(file)
    return render_template('todo.html', tasks=tasks, list_name=todo_list)

@app.route('/todo/<string:todo_list>/complete_task/<int:task_id>', methods=['POST'])
def complete_task(todo_list, task_id):
    with open(f'./static/json/tdl/{todo_list}.json', 'r+') as file:
        tasks = json.load(file)
        tasks[task_id]['completed'] = not tasks[task_id]['completed']
        file.seek(0)
        json.dump(tasks, file, indent=4)
        file.truncate()

    return jsonify(success=True)

@app.route('/get_tasks/<string:todo_list>')
def get_tasks(todo_list):
    with open(f'./static/json/tdl/{todo_list}.json', 'r') as file:
        tasks = json.load(file)
    return jsonify(tasks=tasks)

	
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)

