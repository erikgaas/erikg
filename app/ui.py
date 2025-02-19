from monsterui.all import *
from fasthtml.common import *
from fasthtml.svg import *
from datetime import datetime
from ghapi.all import *

from app.api import *
from app.personal_blog import *

URL = "https://erikgaasedelen.com"

def LoginButton():
    return A(href="/login")(
        Button(cls=(ButtonT.ghost, "hover:bg-muted", "hover:text-primary","transition-colors duration-200", "border border-border/50", "rounded-full","min-w-[100px]"))(
            DivLAligned(UkIcon('log-in', height=16, width=16, cls="mr-2"),  "Sign In",  cls="px-4 py-2"),
        )
    )

def ProfileDropdown(user):
    """Create a profile dropdown button with user info and options"""
    
    # Create dropdown menu items with icons and hotkeys
    dropdown_items = [
        # ("Profile", "user", "⇧⌘P"),
        # ("Settings", "settings", "⌘S"),
        ("Logout", "log-out", "", "/logout")
    ]
    def DropdownItem(text, icon, hotkey="", href=""):
        icon = UkIcon(icon, height=16, width=16, cls="mr-2")
        hotkey = P(hotkey, cls=TextPresets.muted_sm) if hotkey else None
        ANav = A(onclick=f"window.location.href='{href}'", cls="hover:text-primary transition-colors cursor-pointer")
        info = DivLAligned(icon, text)
        item = ANav(DivFullySpaced(info, hotkey))
        return NavCloseLi(item, cls="list-none")
    
    # Main button with user info
    ProfileButton = Button(cls=(ButtonT.ghost, "hover:bg-muted", "hover:text-primary","transition-colors duration-200", "border border-border/50", "rounded-full","min-w-[100px]"))
    profile_avatar = Img(src=user.avatar_url or DiceBearAvatar(user.display_name, 8, 8), alt="Profile", cls="w-8 h-8 rounded-full mr-2")
    profile_name = P(user.display_name, cls=TextPresets.md_weight_muted)
    profile_chevron = UkIcon('chevron-down', height=16, width=16, cls="ml-2")
    button = ProfileButton(DivLAligned(profile_avatar, profile_name, profile_chevron, cls="px-4 py-2"))
    
    dropdown = DropDownNavContainer(
        NavHeaderLi(
            P(user.display_name, cls=TextPresets.bold_sm),
            NavSubtitle(user.email, ),
         cls="list-none"),
        NavDividerLi(cls="list-none"),
        # Menu items
        *[DropdownItem(text, icon, hotkey, href) for text, icon, hotkey, href in dropdown_items], 
    )
        
    return Div(button, dropdown)

def MobileMenu(nav_items):
    return Modal(id="mobile-menu", cls="uk-modal-full", dialog_cls="uk-modal-dialog uk-margin-remove-top")(NavContainer(*nav_items, cls="space-y-4"))

def ErikNavBar(user=None):
    login_btn = LoginButton() if user is None else ProfileDropdown(user)
    sun_icon, moon_icon = UkIcon('sun', height=16, width=16), UkIcon('moon', height=16, width=16)
    icon_group = Div(cls="relative w-4 h-4")(Div(sun_icon, cls="absolute dark:hidden"), Div(moon_icon, cls="absolute hidden dark:block"))

    theme_script = Script("""
            // Check and apply theme on page load
            function applyTheme() {
                const html = document.documentElement;
                const isDark = localStorage.theme === 'dark' || 
                    (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches);
                
                // Ensure uk-theme-blue is always present
                if (!html.classList.contains('uk-theme-blue')) {
                    html.classList.add('uk-theme-blue');
                }
                
                // Handle dark/light theme
                if (isDark) {
                    html.classList.add('dark');
                } else {
                    html.classList.remove('dark');
                }
            }

            // Apply theme immediately
            applyTheme();

            // Function to toggle theme
            function toggleTheme() {
                const html = document.documentElement;
                if (html.classList.contains('dark')) {
                    html.classList.remove('dark');
                    localStorage.theme = 'light';
                } else {
                    html.classList.add('dark');
                    localStorage.theme = 'dark';
                }
                // Ensure uk-theme-blue remains
                if (!html.classList.contains('uk-theme-blue')) {
                    html.classList.add('uk-theme-blue');
                }
            }

            // Watch system theme changes
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
                if (!('theme' in localStorage)) {
                    applyTheme();
                }
            });
        """)
    theme_toggle = Button(cls=ButtonT.secondary, onclick="toggleTheme()")(icon_group)

    social_icons = DivHStacked(cls="space-x-4 hidden sm:flex")(
        UkIconLink('github', href="https://github.com/erikgaas", height=20),
        UkIconLink('linkedin', href="https://www.linkedin.com/in/erikgaas/", height=20),
        UkIconLink('twitter', href="https://x.com/erikgaas", height=20),  
    )

    nav_items = [Li(A("About", href="/")), Li(A("Projects", href="/projects")), Li(A("Blog", href="/blogposts")), Li(A("Contact"), uk_toggle="target: #contact-modal")]
    mobile_menu = Button(UkIcon('menu', height=24, width=24), cls=(ButtonT.ghost, "sm:hidden"), uk_toggle="target: #mobile-menu")

    left_nav  = NavBarLSide(A(H3("Erik Gaasedelen", cls=TextT.primary + "mr-6"), href="/"), NavBarNav(*nav_items, cls="hidden sm:flex"))
    right_nav = NavBarRSide(social_icons, theme_toggle, login_btn, mobile_menu, cls="space-x-4")

    return Div(theme_script, NavBarContainer(left_nav, right_nav, cls="border-b border-border px-4 py-2"), MobileMenu(nav_items))


def HeroSection():
    def SocialButton(icon, href, text):
        return A(href=href, cls=(ButtonT.secondary, "py-3 w-full sm:w-auto inline-flex"))(
            DivLAligned(UkIcon(icon, height=24, width=24, cls="mr-3"), text, cls="px-2")
        )
    
    social_icons = [("github", "https://github.com/erikgaas", "GitHub"), ("linkedin", "https://www.linkedin.com/in/erikgaas", "LinkedIn"), ("file-text", "/static/Erik_Resume.pdf", "Resume")]
    social_buttons = [SocialButton(icon, href, text) for icon, href, text in social_icons]
    social_buttons = Div(*social_buttons,cls="space-y-3 sm:space-y-0 sm:flex sm:space-x-6 w-full")
    name = H1("Erik Gaasedelen", cls=TextT.bold + TextT.muted + TextT.primary + "text-center sm:text-left")
    title = P("Senior Engineering Manager", cls=TextT.lg + TextT.muted + TextT.primary + "text-center sm:text-left")
    about = P("""Fullstack, Deep Learning, Autonomous Vehicles, Med Tech. Learn, build, teach. 🔁""", cls=TextT.muted + "text-center sm:text-left")
    contact = DivLAligned(UkIcon("mail", height=24, width=24, cls="mr-3"),"Get in touch", cls="px-4")
    contact_button = Button(uk_toggle="target: #contact-modal", cls=(ButtonT.primary, "py-3 w-full sm:w-auto sm:min-w-[180px] mt-3 sm:mt-0", "text-lg"))(contact)
    erik_image = Img(src="static/github_profile.png", alt="Profile Picture", cls="rounded-full w-32 h-32 sm:w-48 sm:h-48 object-cover shadow-lg mx-auto sm:mx-0")

    profile_pic = Div(erik_image, cls="mb-6 sm:mb-0 sm:mr-8")
    footer_buttons = Div(social_buttons, contact_button, cls="flex flex-col sm:flex-row sm:justify-between items-center space-y-3 sm:space-y-0")
    profile_info = Div(name, title, about, DividerSplit(), footer_buttons, cls='space-y-4')

    return Card(cls=(CardT.secondary, "mt-8 mx-auto max-w-4xl p-8"))(
        Div(profile_pic, profile_info, cls="flex flex-col sm:flex-row items-center sm:items-start text-center sm:text-left"))


def BlogCard(blog):
    """Create a preview card for a single blog post"""
    image_section = Div(cls="relative")(Img(src=blog.image_url, alt=blog.title, cls="object-cover w-full h-48"))
    formated_created_date = datetime.strptime(blog.created_at, "%Y-%m-%dT%H:%M:%S.%f").strftime("%B %d, %Y")
    published = DivHStacked(UkIcon("calendar", height=16, width=16), P(formated_created_date, cls=TextPresets.muted_sm), cls="space-x-2")
    views = DivHStacked(UkIcon("eye", height=16, width=16), P(f"{blog.views} views", cls=TextPresets.muted_sm), cls="space-x-2")
    metadata = DivLAligned(cls="space-x-4")(published, views)
    title_section = Div(cls="space-y-2")(H3(blog.title, cls=TextT.bold), metadata)
    description = P(blog.description, cls=TextPresets.muted_sm)
    tags = Div(cls="flex flex-wrap gap-2")(*[Label(tag.strip(), cls=LabelT.secondary) for tag in blog.tags.split(',') if tag.strip()])
    read_more = A(href=f"/blog/{blog.url_slug}", cls=(AT.muted, TextPresets.bold_sm))(
        DivLAligned("Read more", UkIcon("arrow-right", height=16, width=16, cls="ml-2"))
    )
    content_section = Div(title_section, description, tags, read_more, cls="space-y-4 p-6")
    return Card(image_section, content_section, cls=(CardT.hover + CardT.secondary, "max-w-sm"))

def HomeSectionHeader(title, description, button_text, button_href):
    view_all_btn = A(DivLAligned(button_text, UkIcon("arrow-right", height=16, width=16), cls="px-4 py-2"),
        href=button_href,
        cls=(ButtonT.secondary, "hover:shadow-md", "transition-all duration-200", 
             "border border-border", "min-w-[160px]", "inline-flex")
    )

    header = DivFullySpaced(
        Div(H2(title, cls=(TextT.bold, TextT.primary, "text-2xl")), P(description, cls=(TextPresets.muted_sm, "mt-2")), cls="space-y-1"),
        view_all_btn, cls="items-center"
    )
    return header

def LatestBlogs(blogs):
    """Create a section displaying the latest blog posts"""
    header = HomeSectionHeader("Latest Posts", "Check out my latest thoughts and tutorials", "View all posts", "/blogposts")    
    blog_grid = Div(cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8 justify-items-center")(*[BlogCard(blog) for blog in blogs])
    return Section(header, blog_grid, cls="mt-16 mx-auto max-w-6xl px-4")

# # Let's create some sample blog posts
# sample_blogs = [
#     SimpleNamespace(
#         title="Building a Personal Website with MonsterUI",
#         description="A deep dive into creating a modern, responsive personal website using Python and MonsterUI framework.",
#         image_url="https://picsum.photos/800/400?random=1",
#         created_at="July 24, 2024",
#         views=142,
#         tags="python,web-development,tutorial",
#         url_slug="building-personal-website-monsterui"
#     ),
#     SimpleNamespace(
#         title="Machine Learning in Production",
#         description="Best practices for deploying and monitoring machine learning models in production environments.",
#         image_url="https://picsum.photos/800/400?random=2",
#         created_at="July 22, 2024",
#         views=98,
#         tags="machine-learning,devops,python",
#         url_slug="ml-in-production"
#     ),
#     SimpleNamespace(
#         title="The Future of Autonomous Vehicles",
#         description="Exploring recent developments in self-driving technology and what the future might hold.",
#         image_url="https://picsum.photos/800/400?random=3",
#         created_at="July 20, 2024",
#         views=215,
#         tags="autonomous-vehicles,technology,future",
#         url_slug="future-of-av"
#     )
# ]

@dataclass
class ContactRequest:
    name: str
    email: str
    message: str

def ContactModal():
    modal_header = DivLAligned(UkIcon("mail", height=24, width=24, cls="text-primary mr-3"), H3("Get in Touch", cls=TextT.bold))

    alert = Alert(
        DivLAligned(
            UkIcon("info", cls="text-white dark:text-white !important"), 
            Div(
                H4("Let's Connect!", cls="text-white dark:text-white !important"),
                P("I'll get back to you as soon as possible.", cls="text-white dark:text-white !important")
            )
        ),
        cls=(AlertT.info, "mb-6")
    )

    name_input = Div(LabelInput("Name", id="name",  placeholder="Your name", icon="user",uk_tooltip="Please enter your full name"))
    email_input = Div(
        LabelInput("Email", id="email", type="email", placeholder="your.email@example.com", icon="mail", uk_tooltip="I'll use this to respond to your message")
    )

    message_input = Div(
        LabelTextArea("Message", id="message", 
                      placeholder="What would you like to discuss? Feel free to be as detailed as needed.",
                      uk_tooltip="Share your thoughts, questions, or project ideas"
        )
    )

    # subscribe_checkbox = Div(
    #     LabelCheckboxX("Keep me updated about new blog posts and projects", 
    #                     id="subscribe", cls="text-sm", input_cls="bg-primary hover:bg-primary-focus border-primary")
    # )

    cancel_button = Button(cls=(ButtonT.secondary, "py-3 min-w-[120px]"), uk_toggle="target: #contact-modal")(
        DivLAligned(UkIcon("", height=20, width=20, cls="mr-2"), 
                    "Cancel",
                    cls="px-4")
    )

    send_button = Button(cls=(ButtonT.primary, "py-3 min-w-[180px]"), submit=True)(
        DivLAligned(UkIcon("send", height=20, width=20, cls="mr-2"),
            "Send Message",
            Loading(cls=(LoadingT.spinner + LoadingT.sm, "ml-2"), htmx_indicator=True, id="loading-indicator"),
            cls="px-4"), 
    )

    action_buttons = DivRAligned(cancel_button, send_button, cls="space-x-4")

    contact_form = Form(
        Grid(name_input, email_input, cols=2, gap=6), 
        message_input,  
        DivRAligned(action_buttons, cls="mt-6"),
        cls='space-y-6',
        hx_post="/api/contact", 
        hx_trigger="submit",
        hx_on="htmx:afterRequest: UIkit.modal('#contact-modal').hide()"
    )

    return Modal(
        alert, 
        contact_form, 
        header=(modal_header, ),
        cls=(CardT.secondary, "w-full mx-auto"), 
        id="contact-modal"
    )

def ProjectCard(project):
    """Create a card for a single project"""
    status_colors = {'in-progress': AlertT.warning, 'completed': AlertT.success, 'archived': AlertT.info}
    image_section = Div( Img(src=project.image_url, alt=project.title, cls="object-cover w-full h-48"), cls="relative")
    badges = Div(
        Alert(project.status.title(), cls=(status_colors.get(project.status, AlertT.info), "text-sm")),
        Label("Featured", cls=LabelT.secondary) if project.featured else None, cls="absolute top-4 right-4 space-y-2")
    
    title_section = DivFullySpaced(
        H3(project.title, cls=TextT.bold),
        DivHStacked(UkIconLink("github", href=project.github_url, height=20),
                    UkIconLink("link", href=project.project_url, height=20), cls="space-x-3"))
    
    description = P(project.description, cls=TextPresets.muted_sm)

    tags = Div(
        *[Label(tag.strip(), cls=LabelT.secondary) for tag in project.tags.split(',') if tag.strip()],
        cls="flex flex-wrap gap-2"
    )
    
    return Card(image_section, badges, Div(title_section, description, tags, cls="space-y-4 p-6"),
                cls=(CardT.hover + CardT.secondary, "max-w-sm"))

def ProjectsSection(projects):
    """Create the projects section"""
    header = HomeSectionHeader("Featured Projects", "Some things I've built", "View all projects", "/projects")
    project_grid = Div(
        cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8 justify-items-center"
    )(*[ProjectCard(project) for project in projects])
    
    return Section(header, project_grid, cls="mt-16 mx-auto max-w-6xl px-4")

# sample_projects = [
#     SimpleNamespace(
#         title="AutoML Platform",
#         description="An end-to-end machine learning platform for automated model training and deployment.",
#         image_url="https://picsum.photos/800/400?random=4",
#         project_url="https://github.com/username/automl",
#         github_url="https://github.com/username/automl",
#         status="completed",
#         featured=True,
#         tags="python,machine-learning,docker"
#     ),
#     SimpleNamespace(
#         title="Autonomous Navigation System",
#         description="Real-time path planning and obstacle avoidance system for autonomous vehicles.",
#         image_url="https://picsum.photos/800/400?random=5",
#         project_url="https://github.com/username/nav-system",
#         github_url="https://github.com/username/nav-system",
#         status="in-progress",
#         featured=True,
#         tags="robotics,c++,ros"
#     ),
#     SimpleNamespace(
#         title="Medical Image Analysis",
#         description="Deep learning models for automated medical image analysis and diagnosis.",
#         image_url="https://picsum.photos/800/400?random=6",
#         project_url="https://github.com/username/med-image",
#         github_url="https://github.com/username/med-image",
#         status="completed",
#         featured=True,
#         tags="deep-learning,healthcare,python"
#     )
# ]

def Footer():
    social_links = [("github", "https://github.com/erikgaas"), ("linkedin", "https://www.linkedin.com/in/erikgaas"), ("twitter", "https://x.com/erikgaas"),]
    social_icons = DivHStacked(
        *[UkIconLink(icon, href=url, height=20, cls="text-gray-300 hover:text-primary transition-colors")for icon, url in social_links],
        cls="space-x-6"
    )

    copyright = P(f"© {datetime.now().year} Erik Gaasedelen. All rights reserved.", cls=TextPresets.muted_sm)
    return Section(DivVStacked(DividerSplit(), DivCentered(social_icons, copyright, cls="space-y-4 py-8")), cls="mt-auto")

def BlogToolbar(tags, active_tag=None, sort_by="newest"):
    search_input = Div(
        Input(
            placeholder="Search posts...",
            cls="w-full sm:w-[300px] bg-secondary border-border text-secondary-foreground hover:bg-secondary/80 focus:bg-secondary/80",
            uk_icon="icon: search"
        ),
        cls="flex-grow sm:flex-grow-0"
    )
    
    sort_options = [("newest", "Newest First"), ("oldest", "Oldest First"), ("popular", "Most Popular"), ("updated", "Recently Updated")]
    
    sort_dropdown = UkSelect(
        *[Option(label, value=value, selected=(value==sort_by))
          for value, label in sort_options],
        cls="w-[200px]",
        placeholder="Sort by"
    )

    def TagButton(tag): return Button(tag, cls=(ButtonT.ghost, "rounded-full text-sm py-1 px-3", "bg-primary text-white" if tag == active_tag else ""))
    tag_filters = Div(cls="flex flex-wrap gap-2")(*[TagButton(tag) for tag in tags])
    
    return Div(DivFullySpaced(search_input, sort_dropdown, cls="flex-wrap gap-4"), tag_filters, cls="space-y-4 mb-8")


def BlogPage(blogs, auth=None):
    all_tags = set()
    for blog in blogs: all_tags.update(tag.strip() for tag in blog.tags.split(','))
    
    header = DivFullySpaced(
        Div(
            H1("Blog", cls=(TextT.bold + TextT.primary, "text-3xl")),
            P("Thoughts, tutorials, and insights", cls=TextPresets.muted_sm),
            cls="space-y-2"
        ),
        Button(
            DivLAligned(
                UkIcon("plus-circle", height=20),
                "New Post"
            ),
            cls=ButtonT.primary,
            uk_toggle="target: #new-blog-modal"
        ) if auth and get_user(auth).is_admin else None
    )
    
    toolbar = BlogToolbar(sorted(all_tags))
    blog_grid = Div(cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8 justify-items-center")(*[BlogCard(blog) for blog in blogs])

    pagination = DivHStacked(
        Button(UkIcon("chevron-left"), cls=ButtonT.ghost),
        Button("1", cls=(ButtonT.primary, "mx-1")),
        Button("2", cls=(ButtonT.ghost, "mx-1")),
        Button("3", cls=(ButtonT.ghost, "mx-1")),
        Button(UkIcon("chevron-right"), cls=ButtonT.ghost),
        cls="mt-8 justify-center space-x-2"
    )

    return Div(header, toolbar, blog_grid, pagination, NewBlogModal() if auth and get_user(auth).is_admin else None, cls="container mx-auto max-w-6xl px-4 py-8 space-y-8")

def ProjectToolbar(tags, statuses, active_tag=None, active_status=None, sort_by="newest"):
    search_input = Div(
        Input(
            placeholder="Search projects...",
            cls="w-full sm:w-[300px] bg-secondary border-border text-secondary-foreground hover:bg-secondary/80 focus:bg-secondary/80",
            uk_icon="icon: search"
        ),
        cls="flex-grow sm:flex-grow-0"
    )
    
    sort_options = [
        ("newest", "Newest First"),
        ("oldest", "Oldest First"),
        ("updated", "Recently Updated"),
        ("featured", "Featured First")
    ]
    
    sort_dropdown = UkSelect(
        *[Option(label, value=value, selected=(value==sort_by))
          for value, label in sort_options],
        cls="w-[200px]",
        placeholder="Sort by"
    )

    status_filters = Div(cls="flex flex-wrap gap-2")(
        *[Button(
            DivLAligned(
                status.title(),
                cls="px-2 py-1"
            ),
            cls=(
                ButtonT.ghost,
                "rounded-full text-sm",
                "bg-primary text-white" if status == active_status else ""
            )
        ) for status in statuses]
    )
    
    tag_filters = Div(cls="flex flex-wrap gap-2")(
        *[Button(
            tag,
            cls=(
                ButtonT.ghost,
                "rounded-full text-sm py-1 px-3",
                "bg-primary text-white" if tag == active_tag else ""
            )
        ) for tag in tags]
    )
    
    return Div(cls="space-y-6 mb-8",)(
        DivFullySpaced(search_input, sort_dropdown, cls="flex-wrap gap-4"),
        Div(H4("Status", cls=TextPresets.bold_sm), status_filters, cls="space-y-2"),
        Div(H4("Technologies", cls=TextPresets.bold_sm), tag_filters, cls="space-y-2"),
    )

def ProjectPage(projects, auth=None):
    # Extract unique tags and statuses from all projects
    all_tags = set()
    all_statuses = set()
    for project in projects:
        all_tags.update(tag.strip() for tag in project.tags.split(','))
        all_statuses.add(project.status)
    
    header = DivFullySpaced(
        Div(
            H1("Projects", cls=(TextT.bold + TextT.primary, "text-3xl")),
            P("A showcase of my work and experiments", cls=TextPresets.muted_sm),
            cls="space-y-2"
        ),
        Button(
            DivLAligned(
                UkIcon("plus-circle", height=20, width=20, cls="mr-2"),
                "New Project"
            ),
            cls=ButtonT.primary,
            uk_toggle="target: #new-project-modal"
        ) if auth and get_user(auth).is_admin else None
    )
    
    toolbar = ProjectToolbar(sorted(all_tags), sorted(all_statuses))
    
    project_grid = Div(
        cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8 justify-items-center"
    )(*[ProjectCard(project) for project in projects])

    pagination = DivHStacked(
        Button(UkIcon("chevron-left"), cls=ButtonT.ghost),
        Button("1", cls=(ButtonT.primary, "mx-1")),
        Button("2", cls=(ButtonT.ghost, "mx-1")),
        Button("3", cls=(ButtonT.ghost, "mx-1")),
        Button(UkIcon("chevron-right"), cls=ButtonT.ghost),
        cls="mt-8 justify-center space-x-2"
    )

    return Div(
        header, 
        toolbar, 
        project_grid, 
        pagination, 
        NewProjectModal() if auth and get_user(auth).is_admin else None,
        cls="container mx-auto max-w-6xl px-4 py-8 space-y-8"
    )

# more_sample_projects = sample_projects + [
#     SimpleNamespace(
#         title="Personal Finance Dashboard",
#         description="Interactive dashboard for tracking personal finances and investments.",
#         image_url="https://picsum.photos/800/400?random=7",
#         project_url="https://github.com/username/finance-dash",
#         github_url="https://github.com/username/finance-dash",
#         status="in-progress",
#         featured=False,
#         tags="python,react,finance"
#     ),
#     SimpleNamespace(
#         title="Smart Home Controller",
#         description="IoT system for managing home automation devices.",
#         image_url="https://picsum.photos/800/400?random=8",
#         project_url="https://github.com/username/smart-home",
#         github_url="https://github.com/username/smart-home",
#         status="archived",
#         featured=False,
#         tags="python,iot,raspberry-pi"
#     )
# ]

def TableOfContents(sections):
    def create_toc_link(text, id):
        return Li(A(text, href=f"#{id}"), cls=(TextPresets.muted_sm, "list-none"))
    
    return Div(
        H4("Table of Contents", cls=TextPresets.muted_sm),
        NavContainer(
            *[create_toc_link(text, id) for text, id in sections],
            uk_scrollspy_nav="closest: li; scroll: true; offset: 100",
            sticky="offset: 100",
            cls=(NavT.primary, "space-y-2 p-4 rounded-lg border border-border w-64")
        ),
        cls="hidden [@media(min-width:1340px)]:block fixed top-24",
        style="left: max(40px, calc((100vw - 768px) / 2 - 280px))"
    )

# Let's create a sample blog post to demonstrate
def BlogPost(auth=None):
    # Sample sections for our blog
    sections = [
        ("Introduction", "introduction"),
        ("Background", "background"),
        ("Methodology", "methodology"),
        ("Results", "results"),
        ("Discussion", "discussion"),
        ("Conclusion", "conclusion")
    ]
    
    # Create the content sections
    def create_section(title, id):
        return Section(
            H2(title, cls=(TextT.bold, "text-2xl mb-4")),
            P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 10),
            P("Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " * 10),
            id=id,
            cls="mb-12"
        )
    
    content = Div(*[create_section(title, id) for title, id in sections],
                  cls="prose max-w-none") # prose class for better typography
    
    gh_integration = GithubInsights(auth=auth)
    
    # Create the layout with TOC on the left and content on the right
    return Div(
        TableOfContents(sections),
        gh_integration,
        content,
        cls="container mx-auto max-w-3xl px-4 py-8 relative"  # Narrower max-width to allow space for TOC
    )

def estimate_read_time(text, words_per_minute=200):
    """Estimate reading time in minutes"""
    word_count = len(text.split())
    minutes = max(1, round(word_count / words_per_minute))
    return f"{minutes} min read"

def PostTags(tags):
    """Render a list of tags with consistent styling"""
    return Div(
        *[Label(tag.strip(), cls=LabelT.secondary) for tag in tags.split(',')],
        cls="flex flex-wrap gap-2 mb-4"
    )

def AuthorInfo(author_name, created_at):
    """Author avatar and details"""
    formatted_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%f").strftime("%B %d, %Y")
    return DivLAligned(
        Img(src="../static/github_profile.png", alt="Profile", cls="w-8 h-8 rounded-full mr-2"),
        Div(
            P(author_name, cls=TextT.lg + TextT.muted + TextT.secondary),
            P(formatted_date, cls=TextPresets.muted_sm)
        ),
        cls="gap-3"
    )

def PostMetrics(views):
    """Reading time and view count"""
    return DivLAligned(
        DivHStacked(UkIcon("eye"), P(f"{views} views", cls=TextPresets.muted_sm)),
        cls="gap-4"
    )

def ShareButtons(post):
    """Social sharing buttons with working share functionality"""
    url = f"{URL}/blog/{post.url_slug}"
    def twitter_share(title, url): return f"https://twitter.com/intent/tweet?text={title}&url={url}"
    def linkedin_share(title, url): return f"https://www.linkedin.com/sharing/share-offsite/?url={url}"
    def facebook_share(url): return f"https://www.facebook.com/sharer/sharer.php?u={url}"
    
    def copy_link(cls=""):
        return Button(
            UkIcon("link"), 
            cls=cls,
            uk_tooltip="Copy link to clipboard",
            onclick="navigator.clipboard.writeText(window.location.href); UIkit.notification({message: 'Link copied to clipboard!', pos: 'bottom-right', status: 'success'})"
        )
    
    def ShareAnchor(icon, href, tooltip):
        return A(UkIcon(icon), href=href, target="_blank", uk_tooltip=tooltip, cls=ButtonT.ghost)
    
    social = [
        ShareAnchor("twitter", twitter_share(post.title, url), "Share on Twitter"),
        ShareAnchor("linkedin", linkedin_share(post.title, url), "Share on LinkedIn"),
        ShareAnchor("facebook", facebook_share(url), "Share on Facebook"),
        copy_link(cls=ButtonT.ghost)
    ]

    return Div(
        H4("Share this post", cls=TextPresets.bold_sm + TextT.default + TextT.muted + TextT.secondary),
        DivHStacked(*social, cls="gap-2"),
        cls="mt-6"
    )

def NavButton(post, direction="left"):
    """Navigation button for previous/next post"""
    if not post: return Div(cls="flex-1")
    
    is_next = direction == "right"
    icon = UkIcon(f"arrow-{direction}", height=20)
    text_div = Div(
        P("Next" if is_next else "Previous", cls=TextPresets.muted_sm),
        P(post.title, cls=TextPresets.bold_sm),
        cls="text-right" if is_next else ""
    )
    
    content = DivRAligned(text_div, icon, cls="gap-2") if is_next else DivLAligned(icon, text_div, cls="gap-2")
    return A(content, href=f"/blog/{post.url_slug}")

def BlogPostHeader(post):
    return Section(
        PostTags(post.tags),
        H1(post.title, cls=(TextT.lg + TextT.muted + TextT.primary, "text-4xl mb-6")),
        DivLAligned(
            AuthorInfo("Erik Gaasedelen", post.created_at),
            PostMetrics(post.views),
            cls="justify-between items-center"
        ),
        ShareButtons(post),
        DividerSplit(),
        cls="mb-8"
    )

def BlogPostNavigation(prev_post=None, next_post=None):
    return Section(
        DividerSplit(),
        DivFullySpaced(
            NavButton(prev_post, "left"),
            Button(DivLAligned(UkIcon("list"), "All posts"), 
                   href="/blog", cls=ButtonT.secondary),
            NavButton(next_post, "right")
        ),
        cls="mt-12"
    )

def FullBlogPost(post=None, prev_post=None, next_post=None, auth=None, token=None):
    if post.url_slug == "build-a-personal-blog":
        content = BuildPersonalSiteBlogPost(auth=auth, token=token)
    
    return Div(
        BlogPostHeader(post),
        content,
        #BlogPostNavigation(prev_post, next_post),
        cls="container mx-auto max-w-3xl px-4 py-8"
    )

def LoginScreen(oauth_url):
    """Create a more polished login screen with GitHub OAuth"""
    page_background = "bg-gradient-to-b from-background to-secondary/10"
    
    header = DivCentered(
        # Add a small brand icon above the title
        UkIcon("code", height=40, width=40, cls="text-primary mb-4"),
        H2("Welcome", cls=(TextT.bold, TextT.primary, "text-3xl")),
        P("Sign in to access interactive features", 
          cls=(TextPresets.muted_sm, "max-w-sm text-center")),
        cls="space-y-2 mb-8"
    )

    github_button = A(
        DivLAligned(cls="px-4 py-3")(
            UkIcon("github", height=24, width=24, cls="mr-3"), 
            "Continue with GitHub",
        ),
        href=oauth_url,
        cls=(ButtonT.primary, "w-full inline-flex justify-center hover:opacity-90",
             "transition-all duration-200 transform hover:scale-[1.02]",
             "shadow-md hover:shadow-lg")
    )

    info_section = Div(cls="space-y-4 mt-8")(
        DividerSplit("Why GitHub?", cls="text-primary/70"),
        Card(
            DivLAligned(
                UkIcon("shield", height=16, cls="text-primary"), 
                P("Secure and simple login process", cls=TextPresets.muted_sm),
                cls="gap-2"
            ),
            DivLAligned(
                UkIcon("key", height=16, cls="text-primary"), 
                P("No additional password needed", cls=TextPresets.muted_sm),
                cls="gap-2"
            ),
            cls=(CardT.secondary, "space-y-4 p-4 bg-secondary/50")
        ),
    )

    footer = Div(
        P("By continuing, you agree to our ",
          A("Terms of Service", href="/tos", 
            cls=(AT.muted, "hover:text-primary transition-colors")),
          " and ",
          A("Privacy Policy", href="/privacy", 
            cls=(AT.muted, "hover:text-primary transition-colors")),
          cls=(TextPresets.muted_sm, "text-secondary-foreground/70")),
        cls="mt-8 text-center"
    )

    back_link = A(
        DivLAligned(
            UkIcon("arrow-left", height=16, cls="mr-2"), 
            "Back to home",
            cls="group-hover:transform group-hover:-translate-x-1 transition-transform"
        ),
        href="/",
        cls=(AT.muted, "mt-6 inline-flex hover:text-primary transition-colors group")
    )

    login_card = Card(
        header, github_button, info_section, footer,
        cls=(CardT.secondary, "p-8 w-full max-w-md",
             "border border-border/50",
             "shadow-xl hover:shadow-2xl transition-shadow duration-500",
             "backdrop-blur-sm bg-secondary/50")
    )

    # Add decorative elements
    decorative_circle = Div(
        cls="absolute top-[-120px] right-[-120px] w-64 h-64 rounded-full bg-primary/5 blur-3xl pointer-events-none"
    )
    
    decorative_circle2 = Div(
        cls="absolute bottom-[-150px] left-[-150px] w-96 h-96 rounded-full bg-primary/5 blur-3xl pointer-events-none"
    )

    return Div(
        Div(
            decorative_circle,
            decorative_circle2,
            login_card, 
            back_link,
            cls="flex flex-col items-center justify-center min-h-[80vh] relative"
        ),
        cls=f"container mx-auto px-4 {page_background}"
    )

def TermsOfService():
    return Div(cls="container mx-auto max-w-3xl px-4 py-8 prose dark:prose-invert")(
        H1("Terms of Service"),
        
        Section(
            H2("1. Agreement to Terms"),
            P("""By accessing and using this website (erikgaasedelen.com), you accept and agree to be bound by the terms and 
               provisions of this agreement.""")
        ),
        
        Section(
            H2("2. User Accounts"),
            P("""To access certain features of the site, you may be required to sign in using GitHub OAuth. You are responsible for:"""),
            Ul(
                Li("Maintaining the confidentiality of your account"),
                Li("All activities that occur under your account"),
                Li("Ensuring your GitHub account information is accurate")
            )
        ),
        
        Section(
            H2("3. Content and Conduct"),
            P("""Users may post comments and interact with blog posts. You retain ownership of your content, but grant us a license to use, 
               display, and distribute it on the site. You agree not to:"""),
            Ul(
                Li("Post illegal, harmful, or offensive content"),
                Li("Spam or abuse site features"),
                Li("Attempt to disrupt the site's functionality"),
                Li("Impersonate others or misrepresent your identity")
            )
        ),
        
        Section(
            H2("4. Intellectual Property"),
            P("""The site content, features, and functionality are owned by Erik Gaasedelen and are protected by copyright and other 
               intellectual property laws.""")
        ),
        
        Section(
            H2("5. Third-Party Services"),
            P("""This site uses GitHub for authentication and may include links to third-party websites. We are not responsible for 
               third-party content or privacy practices.""")
        ),
        
        Section(
            H2("6. Limitation of Liability"),
            P("""The site is provided 'as is' without warranties of any kind. We are not liable for any damages arising from 
               your use of the site.""")
        ),
        
        Section(
            H2("7. Changes to Terms"),
            P("""We reserve the right to modify these terms at any time. Users will be notified of significant changes.""")
        ),
        
        Section(
            H2("8. Contact Information"),
            P("""If you have questions about these terms, please contact us through the site's contact form.""")
        ),
        
        P(f"Last updated: {datetime.now().strftime('%B %d, %Y')}", cls=TextPresets.muted_sm)
    )

def PrivacyPolicy():
    return Div(cls="container mx-auto max-w-3xl px-4 py-8 prose dark:prose-invert")(
        H1("Privacy Policy"),
        P(f"Last Updated: {datetime.now().strftime('%B %d, %Y')}"),
        
        Section(
            H2("1. Information We Collect"),
            H3("1.1 Information from GitHub Authentication"),
            P("""When you sign in using GitHub, we receive and store:"""),
            Ul(
                Li("Your GitHub username and ID"),
                Li("Your display name"),
                Li("Your email address (if public on GitHub)"),
                Li("Your avatar URL"),
                Li("Your public GitHub profile information")
            ),
            
            H3("1.2 Information You Provide"),
            P("""We collect information you actively provide:"""),
            Ul(
                Li("Comments on blog posts"),
                Li("Contact form submissions"),
                Li("Interaction data with blog content")
            )
        ),
        
        Section(
            H2("2. How We Use Your Information"),
            P("""We use the collected information for:"""),
            Ul(
                Li("Authentication and account management"),
                Li("Displaying your profile information alongside your comments"),
                Li("Responding to your contact form submissions"),
                Li("Improving site functionality and content"),
                Li("Ensuring site security and preventing abuse")
            )
        ),
        
        Section(
            H2("3. Data Storage and Security"),
            P("""We implement reasonable security measures to protect your information:"""),
            Ul(
                Li("All data is stored securely in our database"),
                Li("We use secure HTTPS connections"),
                Li("Access to personal information is restricted to authorized personnel"),
                Li("We regularly review our security practices")
            )
        ),
        
        Section(
            H2("4. Cookies and Local Storage"),
            P("""We use:"""),
            Ul(
                Li("Session cookies for authentication"),
                Li("Local storage for theme preferences"),
                Li("GitHub OAuth cookies for authentication")
            )
        ),
        
        Section(
            H2("5. Third-Party Services"),
            P("""We use the following third-party services:"""),
            Ul(
                Li("GitHub (for authentication)"),
                Li("Any analytics services you use", cls=TextPresets.muted_sm)
            ),
            P("""Each third-party service has its own privacy policy and data handling practices.""")
        ),
        
        Section(
            H2("6. Your Rights"),
            P("""You have the right to:"""),
            Ul(
                Li("Access your personal information"),
                Li("Request deletion of your account and data"),
                Li("Opt out of communications"),
                Li("Request a copy of your data")
            )
        ),
        
        Section(
            H2("7. Changes to Privacy Policy"),
            P("""We may update this privacy policy from time to time. We will notify users of any material changes through:"""),
            Ul(
                Li("A notice on our website"),
                Li("An email to registered users (for significant changes)")
            )
        ),
        
        Section(
            H2("8. Contact Information"),
            P("""If you have questions about this privacy policy or your personal data, please:"""),
            Ul(
                Li("Use our contact form"),
            )
        ),
        
        DividerSplit(),
        
        P("""This privacy policy is intended to help you understand what information we collect, 
           how we use it, and what choices you have regarding your information.""", 
           cls=TextPresets.muted_sm)
    )

def ContactRequestCard(contact):
    """Create a card for a single contact request"""
    status = Alert("Responded" if contact.responded else "Pending",
                  cls=(AlertT.success if contact.responded else AlertT.warning, 
                       "w-24 text-center text-sm font-medium"))
    
    header = DivFullySpaced(
        DivLAligned(
            H4(contact.name, cls=(TextT.bold, "text-lg")),
            P(contact.email, cls=(TextPresets.muted_sm, "mt-1")),
            cls="space-y-0.5"
        ),
        status
    )
    
    timestamps = DivFullySpaced(
        DivLAligned(
            UkIcon("calendar", height=16, width=16, cls="text-muted mr-2"),
            P(f"Received: {contact.created_at}", cls=TextPresets.muted_sm)
        ),
        DivLAligned(
            UkIcon("clock", height=16, width=16, cls="text-muted mr-2"),
            P(f"Responded: {contact.response_date or 'Not yet'}", 
              cls=(TextPresets.muted_sm, "text-success" if contact.responded else ""))
        )
    )
    
    actions = DivRAligned(
        Button(DivLAligned(UkIcon("trash-2", height=16, width=16, cls="mr-2"), "Delete"), 
               cls=(ButtonT.ghost, "text-destructive hover:text-destructive/90"),
               hx_delete=f'/contact/delete/{contact.id}',
               target_id=f'contact-{contact.id}',
               hx_swap="outerHTML",
               hx_confirm="Are you sure you want to delete this contact request?"),
        Button(DivLAligned(
                UkIcon("check-circle" if not contact.responded else "x-circle", 
                      height=16, width=16, cls="mr-2"),
                "Mark " + ("Pending" if contact.responded else "Responded")),
               cls=(ButtonT.primary, "ml-2"),
               hx_get=f'/contact/toggle/{contact.id}',
               target_id=f'contact-{contact.id}',
               hx_swap="outerHTML"),
        cls="mt-4"
    )
    
    return Card(header,
               Div(P(contact.message, cls=(TextT.muted, "text-sm leading-relaxed")), 
                   DividerSplit(cls="my-4"), 
                   timestamps,
                   cls="space-y-4"),
               actions,
               id=f'contact-{contact.id}',
               cls=(CardT.hover + CardT.secondary, "mb-4 p-5"))

def ContactRequests(requests):
    """Display and manage contact form submissions"""
    header = HomeSectionHeader(
        "Contact Requests",
        "Manage and respond to contact form submissions",
        None, None
    )
    
    toolbar = DivFullySpaced(
        Input(placeholder="Search requests...", 
              cls="w-64 bg-secondary border-border",
              uk_icon="icon: search"),
        UkSelect(*Options("All", "Pending", "Responded", selected_idx=0), 
                cls="w-32 ml-2 bg-secondary border-border"),
        cls="mb-6"
    )
    
    if not requests:
        return Div(header, toolbar,
            Card(DivCentered(
                UkIcon('mail', height=48, width=48, cls="text-primary/50 mb-4"),
                H3("No Contact Requests", cls=(TextT.bold, "text-xl")),
                P("When you receive contact requests, they will appear here.", 
                  cls=(TextPresets.muted_sm, "max-w-sm text-center")),
                cls="py-16"
            ), cls=(CardT.secondary, "border border-border/50")),
            cls="container mx-auto max-w-4xl px-4 py-8 space-y-6"
        )
    
    return Div(header, toolbar, *map(ContactRequestCard, requests),
              cls="container mx-auto max-w-4xl px-4 py-8 space-y-6")


def NewProjectModal():
    folder_icon = UkIcon("folder-plus", height=24, width=24, cls="text-primary mr-3")
    header_text = H3("Add New Project", cls=TextT.bold)
    
    modal_header = DivLAligned(folder_icon, header_text)

    title_input = LabelInput("Title", id="title", placeholder="Project name", uk_tooltip="A clear, concise name for your project")
    
    description_input = LabelTextArea("Description", id="description", 
                                    placeholder="Describe your project's purpose and key features",
                                    uk_tooltip="What makes this project special?")
    
    url_inputs = Grid(
        LabelInput("Project URL", id="project_url", placeholder="https://...",  icon="link", uk_tooltip="Link to live demo or deployment"),
        LabelInput("GitHub URL", id="github_url", placeholder="https://github.com/...", icon="github", uk_tooltip="Link to source code"),
        cols=2, gap=6
    )
    
    image_input = LabelInput("Image URL", id="image_url", placeholder="https://...", icon="image", uk_tooltip="A screenshot or preview image")

    status_select = LabelSelect(
        *Options("in-progress", "completed", "archived", selected_idx=0),
        label="Status",
        id="status",
        uk_tooltip="Current state of the project"
    )
    
    tags_input = LabelInput("Tags", id="tags", placeholder="python, web-development, machine-learning", 
                           uk_tooltip="Comma-separated list of technologies or categories")
    
    featured_checkbox = LabelCheckboxX(
        "Feature this project", 
        id="featured",
        name="featured",
        value="1",        # Will submit as '1' when checked
        uk_tooltip="Show this project in the featured section"
    )

    cancel_button = Button(cls=(ButtonT.secondary, "py-3 min-w-[120px]"), uk_toggle="target: #new-project-modal")(
        DivLAligned(UkIcon("x", height=20, width=20, cls="mr-2"), "Cancel", cls="px-4")
    )

    loading_icon = Loading(cls=(LoadingT.spinner + LoadingT.sm, "ml-2"), htmx_indicator=True)
    save_button = Button(cls=(ButtonT.primary, "py-3 min-w-[180px]"), submit=True)(
                    DivLAligned(UkIcon("save", height=20, width=20, cls="mr-2"), "Save Project", loading_icon, cls="px-4"))

    action_buttons = DivRAligned(cancel_button, save_button, cls="space-x-4")

    project_form = Form(
        Grid(title_input, status_select, cols=2, gap=6),
        description_input,
        url_inputs,
        image_input,
        tags_input,
        featured_checkbox,
        DivRAligned(action_buttons, cls="mt-6"),
        cls='space-y-6',
        hx_post="/api/projects/new",
        hx_trigger="submit",
        hx_on="htmx:afterRequest: UIkit.modal('#new-project-modal').hide()"
    )

    return Modal(project_form, header=(modal_header,), cls=(CardT.secondary, "w-full mx-auto"), id="new-project-modal")

def NewBlogModal():
    file_icon = UkIcon("file-text", height=24, width=24, cls="text-primary mr-3")
    modal_header = DivLAligned(file_icon, H3("Add New Blog Post", cls=TextT.bold))

    title_input = LabelInput(
        "Title", 
        id="title", 
        placeholder="Your blog post title", 
        uk_tooltip="A clear, engaging title for your post"
    )
    
    description_input = LabelTextArea(
        "Description", 
        id="description", 
        placeholder="A brief summary of your blog post",
        uk_tooltip="This will appear in preview cards and search results"
    )
    
    url_slug_input = LabelInput(
        "URL Slug", 
        id="url_slug", 
        placeholder="my-awesome-blog-post",
        uk_tooltip="The URL-friendly version of your title (e.g., my-first-post)"
    )
    
    image_input = LabelInput(
        "Image URL", 
        id="image_url", 
        placeholder="https://...", 
        icon="image", 
        uk_tooltip="Cover image for your blog post"
    )
    
    tags_input = LabelInput(
        "Tags", 
        id="tags", 
        placeholder="python, web-development, tutorial", 
        uk_tooltip="Comma-separated list of topics"
    )
    
    published_checkbox = LabelCheckboxX(
        "Publish immediately", 
        id="published",
        name="published",
        value="1",
        uk_tooltip="Uncheck to save as draft"
    )

    # Buttons
    cancel_button = Button(
        cls=(ButtonT.secondary, "py-3 min-w-[120px]"), 
        uk_toggle="target: #new-blog-modal"
    )(
        DivLAligned(
            UkIcon("x", height=20, width=20, cls="mr-2"), 
            "Cancel", 
            cls="px-4"
        )
    )

    loading_icon = Loading(
        cls=(LoadingT.spinner + LoadingT.sm, "ml-2"), 
        htmx_indicator=True
    )
    
    save_button = Button(
        cls=(ButtonT.primary, "py-3 min-w-[180px]"), 
        submit=True
    )(
        DivLAligned(
            UkIcon("save", height=20, width=20, cls="mr-2"), 
            "Save Post", 
            loading_icon, 
            cls="px-4"
        )
    )

    action_buttons = DivRAligned(
        cancel_button, 
        save_button, 
        cls="space-x-4"
    )

    blog_form = Form(
        Grid(title_input, url_slug_input, cols=2, gap=6),
        description_input,
        image_input,
        tags_input,
        published_checkbox,
        DivRAligned(action_buttons, cls="mt-6"),
        cls='space-y-6',
        hx_post="/api/blogs/new",
        hx_trigger="submit",
        hx_on="htmx:afterRequest: UIkit.modal('#new-blog-modal').hide()"
    )

    return Modal(
        blog_form, 
        header=(modal_header,), 
        cls=(CardT.secondary, "w-full mx-auto"), 
        id="new-blog-modal"
    )

def AdminLoginForm():
    return Card(
        H3("Admin Access", cls=(TextPresets.bold_sm, "mb-4 text-zinc-800 dark:text-zinc-200")),
        Form(
            P("Enter admin password to continue:", 
              cls="text-zinc-700 dark:text-zinc-300 mb-4"),
            DivLAligned(
                UkIcon("lock", height=20, cls="text-zinc-500"),
                Input(
                    type="password",
                    name="password",
                    placeholder="Admin password",
                    cls="flex-1 bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-md px-3 py-2"
                ),
                cls="gap-2 w-full"
            ),
            Button(
                "Access Admin Panel",
                cls=(ButtonT.primary, "w-full mt-4")
            ),
            hx_post="/admin/login",
            hx_target="#admin-content"
        ),
        cls="p-6 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 max-w-md mx-auto"
    )

def AdminPage(session, auth=None):
    has_admin_rights = (auth and get_user(auth).is_admin) or session.get('admin_access')
    if not has_admin_rights:
        return Div(
            H1("Admin Dashboard", 
               cls=(TextT.bold, "text-3xl mb-6 text-zinc-900 dark:text-white")),
            AdminLoginForm(),
            id="admin-content",
            cls="container mx-auto max-w-4xl p-4"
        )
    
    db_files = [
        ("Database", "personal_site.sqlite"),
        ("Write-Ahead Log", "personal_site.sqlite-wal"),
        ("Shared Memory File", "personal_site.sqlite-shm")
    ]
    
    download_buttons = [
        DivLAligned(
            UkIcon(
                "database" if name == "Database" else "file", 
                height=20, 
                cls="text-blue-500 dark:text-blue-400"
            ),
            A(
                f"Download {name}", 
                href=f"/admin/download/{filename}",
                cls="inline-flex items-center px-4 py-2 bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-md text-sm font-medium text-zinc-900 dark:text-zinc-100 hover:bg-zinc-50 dark:hover:bg-zinc-700 transition-colors"
            ),
            cls="gap-3"
        ) for name, filename in db_files
    ]

    upload_form = Form(
        P("Upload database files:", cls="text-zinc-700 dark:text-zinc-300 mb-2"),
        Input(
            type="file",
            name="database",
            multiple=True,
            accept=".sqlite,.sqlite-wal,.sqlite-shm",
            cls="mb-4 text-zinc-700 dark:text-zinc-300"
        ),
        Button(
            DivLAligned(
                UkIcon("upload", height=20),
                "Upload Files",
                Loading(cls=(LoadingT.spinner + LoadingT.sm, "ml-2"), htmx_indicator=True)
            ),
            cls=(ButtonT.primary, "mt-2")
        ),
        hx_post="/admin/upload",
        hx_encoding="multipart/form-data",
        hx_target="#upload-result"
    )

    return Div(
        H1("Admin Dashboard", 
           cls=(TextT.bold, "text-3xl mb-6 text-zinc-900 dark:text-white")),
        Grid(
            Card(
                H3("Database Management", 
                   cls=(TextPresets.bold_sm, "mb-4 text-zinc-800 dark:text-zinc-200")),
                Div(*download_buttons, cls="space-y-4"),
                cls="p-6 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800"
            ),
            Card(
                H3("Upload Database", 
                   cls=(TextPresets.bold_sm, "mb-4 text-zinc-800 dark:text-zinc-200")),
                upload_form,
                Div(id="upload-result"),
                cls="p-6 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800"
            ),
            cols=1,
            gap=6
        ),
        cls="container mx-auto max-w-4xl p-4"
    )



def CommonScreen(*c, auth=None):
    user = get_user(auth)
    return Div(
        ErikNavBar(user=user),
        *c,
        ContactModal(),
        Footer(),
        cls="min-h-screen bg-background"
    )

def Home(auth=None):
    projects = get_projects()
    blogs = get_blog_posts()
    return CommonScreen(    
        HeroSection(),
        LatestBlogs(blogs),
        ProjectsSection(projects),
        auth=auth
    )
    
def ListBlogs(auth=None):
    blogs = get_blog_posts()
    return CommonScreen(BlogPage(blogs, auth=auth), auth=auth)

def ListProjects(auth=None):
    projects = get_projects()
    return CommonScreen(ProjectPage(projects, auth=auth), auth=auth)

def BlogPostPage(post=None, auth=None, token=None):
    return CommonScreen(FullBlogPost(post=post, auth=auth, token=token), auth=auth)

def LoginPage(oauth_url, auth=None):
    return CommonScreen(LoginScreen(oauth_url), auth=auth)

def TermsOfServicePage(auth=None):
    return CommonScreen(TermsOfService(), auth=auth)

def PrivacyPolicyPage(auth=None):
    return CommonScreen(PrivacyPolicy(), auth=auth)

def ContactRequestsPage(auth=None):
    user = get_user(auth)
    requests = get_contact_requests()
    if user.is_admin: return CommonScreen(ContactRequests(requests), auth=auth)
    else:             return RedirectResponse('/', status_code=303)
