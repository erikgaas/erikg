from datetime import datetime
from app.db import get_database
db = get_database()

def create_user_from_github(info):
    users = db.t.user
    return users.insert(github_id=info['id'], username=info['login'], email=info['email'] or '', display_name=info['name'] or info['login'],
                            avatar_url=info['avatar_url'], bio=info['bio'] or '', created_at=datetime.now().isoformat(),
                            last_login=datetime.now().isoformat(), is_admin=False)

def update_sign_in_latest(user):
    users = db.t.user
    user.last_login = datetime.now().isoformat()
    return users.update(user)

def sign_in(info):
    users = db.t.user
    user = users(where="github_id=?", where_args=(info['id'],))
    if user: return update_sign_in_latest(user[0])
    else:    return create_user_from_github(info, db)

def get_user(auth):
    users = db.t.user
    user = users(where="github_id=?", where_args=(auth,))
    return user[0] if user else None

def save_mode_preference(auth, mode):
    pass
