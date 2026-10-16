from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config.database import get_db
from models.webview_link import WebviewLink
from config.google_sheets import (
    get_google_sheet_links,
    add_google_sheet_link,
    update_google_sheet_link,
    delete_google_sheet_link
)

router = APIRouter(prefix="/api/webview-links", tags=["WebviewLinks"])

class LinkRequest(BaseModel):
    title: str
    url: str

@router.get("")
def get_links(db: Session = Depends(get_db)):
    google_links = get_google_sheet_links()
    if google_links is not None:
        return google_links

    links = db.query(WebviewLink).order_by(WebviewLink.createdAt.desc()).all()
    return [{"id": l.id, "title": l.title, "url": l.url} for l in links]

@router.post("")
def create_link(data: LinkRequest, db: Session = Depends(get_db)):
    if not data.title or not data.url:
        raise HTTPException(status_code=400, detail="Title and URL are required")

    google_link = add_google_sheet_link(data.title, data.url)
    if google_link is not None:
        return google_link

    new_link = WebviewLink(title=data.title, url=data.url)
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return {"id": new_link.id, "title": new_link.title, "url": new_link.url}

@router.put("/{link_id}")
def update_link(link_id: int, data: LinkRequest, db: Session = Depends(get_db)):
    if not data.title or not data.url:
        raise HTTPException(status_code=400, detail="Title and URL are required")

    if update_google_sheet_link(link_id, data.title, data.url):
        return {"success": True, "link": {"id": link_id, "title": data.title, "url": data.url}}

    link = db.query(WebviewLink).filter(WebviewLink.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found in SQLite")

    link.title = data.title
    link.url = data.url
    db.commit()
    db.refresh(link)
    return {"success": True, "link": {"id": link.id, "title": link.title, "url": link.url}}

@router.delete("/{link_id}")
def delete_link(link_id: int, db: Session = Depends(get_db)):
    if delete_google_sheet_link(link_id):
        return {"success": True}

    link = db.query(WebviewLink).filter(WebviewLink.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found in SQLite")

    db.delete(link)
    db.commit()
    return {"success": True}
