from fasthtml.common import *
from fasthtml.oauth import OAuth, GitHubAppClient, http_patterns, url_match
from monsterui.all import *
from app.ui import *
from app.api import *
import os
import dotenv

dotenv.load_dotenv()

hdrs = Theme.blue.headers(highlightjs=True)

tailwind_config = """
    <script>
        tailwind.config = {
            darkMode: ['class', '[class="uk-theme-dark"]'],  // Match uk-theme-dark
            theme: {
                extend: {}
            }
        }
    </script>
    """

# Insert the tailwind config before the existing script
hdrs.insert(-3, Safe(tailwind_config))

client = GitHubAppClient(os.getenv("GITHUB_CLIENT_ID"),
                         os.getenv("GITHUB_CLIENT_SECRET"))

class Auth(OAuth):
    def __init__(self, app, cli, skip=None, redir_path='/redirect', error_path='/error', 
                 logout_path='/logout', login_path='/login', https=True, http_patterns=http_patterns):
        if not skip: skip = [redir_path,error_path,login_path]
        store_attr()
        def before(req, session):
            auth = req.scope['auth'] = session.get('auth')
            if not auth: return
            # Also add token to request scope
            req.scope['token'] = session.get('github_token')
            res = self.check_invalid(req, session, auth)
            if res: return res
        app.before.append(Beforeware(before, skip=skip))

        @app.get(redir_path)
        def redirect(req, session, code:str=None, error:str=None, state:str=None):
            if not code: 
                session['oauth_error']=error
                return RedirectResponse(self.error_path, status_code=303)
            
            scheme = 'http' if url_match(req.url,self.http_patterns) or not self.https else 'https'
            base_url = f"{scheme}://{req.url.netloc}"
            info = AttrDictDefault(cli.retr_info(code, base_url+redir_path))
            ident = info.get(self.cli.id_key)
            
            if not ident: return self.redir_login(session)
            
            # Store the token in session
            session['github_token'] = cli.token["access_token"]
            
            res = self.get_auth(info, ident, session, state)
            if not res: return self.redir_login(session)
            
            req.scope['auth'] = session['auth'] = ident
            return res

        @app.get(logout_path)
        def logout(session):
            session.pop('auth', None)
            session.pop('github_token', None)
            session.pop('admin_access', None)  # Clear admin access
            return RedirectResponse('/login', status_code=303)
        
    def get_auth(self, info, ident, session, state):
        sign_in(info)
        return RedirectResponse('/', status_code=303)

app, rt = fast_app(hdrs=hdrs)

oauth = Auth(app, client)

@rt
def index(auth):
    return Home(auth=auth)

@rt("/blogposts")
def blogs(auth):
    return ListBlogs(auth=auth)

@rt("/projects")
def projects(auth):
    return ListProjects(auth=auth)

@rt("/blog/{slug:str}")
def blogpost(req, slug:str, auth=None):
    blogpost = get_blog_post(slug)
    if not blogpost: return RedirectResponse("/blogposts", status_code=303)
    add_blog_view(slug)
    return BlogPostPage(post=blogpost, auth=auth, token=req.scope.get('token'))


@rt("/login")
def login(req, auth):
    return LoginPage(oauth_url=oauth.login_link(req), auth=auth)

@rt("/tos")
def tos(auth):
    return TermsOfServicePage(auth=auth)

@rt("/privacy")
def privacy(auth):
    return PrivacyPolicyPage(auth=auth)

@rt("/contact")
def contact(auth):
    return ContactRequestsPage(auth=auth)

@app.post("/api/contact")
async def contact(contact:ContactRequest):
    name = contact.name
    email = contact.email
    message = contact.message
    contact_data = {'name': name,'email': email,'message': message}
    store_contact_request(contact_data)
    
    return Alert(
        DivLAligned(
            UkIcon("check", cls="text-white"), 
            "Message sent successfully! I'll get back to you soon.",
        ),
        cls=AlertT.success
    )

@app.post("/api/projects/new")
async def new_project(project:Project):
    create_project(project)
    return ""

@app.post("/api/blogs/new")
async def new_blog(blog:Blog):
    create_blog_post(blog)
    return ""

@rt("/contact/delete/{id}")
def delete(id: int):
    delete_contact_request(id)
    return ""

@rt("/contact/toggle/{id}")
def toggle(id: int):
    request = mark_contact_request_responded(id)
    return ContactRequestCard(request)

@rt("/admin")
def admin(session,auth=None):
    return AdminPage(session, auth)

@rt("/admin/download/{filename:str}")
def download_db_file(filename: str, auth=None, session=None):
    if (not auth or not get_user(auth).is_admin) and not session.get('admin_access'):
        return RedirectResponse("/", status_code=303)

    try:
        return FileResponse(
            filename,
            filename=filename,
            media_type="application/octet-stream"
        )
    except FileNotFoundError:
        return RedirectResponse("/admin?error=file-not-found", status_code=303)
    
@rt("/admin/upload")
async def upload_database(request, auth=None, session=None):
    if (not auth or not get_user(auth).is_admin) and not session.get('admin_access'):
        return RedirectResponse("/", status_code=303)
    
    form = await request.form()
    files = form.getlist('database')
    
    try:
        for file in files:
            if not isinstance(file, UploadFile): continue
            content = await file.read()
            with open(file.filename, 'wb') as f:
                f.write(content)
        
        return Alert(
            DivLAligned(
                UkIcon("check-circle"),
                P("Database files uploaded successfully!", cls="text-white")
            ),
            cls=AlertT.success
        )
    except Exception as e:
        return Alert(
            DivLAligned(
                UkIcon("alert-triangle"),
                P(f"Error uploading files: {str(e)}", cls="text-white")
            ),
            cls=AlertT.error
        )
    
@rt("/admin/login")
async def admin_login(request, session):
    form = await request.form()
    password = form.get('password')
    
    if password == os.getenv('ADMIN_PASSWORD'):
        session['admin_access'] = True
        return AdminPage(session)  # Return full admin page
    else:
        return Alert(
            DivLAligned(
                UkIcon("x-circle"),
                P("Invalid admin password", cls="text-white")
            ),
            cls=AlertT.error
        )

serve()
