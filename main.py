from fasthtml.common import *
from fasthtml.oauth import OAuth, GitHubAppClient
from monsterui.all import *
from app.ui import *
from app.api import sign_in
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
    def get_auth(self, info, ident, session, state):
        sign_in(info)
        return RedirectResponse('/', status_code=303)

app, rt = fast_app(hdrs=hdrs)

oauth = Auth(app, client)

@rt
def index(auth):
    print(auth)
    return Home(auth=auth)

@rt("/blogposts")
def blogs(auth):
    return ListBlogs(auth=auth)

@rt("/projects")
def projects(auth):
    return ListProjects(auth=auth)

@rt("/blogposts/sample-post")
def blogpost(auth):
    return BlogPostPage()

@rt("/login")
def login(req, auth):
    return LoginPage(oauth_url=oauth.login_link(req), auth=auth)

serve()
