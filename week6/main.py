from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, Form
from fastapi import Request
import mysql.connector
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="redredgreengreen")


class MessageData(BaseModel):
    content: str


STYLE = """
<style>
    body {
        font-family: sans-serif;
        background: #e4ece9;
        margin: 0;
        padding: 40px 0;
    }
    .card {
        width: 340px;
        margin: 0 auto;
        background: white;
        border: 1px solid #ddd;
        border-radius: 4px;
        overflow: hidden;
    }
    .card-header {
        background: #0b5c4f;
        color: white;
        text-align: center;
        padding: 18px;
        font-size: 18px;
        font-weight: bold;
    }
    .section {
        padding: 20px 24px;
        border-bottom: 1px solid #eee;
    }
    .section:last-child {
        border-bottom: none;
    }
    .section h3 {
        text-align: center;
        margin: 0 0 14px 0;
    }
    input[type="text"], input[type="email"], input[type="password"] {
        width: 100%;
        padding: 6px;
        margin: 4px 0;
        border: 1px solid #bbb;
        border-radius: 3px;
        box-sizing: border-box;
    }
    .btn-row {
        text-align: center;
        margin-top: 10px;
    }
    #messages p {
        text-align: center;
        margin: 10px 0;
    }
    #messages b {
        color: #0b5c4f;
    }
    a {
        color: #0b5c4f;
    }
</style>
"""


@app.get("/", response_class=HTMLResponse)
def home():
    return STYLE + """
    <div class="card">
        <div class="card-header">歡迎光臨，請註冊登入系統</div>

        <div class="section">
            <h3>註冊帳號</h3>
            <form action="/signup" method="post">
                <input type="text" name="name" placeholder="姓名" required>
                <input type="email" name="email" placeholder="信箱" required>
                <input type="password" name="password" placeholder="密碼" required>
                <div class="btn-row">
                    <input type="submit" value="註冊">
                </div>
            </form>
        </div>

        <div class="section">
            <h3>登入系統</h3>
            <form action="/login" method="post">
                <input type="email" name="email" placeholder="信箱" required>
                <input type="password" name="password" placeholder="密碼" required>
                <div class="btn-row">
                    <input type="submit" value="登入">
                </div>
            </form>
        </div>
    </div>
    """


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
def error_page(msg: str):
    return STYLE + f"""
    <div class="card">
        <div class="card-header">失敗頁面</div>
        <div class="section">
            <p style="text-align:center; color:#555;">{msg}</p>
        </div>
    </div>
    """


@app.get("/member", response_class=HTMLResponse)
def member(request: Request):
    if "id" not in request.session:
        return RedirectResponse(url="/", status_code=303)
    name = request.session["name"]
    return STYLE + f"""
    <div class="card">
        <div class="card-header">歡迎光臨，這是會員頁</div>

        <div class="section" style="text-align:center;">
            <b>{name}</b>，歡迎登入系統<br>
            <a href="/logout">登出系統</a>
        </div>

        <div class="section">
            <h3>快來留言吧</h3>
            <input type="text" id="content" placeholder="內容">
            <div class="btn-row">
                <button onclick="createMessage()">送出</button>
            </div>
        </div>

        <div class="section">
            <div id="messages"></div>
        </div>
    </div>

    <script>
        function loadMessages() {{
            fetch("/api/message")
                .then(response => response.json())
                .then(result => {{
                    let messagesDiv = document.getElementById("messages");
                    messagesDiv.innerHTML = "";
                    for (let msg of result.data) {{
                        let html = "<p><b>" + msg.name + "</b>：" + msg.content;
                        if (msg.self) {{
                            html += " <button onclick='deleteMessage(" + msg.id + ")'>x</button>";
                        }}
                        html += "</p>";
                        messagesDiv.innerHTML += html;
                    }}
                }});
        }}

        function createMessage(){{
            let content = document.getElementById("content").value;
            fetch("/api/message", {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify({{ content: content }})
            }})
                .then(response => response.json())
                .then(result => {{
                    document.getElementById("content").value = "";
                    loadMessages();
                }});
        }}

        function deleteMessage(id) {{
            if (confirm("確定要刪除嗎?")) {{
                fetch("/api/message/" + id, {{ method: "DELETE" }})
                    .then(response => response.json())
                    .then(result => {{
                        loadMessages();
                    }});
            }}
        }}

        loadMessages();
    </script>
    """


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
