from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# Database setup
DATABASE_URL = "postgresql://admin:admin123@db:5432/yourdb"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Models


class User(Base):
    __tablename__ = "users"
    username = Column(String, index=True)
    email = Column(String, primary_key=True, index=True)
    password = Column(String)


Base.metadata.create_all(bind=engine)

# FastAPI setup
app = FastAPI()
# Define the base directory and static directory
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"

# Mount the static directory
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes


@app.get("/", response_class=HTMLResponse)
async def signin_page(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request, "error": None})


@app.get("/signin", response_class=HTMLResponse)
async def signin_page(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request, "error": None})


@app.post("/signin", response_class=HTMLResponse)
async def signin(request: Request, email: str = Form(...), password: str = Form(...), db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter_by(email=email, password=password).first()
    if user:
        return RedirectResponse(url="/home", status_code=303)
    print("error: Invalid credentials")
    return templates.TemplateResponse("signin.html", {"request": request, "error": "**Invalid credentials"})


@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "error": None})


@app.post("/signup", response_class=HTMLResponse)
async def signup(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: SessionLocal = Depends(get_db)):
    if db.query(User).filter_by(email=email).first():
        return templates.TemplateResponse("signup.html", {"request": request, "error": "**User already exists"})
    new_user = User(username=username, email=email, password=password)
    db.add(new_user)
    db.commit()
    return templates.TemplateResponse("signup.html", {"request": request, "success": "Account created successfully!"})


@app.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
