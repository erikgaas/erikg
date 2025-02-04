from fasthtml.common import *
from monsterui.all import *
from ui import *


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

app, rt = fast_app(hdrs=hdrs)

@rt
def index():
    return Home()

@rt("/blogposts")
def blogs():
    return ListBlogs()

serve()
