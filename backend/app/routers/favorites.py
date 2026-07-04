"""收藏夹路由."""
import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.favorite import Favorite

router = APIRouter(prefix="/api/favorites", tags=["favorites"])


class AddFavoriteRequest(BaseModel):
    full_name: str
    name_data: dict  # {full_name, meaning, wuxing, source}


@router.get("", summary="收藏列表")
async def list_favorites(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取当前用户的收藏列表."""
    favs = (
        db.query(Favorite)
        .filter(Favorite.user_id == user.id)
        .order_by(Favorite.created_at.desc())
        .all()
    )
    items = []
    for f in favs:
        try:
            data = json.loads(f.name_data)
        except (json.JSONDecodeError, TypeError):
            data = {}
        items.append({"id": f.id, "full_name": f.full_name, "name_data": data, "created_at": f.created_at.isoformat() if f.created_at else ""})
    return {"total": len(items), "items": items}


@router.post("", summary="添加收藏")
async def add_favorite(
    request: AddFavoriteRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """收藏一个名字."""
    existing = db.query(Favorite).filter(Favorite.user_id == user.id, Favorite.full_name == request.full_name).first()
    if existing:
        raise HTTPException(status_code=409, detail="已收藏过该名字")
    fav = Favorite(
        user_id=user.id,
        full_name=request.full_name,
        name_data=json.dumps(request.name_data, ensure_ascii=False),
    )
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return {"message": "已收藏", "id": fav.id}


@router.delete("/{fav_id}", summary="取消收藏")
async def remove_favorite(
    fav_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """取消收藏."""
    fav = db.query(Favorite).filter(Favorite.id == fav_id, Favorite.user_id == user.id).first()
    if not fav:
        raise HTTPException(status_code=404, detail="收藏不存在")
    db.delete(fav)
    db.commit()
    return {"message": "已取消收藏"}
