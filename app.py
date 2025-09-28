from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED
import secrets

# --- App konfigurieren ---
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- Zugangsdaten ---
USERS = {
    "oebv": "oebv",
    "admin": "unipod"
}

security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    """Einfacher Basic-Auth Check"""
    correct_username = credentials.username in USERS
    correct_password = (
        correct_username
        and secrets.compare_digest(USERS[credentials.username], credentials.password)
    )
    if not (correct_username and correct_password):
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# --- Podcast-Daten ---
DEMO_PODCASTS = [
    {"title": "Einführung: Was ist UniPod?", "src": "/static/audio/unipod.mp3", "length": "01:09"},
    {"title": "Beispiel: Der menschliche Schädel", "src": "/static/audio/schaedel.mp3", "length": "01:53"},
]

# --- Startseite ---
@app.get("/", response_class=HTMLResponse)
def home(request: Request, user: str = Depends(authenticate)):
    return templates.TemplateResponse("index.html", {"request": request, "podcasts": DEMO_PODCASTS, "user": user})

# --- Über Uns ---
@app.get("/about", response_class=HTMLResponse)
def about(request: Request, user: str = Depends(authenticate)):
    return templates.TemplateResponse("about.html", {"request": request, "user": user})
