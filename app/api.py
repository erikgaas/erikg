from dataclasses import dataclass
from datetime import datetime
from app.db import get_database
db = get_database()

Project = db.t.project.dataclass()

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

def store_contact_request(contact):
    contacts = db.t.contact
    return contacts.insert(name=contact['name'], email=contact['email'], message=contact['message'], created_at=datetime.now().isoformat(), deleted=False, responded=False, response_date=None)

def get_contact_requests():
    contacts = db.t.contact
    return contacts(where="deleted=?", where_args=(False,))

def delete_contact_request(id):
    contacts = db.t.contact
    return contacts.update(id=id, deleted=True)

def mark_contact_request_responded(id):
    contacts = db.t.contact
    return contacts.update(id=id, responded=True, response_date=datetime.now().isoformat())

def homepage_projects():
    projects = db.t.project
    return projects(where="featured=?", where_args=(True,), order="created_at DESC", limit=3)

def get_projects(statuses=None, tags=None, featured=None, newest=True):
    projects = db.t.project
    where_clauses = []
    where_args = []
    if statuses:
        where_clauses.append("status IN (?)")
        where_args.extend(statuses)
    if tags:
        where_clauses.append("tags LIKE ?")
        where_args.append(f"%{tags}%")
    if featured:
        where_clauses.append("featured=?")
        where_args.append(featured)
    if newest:
        order = "created_at DESC"
    return projects(where=" AND ".join(where_clauses), where_args=where_args, order=order)

def create_project(project:Project):
    projects = db.t.project
    project.created_at = datetime.now().isoformat()
    project.updated_at = project.created_at
    return projects.insert(project)

def homepage_blogposts():
    blogposts = db.t.blog
    return blogposts(where="published=?", where_args=(True,))
