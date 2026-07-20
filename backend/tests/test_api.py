from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_rejects_bad_extension():
    response = client.post(
        "/api/v1/predict",
        files={"file": ("notes.txt", b"not audio", "text/plain")},
    )
    assert response.status_code == 400

def test_predict_rejects_corrupted_audio():
    response = client.post(
        "/api/v1/predict",
        files={"file": ("fake.wav", b"this is not a real wav file", "audio/wav")},
    )
    assert response.status_code == 422

def test_history_returns_list():
    response = client.get("/history")
    assert response.status_code == 200
    assert "history" in response.json()
    assert isinstance(response.json()["history"], list)
