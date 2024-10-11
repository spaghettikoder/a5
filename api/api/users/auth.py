from sqlalchemy.orm import Session
import model
import user_schemas


async def get_user(
    db: Session,
    username: str,
) -> user_schemas.UserInDB:
    return db.query(model.User).filter(model.User.username == username).first()

async def get_user_by_id(db: Session, user_id: int):
    ret = db.query(model.User).filter(model.User.user_id == user_id).first()
    return ret
