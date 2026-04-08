from pathlib import Path

from fastapi import Depends, FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .config import settings
from .crud import (
    get_all_catalog_designs,
    get_designs_by_tag,
    get_saved_designs_for_user,
    get_saved_tags_for_user,
    get_random_design,
    remove_saved_design_for_user,
    save_design_for_user,
    serialize_design,
)
from .database import get_db
from .seed import seed_db
from .seed_data import TAG_LABELS

app = FastAPI(title=settings.app_name)
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.on_event("startup")
def startup_event():
    seed_db()


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request, tag: str | None = Query(default=None), db: Session = Depends(get_db)):
    designs = get_designs_by_tag(db, tag) if tag else get_all_catalog_designs(db)
    return templates.TemplateResponse(
        "gallery.html",
        {
            "request": request,
            "designs": [serialize_design(item) for item in designs],
            "tags": list(TAG_LABELS.keys()),
            "tag_labels": TAG_LABELS,
            "active_tag": tag,
            "telegram_id": None,
            "page_title": "Curated catalog",
            "is_demo": True,
        },
    )


@app.get("/gallery/{telegram_id}", response_class=HTMLResponse)
def gallery_page(request: Request, telegram_id: str, tag: str | None = Query(default=None), db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "gallery.html",
        {
            "request": request,
            "designs": [serialize_design(item) for item in get_saved_designs_for_user(db, telegram_id, tag)],
            "tags": get_saved_tags_for_user(db, telegram_id),
            "tag_labels": TAG_LABELS,
            "active_tag": tag,
            "telegram_id": telegram_id,
            "page_title": "Saved gallery",
            "is_demo": False,
        },
    )


@app.get("/api/random")
def api_random(db: Session = Depends(get_db)):
    design = get_random_design(db)
    return serialize_design(design) if design else {"message": "No designs found"}


@app.get("/api/by_tag/{tag}")
def api_by_tag(tag: str, db: Session = Depends(get_db)):
    return [serialize_design(item) for item in get_designs_by_tag(db, tag)]


@app.post("/api/save/{telegram_id}/{design_id}")
def api_save(telegram_id: str, design_id: int, db: Session = Depends(get_db)):
    return {"saved": save_design_for_user(db, telegram_id, design_id)}


@app.post("/api/remove/{telegram_id}/{design_id}")
def api_remove(telegram_id: str, design_id: int, db: Session = Depends(get_db)):
    return {"removed": remove_saved_design_for_user(db, telegram_id, design_id)}
