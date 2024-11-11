import unittest
import sys
sys.path.append(r'C:\Users\Zeus\Documents\GitHub\Flask_NetTowers')

from flask import Flask
from app import app  # Импортируем ваш Flask-приложение
from flask.testing import FlaskClient

class RegistrationTestCase(unittest.TestCase):
    def setUp(self):
        # Создаем тестовый клиент
        app.config["TESTING"]= True
        app.config["DEBUG"] = False
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()
        self.base_url = '/reg'


    def test_phone_validator_valid_data(self):
        """Проверка, что корректные данные для phone проходят валидацию."""
        response = self.app.post('/reg', data={
            'phone': '12345678',  # Минимально допустимая длина
            "address": "123 Main St",
            "name": "John Doe"
            # Другие данные формы, которые проходят валидацию
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'its lower than 7 and 10', response.data)

    def test_phone_validator_too_short(self):
        """Проверка, что слишком короткий номер не проходит валидацию."""
        response = self.app.post('/reg', data={
            'phone': '123',  # Меньше минимальной длины
            # Другие данные формы
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'its lower than 7 and 10', response.data)

    def test_phone_validator_too_long(self):
        """Проверка, что слишком длинный номер не проходит валидацию."""
        response = self.app.post('/reg', data={
            'phone': '12345678901',  # Больше максимальной длины
            # Другие данные формы
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'its lower than 7 and 10', response.data)

    def test_other_fields(self):
        """Добавить тесты для других полей формы /registration."""
        # Например, для проверки обязательных полей или других валидаторов