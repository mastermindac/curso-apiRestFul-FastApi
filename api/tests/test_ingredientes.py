from fastapi.testclient import TestClient
from api import app

#Cliente que utiliza la aplicacion principal
client = TestClient(app)

#Primer test sobre el endpont /
def test_read_main():
    response = client.get("/")
    # Comprobaciones
    assert response.status_code == 200
    assert response.json() == {"Hola": "Pakito"}

#Test sobre Endpoint ingredienteId
def test_read_ingredienteId():
    response = client.get("/ingredientes/23")
    assert response.status_code == 200

def test_read_ingredienteId_no_encontrado():
    response = client.get("/ingredientes/239898989")
    assert response.status_code == 404
    assert response.json() == {'error': 'Ingrediente 239898989 no encontrado'}

#Test sobre post de ingrediente
def test_create_ingredient():
    response = client.post(
        "/ingredientes/",
        headers={"Content-Type": "application/json"},
        json={
              "nombre": "Prueba",
              "calorias": 3,
              "carbohidratos": 0,
              "proteinas": 0,
              "grasas": 0,
              "fibra": 0
            }
    )
    assert response.status_code == 200