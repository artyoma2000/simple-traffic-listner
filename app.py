from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'


def filter_string(string, start_char, end_char):
    start_index = string.find(start_char)  # Находим индекс первого символа
    string = string[start_index+2:]
    end_index = string.find(end_char)  # Находим индекс второго символа
    if end_index == -1:  # Если один из символов не найден
        return string
    else:
        return string[:end_index]  # выполняем срезы и объединяем строки


def create_table():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS visited_resources 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  resource_name TEXT NOT NULL,
                  timestamp INTEGER NOT NULL)''')
    conn.commit()
    conn.close()


@app.route('/visited_links', methods=['POST'])
def add_resource():
    now = datetime.now()
    data = request.get_json()
    resource_name = data.get('resource_name')
    timestamp = int(now.timestamp())
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    for single_one in resource_name:
        c.execute("INSERT INTO visited_resources (resource_name, timestamp) VALUES (?, ?)",
                  (single_one, timestamp))
    conn.commit()
    conn.close()

    return jsonify({'message': 'ok'})


@app.route('/visited_links', methods=['GET'])
def get_resources():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM visited_resources")
    resources = c.fetchall()
    conn.close()

    data = []
    for resource in resources:
        resource_dict = {
            'id': resource[0],
            'resource_name': resource[1],
            'timestamp': resource[2]
        }
        data.append(resource_dict)

    return jsonify(data)


@app.route('/visited_domains', methods=['GET'])
def get_domains():
    start = request.args.get('start')
    stop = request.args.get('stop')
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM visited_resources WHERE timestamp >= ? AND timestamp <= ?", (start, stop))
    resources = c.fetchall()
    conn.close()
    data = []

    for resource in resources:
        data.append(filter_string(resource[1], '//', '/'))
    data = list(set(data))
    return jsonify({"domains": data, "status": "ok"})


if __name__ == '__main__':
    create_table()
    app.run()
