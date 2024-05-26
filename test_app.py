import unittest
from flask_testing import TestCase
from flask import Flask
from io import BytesIO
from app import app
import re

class TestApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    # Тестирование главной страницы
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Решение квадратного уравнения', response.data.decode('utf-8'))

    # Тестирование успешного расчета корней
    def test_calculate_roots(self):
        data = {'a': '1', 'b': '-3', 'c': '2'}
        response = self.client.post('/result', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Корень 1:', response.data.decode('utf-8'))
        self.assertIn('Корень 2:', response.data.decode('utf-8'))

    # Тестирование ошибки, когда 'a' равно нулю
    def test_a_is_zero(self):
        data = {'a': '0', 'b': '1', 'c': '1'}
        response = self.client.post('/result', data=data)
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')

        # Используем регулярное выражение, чтобы проверить наличие сообщения
        expected_error = "Значение.*не может быть равно нулю."
        self.assertTrue(re.search(expected_error, response_text), f"Expected error message not found: {response_text}")

    # Тестирование ошибки, когда дискриминант отрицательный
    def test_no_real_roots(self):
        data = {'a': '1', 'b': '1', 'c': '1'}
        response = self.client.post('/result', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Нет реальных корней', response.data.decode('utf-8'))

    # Тестирование ошибки, когда входные данные некорректны
    def test_invalid_input(self):
        data = {'a': 'invalid', 'b': '1', 'c': '1'}
        response = self.client.post('/result', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Некорректный ввод. Пожалуйста, введите числа.", response.data.decode('utf-8'))

if __name__ == 'main':
    unittest.main()
