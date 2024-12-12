from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse

app = FastAPI()

security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "test" or credentials.password != "test":
        raise HTTPException(status_code=401, detail="Неправильный логин или пароль")
    return credentials.username

@app.get("/protected")
def protected_route(username: str = Depends(get_current_user)):
    return JSONResponse(content={"message": f"Привет, {username}!"}, media_type="application/json")