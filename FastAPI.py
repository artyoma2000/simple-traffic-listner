from fastapi import FastAPI, Request
from datetime import datetime
from pydantic import BaseModel
from typing import List, Dict, Any
import psycopg2

app = FastAPI()

connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    port='5433',
    password="123456789"
)


class Resource(BaseModel):
    resource_name: List[str]


def filter_string(string: str, start_char: str, end_char: str) -> str:
    start_index = string.find(start_char)
    string = string[start_index + 2:]
    end_index = string.find(end_char)
    if end_index == -1:
        return string
    else:
        return string[:end_index]


def create_table():
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS visited_resources
    (id SERIAL PRIMARY KEY,
    resource_name VARCHAR NOT NULL,
    timestamp INTEGER NOT NULL)''')
    connection.commit()
    connection.close()


@app.post('/visited_links')
async def add_resource(request: Request, resource: Resource):
    data = await request.json()
    resource_name = data.get('resource_name')
    timestamp = int(datetime.now().timestamp())
    cursor = connection.cursor()
    for single_one in resource_name:
        cursor.execute("INSERT INTO visited_resources (resource_name, timestamp) VALUES (%s, %s)",
                       (single_one, timestamp))
    connection.commit()
    connection.close()

    return {'message': 'ok'}


@app.get('/visited_links')
async def get_resources():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM visited_resources")
    resources = cursor.fetchall()
    connection.close()
    data = []
    for resource in resources:
        resource_dict = {
            'id': resource[0],
            'resource_name': resource[1],
            'timestamp': resource[2]
        }
        data.append(resource_dict)

    return data


@app.get('/visited_domains')
async def get_domains(start: int, stop: int):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM visited_resources WHERE timestamp >= %s AND timestamp <= %s", (start, stop))
    resources = cursor.fetchall()
    connection.close()
    data = []

    for resource in resources:
        data.append(filter_string(resource[1], '//', '/'))
    data = list(set(data))
    return {"domains": data, "status": "ok"}
