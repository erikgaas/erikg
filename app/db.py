from fastlite import *

class User: github_id: int; username: str; display_name: str; email: str; \
                avatar_url: str; bio: str; created_at: str; last_login: str; is_admin: bool
    
class Blog: 
    id: int
    title: str
    description: str
    image_url: str
    created_at: str
    updated_at: str  # Good to track when content was last modified
    url_slug: str    # For SEO-friendly URLs like /blog/my-awesome-post
    published: bool  # To draft posts before publishing
    author_id: int   # Foreign key to User table
    views: int       # Track post popularity
    tags: str        # Store comma-separated tags to categorize posts

class Project:
    id: int
    title: str
    description: str
    image_url: str
    project_url: str
    github_url: str
    created_at: str
    updated_at: str
    author_id: int
    featured: bool    # To highlight special projects
    status: str      # e.g., 'in-progress', 'completed', 'archived'
    tags: str        # Similar to blog tags

class Contact:
    id: int
    name: str
    email: str
    message: str
    created_at: str
    responded: bool  # Track if you've handled the contact request
    response_date: str
    deleted: bool


def get_database():
    db = database("personal_site.sqlite")
    users = db['users']
    contacts = db['contacts']
    projects = db['projects']
    if users not in db.tables:db.create(User, pk='github_id')
    if contacts not in db.tables:db.create(Contact, pk='id')
    if projects not in db.tables:db.create(Project, pk='id')
    return db
