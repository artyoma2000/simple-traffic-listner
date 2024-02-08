import datetime
import sqlite3
import unittest
from app import app, create_table, filter_string


class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_add_resource(self):
        response = self.app.post('/visited_links', json={"resource_name": [
            "https://ya.ru/",
            "https://ya.ru/search/?text=мемы+с+котиками",
            "https://sber.ru",
            "https://stackoverflow.com/questions/65724760/how-it-is"
        ]
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'ok'})


def test_filter_string():
    string = "https://www.example.com/path"
    start_char = '//'
    end_char = '/'
    result = filter_string(string, start_char, end_char)
    assert result == "www.example.com"


if __name__ == '__main__':
    create_table()
    unittest.main()
