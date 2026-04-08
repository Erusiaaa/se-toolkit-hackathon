from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models import NailDesign
from .seed_data import DESIGNS


def seed_db():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        existing = {item.image_filename for item in db.query(NailDesign).all()}
        for item in DESIGNS:
            if item["image"] in existing:
                continue
            db.add(
                NailDesign(
                    image_filename=item["image"],
                    title=item["title"],
                    description=item["description"],
                    tags=",".join(item["tags"]),
                )
            )
        db.commit()
    finally:
        db.close()
