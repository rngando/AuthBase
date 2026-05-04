
import requests
from time import sleep


def test_register():
    url = "http://localhost:8000/auth/register"
    for i in range(100):
        sleep(0.1)  # Adiciona um pequeno atraso entre as requisições
        data = {
            "email": f"test{i}@example.com",
            "password": "password123",
            "name": f"Test User {i}"
        }
        response = requests.post(url, json=data)
        print(response.json())

test_register()
