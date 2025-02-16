from fasthtml.common import *
from fasthtml.oauth import OAuth, GitHubAppClient, http_patterns, url_match
from monsterui.all import *
from app.ui import *
from app.api import *
import os
import dotenv

dotenv.load_dotenv()

hdrs = Theme.blue.headers()

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
    def __init__(self, app, cli, skip=None, redir_path='/redirect', error_path='/error', logout_path='/logout', login_path='/login', https=True, http_patterns=http_patterns):
        if not skip: skip = [redir_path,error_path,login_path]
        store_attr()
        def before(req, session):
            auth = req.scope['auth'] = session.get('auth')
            if not auth: return
            res = self.check_invalid(req, session, auth)
            if res: return res
        app.before.append(Beforeware(before, skip=skip))

        @app.get(redir_path)
        def redirect(req, session, code:str=None, error:str=None, state:str=None):
            if not code: session['oauth_error']=error; return RedirectResponse(self.error_path, status_code=303)
            scheme = 'http' if url_match(req.url,self.http_patterns) or not self.https else 'https'
            base_url = f"{scheme}://{req.url.netloc}"
            info = AttrDictDefault(cli.retr_info(code, base_url+redir_path))
            ident = info.get(self.cli.id_key)
            if not ident: return self.redir_login(session)
            res = self.get_auth(info, ident, session, state)
            if not res:   return self.redir_login(session)
            req.scope['auth'] = session['auth'] = ident
            return res

        @app.get(logout_path)
        def logout(session):
            session.pop('auth', None)
            return self.logout(session)
        
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

@rt("/blogposts/sample-post")
def blogpost():
    return BlogPostPage()

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
    contact_data = {
        'name': name,
        'email': email,
        'message': message
    }
    store_contact_request(contact_data)
    
    return Alert(
        DivLAligned(
            UkIcon("check", cls="text-white"), 
            "Message sent successfully! I'll get back to you soon.",
        ),
        cls=AlertT.success
    )

@rt("/contact/delete/{id}")
def delete(id: int):
    delete_contact_request(id)
    return ""

@rt("/contact/toggle/{id}")
def toggle(id: int):
    request = mark_contact_request_responded(id)
    return ContactRequestCard(request)

serve()
