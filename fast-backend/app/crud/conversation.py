from sqlalchemy.orm import Session
from app.models.conversation import Conversation

def create_conversation(db: Session, user_id: int, thread_id: str):
    db_conv = Conversation(user_id=user_id, thread_id=thread_id)
    db.add(db_conv)
    db.commit()
    db.refresh(db_conv)
    return db_conv

def get_conversations_by_user(db: Session, user_id: int):
    return db.query(Conversation).filter(Conversation.user_id == user_id).all()

def get_conversation(db: Session, user_id: int, thread_id: str):
    return db.query(Conversation).filter(
        Conversation.user_id == user_id,
        Conversation.thread_id == thread_id
    ).first()

def delete_conversation(db: Session, user_id: int, thread_id: str):
    conv = get_conversation(db, user_id, thread_id)
    if conv:
        db.delete(conv)
        db.commit()
        return True
    return False
