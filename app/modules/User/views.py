from sqlalchemy.orm import Session

from modules.User.models import User

def get_users(db:Session):
    users_list = db.query(User).all() #ORM
    return users_list 