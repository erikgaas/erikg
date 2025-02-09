from monsterui.all import *
from fasthtml.common import *
from fasthtml.svg import *
from datetime import datetime

def LoginButton():
    return Button(cls=(ButtonT.ghost, "hover:bg-muted", "hover:text-primary","transition-colors duration-200", "border border-border/50", "rounded-full","min-w-[100px]"))(
        DivLAligned(UkIcon('log-in', height=16, width=16, cls="mr-2"),  "Sign In",  cls="px-4 py-2"),
    )

def MobileMenu(nav_items):
    return Modal(id="mobile-menu", cls="uk-modal-full", dialog_cls="uk-modal-dialog uk-margin-remove-top")(NavContainer(*nav_items, cls="space-y-4"))

def ErikNavBar():
    login_btn = LoginButton()
    sun_icon, moon_icon = UkIcon('sun', height=16, width=16), UkIcon('moon', height=16, width=16)
    icon_group = Div(cls="relative w-4 h-4")(Div(sun_icon, cls="absolute dark:hidden"), Div(moon_icon, cls="absolute hidden dark:block"))
    theme_toggle = Button(cls=ButtonT.secondary, uk_toggle="target: html; cls: dark")(icon_group)

    social_icons = DivHStacked(cls="space-x-4 hidden sm:flex")(
        UkIconLink('github', href="https://github.com/erikgaas", height=20),
        UkIconLink('linkedin', href="https://www.linkedin.com/in/erikgaas/", height=20),
        UkIconLink('twitter', href="https://x.com/erikgaas", height=20),  
    )

    nav_items = [Li(A("About", href="/")), Li(A("Projects", href="/projects")), Li(A("Blog", href="/blogposts")), Li(A("Contact"), uk_toggle="target: #contact-modal")]
    mobile_menu = Button(UkIcon('menu', height=24, width=24), cls=(ButtonT.ghost, "sm:hidden"), uk_toggle="target: #mobile-menu")

    left_nav  = NavBarLSide(A(H3("Erik Gaasedelen", cls="mr-6"), href="/"), NavBarNav(*nav_items, cls="hidden sm:flex"))
    right_nav = NavBarRSide(social_icons, theme_toggle, login_btn, mobile_menu, cls="space-x-4")

    return Div(NavBarContainer(left_nav, right_nav, cls="border-b border-border px-4 py-2"), MobileMenu(nav_items))


def HeroSection():
    def SocialButton(icon, href, text):
        return A(href=href, cls=(ButtonT.secondary, "py-3 w-full sm:w-auto inline-flex"))(
            DivLAligned(UkIcon(icon, height=24, width=24, cls="mr-3"), text, cls="px-2")
        )
    
    social_icons = [("github", "https://github.com/erikgaas", "GitHub"), ("linkedin", "https://www.linkedin.com/in/erikgaas", "LinkedIn"), ("file-text", "#", "Resume")]
    social_buttons = [SocialButton(icon, href, text) for icon, href, text in social_icons]
    social_buttons = Div(*social_buttons,cls="space-y-3 sm:space-y-0 sm:flex sm:space-x-6 w-full")
    name = H1("Erik Gaasedelen", cls=TextT.bold + TextT.primary + "text-center sm:text-left")
    title = P("Senior Engineering Manager", cls=TextT.lg + TextT.muted + "text-center sm:text-left")
    about = P("""Fullstack, Deep Learning, Autonomous Vehicles, Med Tech. Trying to make hard problems easier.""", cls=TextT.muted + "text-center sm:text-left")
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
    published = DivHStacked(UkIcon("calendar", height=16, width=16), P(blog.created_at, cls=TextPresets.muted_sm), cls="space-x-2")
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
        Div(H2(title, cls=(TextT.bold, "text-2xl")), P(description, cls=(TextPresets.muted_sm, "mt-2")), cls="space-y-1"),
        view_all_btn, cls="items-center"
    )
    return header

def LatestBlogs(blogs):
    """Create a section displaying the latest blog posts"""
    header = HomeSectionHeader("Latest Posts", "Check out my latest thoughts and tutorials", "View all posts", "/blogposts")    
    blog_grid = Div(cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8 justify-items-center")(*[BlogCard(blog) for blog in blogs])
    return Section(header, blog_grid, cls="mt-16 mx-auto max-w-6xl px-4")

# Let's create some sample blog posts
sample_blogs = [
    SimpleNamespace(
        title="Building a Personal Website with MonsterUI",
        description="A deep dive into creating a modern, responsive personal website using Python and MonsterUI framework.",
        image_url="https://picsum.photos/800/400?random=1",
        created_at="July 24, 2024",
        views=142,
        tags="python,web-development,tutorial",
        url_slug="building-personal-website-monsterui"
    ),
    SimpleNamespace(
        title="Machine Learning in Production",
        description="Best practices for deploying and monitoring machine learning models in production environments.",
        image_url="https://picsum.photos/800/400?random=2",
        created_at="July 22, 2024",
        views=98,
        tags="machine-learning,devops,python",
        url_slug="ml-in-production"
    ),
    SimpleNamespace(
        title="The Future of Autonomous Vehicles",
        description="Exploring recent developments in self-driving technology and what the future might hold.",
        image_url="https://picsum.photos/800/400?random=3",
        created_at="July 20, 2024",
        views=215,
        tags="autonomous-vehicles,technology,future",
        url_slug="future-of-av"
    )
]

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

    subscribe_checkbox = Div(
        LabelCheckboxX(
            "Keep me updated about new blog posts and projects", 
            id="subscribe", cls="text-sm", input_cls="bg-primary hover:bg-primary-focus border-primary")
    )

    cancel_button = Button(cls=(ButtonT.secondary, "py-3 min-w-[120px]"), uk_toggle="target: #contact-modal")(
        DivLAligned(UkIcon("x", height=20, width=20, cls="mr-2"), "Cancel", cls="px-4")
    )

    send_button = Button(
        DivLAligned(
            UkIcon("send", height=20, width=20, cls="mr-2"),
            "Send Message",
            Loading(cls=(LoadingT.spinner + LoadingT.sm, "ml-2"), htmx_indicator=True),
            cls="px-4"
        ), 
        cls=(ButtonT.primary, "py-3 min-w-[180px]")
    )

    action_buttons = DivRAligned(cancel_button, send_button, cls="space-x-4")
    contact_form = Form(Grid(name_input, email_input, cols=2, gap=6),message_input, subscribe_checkbox, cls='space-y-6')

    return Modal(alert, contact_form, header=(modal_header, ), footer=(action_buttons),
                 cls=(CardT.secondary, "w-full mx-auto"), id="contact-modal")

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

sample_projects = [
    SimpleNamespace(
        title="AutoML Platform",
        description="An end-to-end machine learning platform for automated model training and deployment.",
        image_url="https://picsum.photos/800/400?random=4",
        project_url="https://github.com/username/automl",
        github_url="https://github.com/username/automl",
        status="completed",
        featured=True,
        tags="python,machine-learning,docker"
    ),
    SimpleNamespace(
        title="Autonomous Navigation System",
        description="Real-time path planning and obstacle avoidance system for autonomous vehicles.",
        image_url="https://picsum.photos/800/400?random=5",
        project_url="https://github.com/username/nav-system",
        github_url="https://github.com/username/nav-system",
        status="in-progress",
        featured=True,
        tags="robotics,c++,ros"
    ),
    SimpleNamespace(
        title="Medical Image Analysis",
        description="Deep learning models for automated medical image analysis and diagnosis.",
        image_url="https://picsum.photos/800/400?random=6",
        project_url="https://github.com/username/med-image",
        github_url="https://github.com/username/med-image",
        status="completed",
        featured=True,
        tags="deep-learning,healthcare,python"
    )
]

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


def BlogPage(blogs):
    all_tags = set()
    for blog in blogs: all_tags.update(tag.strip() for tag in blog.tags.split(','))
    
    header = DivFullySpaced(
        Div(
            H1("Blog", cls=(TextT.bold + TextT.primary, "text-3xl")),
            P("Thoughts, tutorials, and insights", cls=TextPresets.muted_sm),
            cls="space-y-2"
        ),
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

    return Div(header, toolbar, blog_grid, pagination, cls="container mx-auto max-w-6xl px-4 py-8 space-y-8")

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
    
    return Div(
        DivFullySpaced(search_input, sort_dropdown, cls="flex-wrap gap-4"),
        Div(
            H4("Status", cls=TextPresets.bold_sm),
            status_filters,
            cls="space-y-2"
        ),
        Div(
            H4("Technologies", cls=TextPresets.bold_sm),
            tag_filters,
            cls="space-y-2"
        ),
        cls="space-y-6 mb-8"
    )

def ProjectPage(projects):
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
        )
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

    return Div(header, toolbar, project_grid, pagination, 
              cls="container mx-auto max-w-6xl px-4 py-8 space-y-8")

more_sample_projects = sample_projects + [
    SimpleNamespace(
        title="Personal Finance Dashboard",
        description="Interactive dashboard for tracking personal finances and investments.",
        image_url="https://picsum.photos/800/400?random=7",
        project_url="https://github.com/username/finance-dash",
        github_url="https://github.com/username/finance-dash",
        status="in-progress",
        featured=False,
        tags="python,react,finance"
    ),
    SimpleNamespace(
        title="Smart Home Controller",
        description="IoT system for managing home automation devices.",
        image_url="https://picsum.photos/800/400?random=8",
        project_url="https://github.com/username/smart-home",
        github_url="https://github.com/username/smart-home",
        status="archived",
        featured=False,
        tags="python,iot,raspberry-pi"
    )
]

def TableOfContents(sections):
    def create_toc_link(text, id):
        return Li(A(text, href=f"#{id}"), cls=TextPresets.muted_sm)
    
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
def BlogPost():
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
    
    # Create the layout with TOC on the left and content on the right
    return Div(
        TableOfContents(sections),
        content,
        cls="container mx-auto max-w-3xl px-4 py-8 relative"  # Narrower max-width to allow space for TOC
    )

def estimate_read_time(text, words_per_minute=200):
    """Estimate reading time in minutes"""
    word_count = len(text.split())
    minutes = max(1, round(word_count / words_per_minute))
    return f"{minutes} min read"

def BlogPostHeader(post):
    return Section(
        # Tags
        Div(*[Label(tag.strip(), cls=LabelT.secondary) for tag in post.tags.split(',')],
            cls="flex flex-wrap gap-2 mb-4"),
        
        # Title
        H1(post.title, cls=(TextT.bold, "text-4xl mb-6")),
        
        # Author and metadata
        DivLAligned(
            # Author info
            DivLAligned(
                DiceBearAvatar(post.author_name, h=10, w=10),
                Div(
                    P(post.author_name, cls=TextPresets.bold_sm),
                    P(post.created_at, cls=TextPresets.muted_sm)
                ),
                cls="gap-3"
            ),
            
            # Reading time and views
            DivLAligned(
                DivHStacked(UkIcon("clock", height=16), 
                           P(estimate_read_time(post.content), cls=TextPresets.muted_sm)),
                DivHStacked(UkIcon("eye", height=16), 
                           P(f"{post.views} views", cls=TextPresets.muted_sm)),
                cls="gap-4"
            ),
            cls="justify-between items-center"
        ),
        
        # Share buttons
        Div(
            H4("Share this post", cls=TextPresets.bold_sm),
            DivHStacked(
                *[Button(UkIcon(icon), cls=ButtonT.ghost) 
                  for icon in ["twitter", "linkedin", "facebook", "link"]],
                cls="gap-2"
            ),
            cls="mt-6"
        ),
        
        DividerSplit(),
        cls="mb-8"
    )

def BlogPostNavigation(prev_post=None, next_post=None):
    return Section(
        DividerSplit(),
        DivFullySpaced(
            # Previous post
            Div(cls="flex-1") if not prev_post else (
                A(DivLAligned(
                    UkIcon("arrow-left", height=20),
                    Div(
                        P("Previous", cls=TextPresets.muted_sm),
                        P(prev_post.title, cls=TextPresets.bold_sm)
                    ),
                    cls="gap-2"
                ), href=f"/blog/{prev_post.url_slug}")
            ),
            
            # Back to posts
            Button(
                DivLAligned(UkIcon("list"), "All posts"),
                href="/blog",
                cls=ButtonT.secondary
            ),
            
            # Next post
            Div(cls="flex-1") if not next_post else (
                A(DivRAligned(
                    Div(
                        P("Next", cls=TextPresets.muted_sm),
                        P(next_post.title, cls=TextPresets.bold_sm),
                        cls="text-right"
                    ),
                    UkIcon("arrow-right", height=20),
                    cls="gap-2"
                ), href=f"/blog/{next_post.url_slug}")
            ),
        ),
        cls="mt-12"
    )

def FullBlogPost():
    # Sample post data
    post = SimpleNamespace(
        title="Building a Personal Website with MonsterUI",
        author_name="Erik Gaasedelen",
        created_at="July 24, 2024",
        content="Lorem ipsum " * 1000,  # Long content for scrolling
        views=142,
        tags="python,web-development,tutorial",
        url_slug="building-personal-website-monsterui"
    )
    
    # Sample navigation posts
    prev_post = SimpleNamespace(
        title="Introduction to FastAPI",
        url_slug="intro-to-fastapi"
    )
    next_post = SimpleNamespace(
        title="Advanced Python Tips",
        url_slug="advanced-python-tips"
    )
    
    sections = [
        ("Introduction", "introduction"),
        ("Getting Started", "getting-started"),
        ("Core Concepts", "core-concepts"),
        ("Advanced Features", "advanced-features"),
        ("Best Practices", "best-practices"),
        ("Conclusion", "conclusion")
    ]
    
    return Div(
        BlogPostHeader(post),
        BlogPost(),  # Reusing our previous BlogPost component
        BlogPostNavigation(prev_post, next_post),
        cls="container mx-auto max-w-3xl px-4 py-8"
    )

def CommonScreen(*c):
    return Div(
        ErikNavBar(),
        *c,
        ContactModal(),
        Footer(),
        cls="min-h-screen bg-background"
    )

def Home():
    return CommonScreen(    
        HeroSection(),
        LatestBlogs(sample_blogs),
        ProjectsSection(sample_projects),
    )
    
def ListBlogs():
    return CommonScreen(BlogPage(sample_blogs))

def ListProjects():
    return CommonScreen(ProjectPage(sample_projects))

def BlogPostPage():
    return CommonScreen(FullBlogPost())
