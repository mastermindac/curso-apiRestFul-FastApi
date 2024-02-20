from fastapi.testclient import TestClient
from api import app

#Cliente que utiliza la aplicacion principal
client = TestClient(app)

#Test sobre Endpoint platoId
def test_read_platoId():
    response = client.get("/platos/2")
    assert response.status_code == 200

def test_read_platoId_no_encontrado():
    response = client.get("/platos/239898989")
    assert response.status_code == 404
    assert response.json() == {'error': 'Plato 239898989 no encontrado'}

#Test sobre post de plato
def test_create_plato():
    response = client.post(
        "/platos/",
        headers={"Content-Type": "application/json"},
        json={
            "plato": {
                "nombre": "Prueba",
                "tipo": "entrante",
                "ingredientes": [
                    {
                        "id": 0,
                        "cant": 0,
                        "ud": "string"
                    }
                ]
            },
            "tiempodestacado": 0
            }
    )
    assert response.status_code == 200