from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, Form
from fastapi import Request
import mysql.connector
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

load_dotenv()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="redredgreengreen")
templates = Jinja2Templates(directory="templates")


class MessageData(BaseModel):
    content: str



@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/signup")
def signup(name: str = Form(), email: str = Form(), password: str = Form()):
    db = mysql.connector.connect(
        host="localhost", user="root",
        password=os.getenv("DB_PASSWORD"), database="website"
    )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM member WHERE email = %s", (email,))
    result = cursor.fetchone()

    if result:
        return RedirectResponse(url="/ohoh?msg=重複的電子郵件", status_code=303)
    else:
        cursor.execute(
            "INSERT INTO member (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        db.commit()
        return RedirectResponse(url="/", status_code=303)


@app.post("/login")
def login(request: Request, email: str = Form(), password: str = Form()):
    db = mysql.connector.connect(
        host="localhost", user="root",
        password=os.getenv("DB_PASSWORD"), database="website"
    )
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM member WHERE email = %s AND password = %s",
        (email, password)
    )
    result = cursor.fetchone()

    if result:
        request.session["id"] = result[0]
        request.session["name"] = result[1]
        request.session["email"] = result[2]
        return RedirectResponse(url="/member", status_code=303)
    else:
        return RedirectResponse(url="/ohoh?msg=電子郵件或密碼錯誤", status_code=303)


@app.get("/ohoh", response_class=HTMLResponse)
def error_page(request: Request, msg: str):
    return templates.TemplateResponse("error.html", {"request": request, "msg": msg})


@app.get("/member", response_class=HTMLResponse)
def member(request: Request):
    if "id" not in request.session:
        return RedirectResponse(url="/", status_code=303)
    name = request.session["name"]
    return templates.TemplateResponse("member.html", {"request": request, "name": name})


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)


@app.post("/api/message")
def create_message(request: Request, data: MessageData):
    if "id" not in request.session:
        return {"error": True}
    content = data.content
    member_id = request.session["id"]

    db = mysql.connector.connect(
        host="localhost", user="root",
        password=os.getenv("DB_PASSWORD"), database="website"
    )
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO message (member_id, content) VALUES (%s, %s)",
        (member_id, content)
    )
    db.commit()
    return {"ok": True}


@app.get("/api/message")
def get_messages(request: Request):
    if "id" not in request.session:
        return {"error": True}
    my_id = request.session["id"]

    db = mysql.connector.connect(
        host="localhost", user="root",
        password=os.getenv("DB_PASSWORD"), database="website"
    )
    cursor = db.cursor()
    cursor.execute("""
        SELECT message.id, member.name, message.content, message.member_id
        FROM message
        JOIN member ON message.member_id = member.id
        ORDER BY message.id DESC
    """)
    rows = cursor.fetchall()

    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "name": row[1],
            "content": row[2],
            "self": row[3] == my_id
        })

    return {"ok": True, "data": data}


@app.delete("/api/message/{message_id}")
def delete_message(request: Request, message_id: int):
    if "id" not in request.session:
        return {"error": True}
    my_id = request.session["id"]

    db = mysql.connector.connect(
        host="localhost", user="root",
        password=os.getenv("DB_PASSWORD"), database="website"
    )
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM message WHERE id = %s AND member_id = %s",
        (message_id, my_id)
    )
    db.commit()
    return {"ok": True}