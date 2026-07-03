from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import urllib.request
import json

app = FastAPI()

# session 要加這行，密鑰隨便打
app.add_middleware(SessionMiddleware, secret_key="some-random-secret-key")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# 首頁
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# 登入驗證
@app.post("/login")
async def login(request: Request, email: str = Form(""), password: str = Form("")):
    if not email or not password:
        return RedirectResponse(url="/ohoh?msg=請輸入信箱和密碼", status_code=303)
    if email == "abc@abc.com" and password == "abc":
        request.session["logged_in"] = True
        return RedirectResponse(url="/member", status_code=303)
    else:
        return RedirectResponse(url="/ohoh?msg=信箱或密碼輸入錯誤", status_code=303)


# 會員頁，沒登入就回首頁
@app.get("/member")
async def member(request: Request):
    if not request.session.get("logged_in"):
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("member.html", {"request": request})


# 登出，清狀態然後回首頁
@app.get("/logout")
async def logout(request: Request):
    request.session["logged_in"] = False
    return RedirectResponse(url="/", status_code=303)


# 錯誤頁
@app.get("/ohoh")
async def error(request: Request, msg: str = ""):
    return templates.TemplateResponse("error.html", {"request": request, "msg": msg})


# 旅館查詢，從第三週的 URL 抓資料
@app.get("/hotel/{hotel_id}")
async def hotel(request: Request, hotel_id: int):
    url_ch = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
    url_en = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"
    try:
        with urllib.request.urlopen(url_ch) as res:
            data_ch = json.loads(res.read().decode("utf-8"))
        with urllib.request.urlopen(url_en) as res:
            data_en = json.loads(res.read().decode("utf-8"))
        # 英文資料用 _id 做對照表
        en_map = {}
        for h in data_en["list"]:
            en_map[h["_id"]] = h
        # 找這個 id 的旅館
        for h in data_ch["list"]:
            if h["_id"] == hotel_id:
                en_info = en_map.get(h["_id"], {})
                info = {
                    "name_ch": h.get("旅宿名稱", ""),
                    "name_en": en_info.get("hotel name", ""),
                    "phone": h.get("電話或手機號碼", "")
                }
                return templates.TemplateResponse("hotel.html", {"request": request, "info": info})
    except Exception:
        pass
    return templates.TemplateResponse("hotel.html", {"request": request, "info": None})
