from fastapi.testclient import TestClient
from app.main import app
from app.schemas import UserOut

client = TestClient(app)

def test_root():
    res = client.get("/")
    print('response',res.json())
    assert res.json().get("message")=="Welcolme to my API"
    assert res.status_code==200

def test_create_user():
    res = client.post("/users/",json={"email":"gnaneshp789@gmail.com","password":"password"})
    print(res.json())
    response = UserOut(**res.json())
    assert res.status_code==201
    assert response.email=="gnaneshp789@gmail.com"

def test_login_user():
    res = client.post("/login",data={"username":"gnaneshp789@gmail.com","password":"password"})
    print(res.json())
    assert res.status_code==200