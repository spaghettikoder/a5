from sqlalchemy.orm import Session
import model

async def get_post_by_id(db: Session, post_id: int):
    return db.query(model.Post).filter(model.Post.post_id == post_id).first()
