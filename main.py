from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
import sqlite3

app = FastAPI()

security = HTTPBasic()

# Создаем функцию для создания соединения с базой данных
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Создаем таблицу пользователей, если она не существует
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users
        (username TEXT PRIMARY KEY, password TEXT)
    ''')
    conn.commit()
    conn.close()

create_table()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    # Проверяем существование пользователя в базе данных
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (credentials.username, credentials.password))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        raise HTTPException(status_code=401, detail="Неправильный логин или пароль")
    return credentials.username

@app.get("/protected")
def protected_route(username: str = Depends(get_current_user)):
    return JSONResponse(content={"message": f"Привет, {username}!"}, media_type="application/json")

# Добавляем пользователя в базу данных
@app.post("/register")
def register_user(username: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()
    return JSONResponse(content={"message": "Пользователь добавлен"}, media_type="application/json")