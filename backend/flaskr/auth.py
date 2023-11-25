from flask_restx import Namespace, Resource, fields
from flask_login import logout_user, login_required, current_user  # 用户认证
from flaskr.extensions import db, login_manager
from flaskr.models import User

api = Namespace('auth', description='用户认证相关接口')

@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.user_id == user_id)).scalar_one_or_none()
