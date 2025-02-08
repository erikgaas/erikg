from monsterui.all import *
from fasthtml.common import *
from fasthtml.svg import *
from datetime import datetime

def LoginButton():
    return Button(
        DivLAligned(
            UkIcon('log-in', height=16, width=16, cls="mr-2"), 
            "Sign In", 
            cls="px-4 py-2"
        ),
        cls=(
            ButtonT.ghost, "hover:bg-muted", "hover:text-primary",
            "transition-colors duration-200", "border border-border/50", "rounded-full","min-w-[100px]")
    )

def MobileMenu(nav_items):
    return Modal(
        NavContainer(*nav_items, cls="space-y-4"),
        id="mobile-menu",
        cls="uk-modal-full",
        dialog_cls="uk-modal-dialog uk-margin-remove-top"  # Align to top
    )

def ErikNavBar():
    login_btn = LoginButton()
    theme_toggle = Button(
        Div(
            Div(UkIcon('sun', height=16, width=16), cls="absolute dark:hidden"),
            Div(UkIcon('moon', height=16, width=16), cls="absolute hidden dark:block"),
            cls="relative w-4 h-4" 
        ),
        cls=ButtonT.secondary,
        uk_toggle="target: html; cls: dark"
    )
    
    social_icons = DivHStacked(
        UkIconLink('github', href="https://github.com/erikgaas", height=20),
        UkIconLink('linkedin', href="https://www.linkedin.com/in/erikgaas/", height=20),
        UkIconLink('twitter', href="https://x.com/erikgaas", height=20),
        cls="space-x-4 hidden sm:flex"
    )
    
    nav_items = [
        Li(A("About", href="/")),
        Li(A("Projects", href="/projects")),
        Li(A("Blog", href="/blogposts")),
        Li(A("Contact"), uk_toggle="target: #contact-modal")
    ]
    
    mobile_menu = Button(
        UkIcon('menu', height=24, width=24),
        cls=(ButtonT.ghost, "sm:hidden"),
        uk_toggle="target: #mobile-menu"
    )
    
    return Div(
        NavBarContainer(
            NavBarLSide(A(H3("Erik Gaasedelen", cls="mr-6"), href="/"), NavBarNav(*nav_items, cls="hidden sm:flex")),
            NavBarRSide(social_icons, theme_toggle, login_btn, mobile_menu, cls="space-x-4"),
            cls="border-b border-border px-4 py-2"
        ),
        MobileMenu(nav_items)
    )


def HeroSection():
    def SocialButton(icon, href, text):
        return Button(
            DivLAligned(
                UkIcon(icon, height=24, width=24, cls="mr-3"), 
                text,
                cls="px-2"
            ),
            cls=(ButtonT.secondary, "py-3 w-full sm:w-auto"),  # Full width on mobile
            href=href
        )

    social_buttons = Div(  # Changed to Div for better mobile control
        SocialButton("github", "https://github.com/erikgaas", "GitHub"),
        SocialButton("linkedin", "https://www.linkedin.com/in/erikgaas", "LinkedIn"),
        SocialButton("file-text", "#", "Resume"),
        cls="space-y-3 sm:space-y-0 sm:flex sm:space-x-6 w-full"  # Stack vertically on mobile
    )

    return Card(
        Div(  # Wrapper div with flex column on mobile, row on desktop
            Div(  # Profile image container
                Img(
                    src="https://picsum.photos/400/400?random=1",
                    alt="Profile Picture",
                    cls="rounded-full w-32 h-32 sm:w-48 sm:h-48 object-cover shadow-lg mx-auto sm:mx-0"  # Centered on mobile
                ),
                cls="mb-6 sm:mb-0 sm:mr-8"
            ),
            Div(  # Content container
                H1("Erik Gaasedelen", cls=TextT.bold + TextT.primary + "text-center sm:text-left"),
                P("Senior Engineering Manager", cls=TextT.lg + TextT.muted + "text-center sm:text-left"),
                P("""Fullstack, Deep Learning, Autonomous Vehicles, Med Tech. Trying to make hard problems easier.""",
                  cls=TextT.muted + "text-center sm:text-left"),
                DividerSplit(),
                Div(  # Button container
                    social_buttons,
                    Button(
                        DivLAligned(
                            UkIcon("mail", height=24, width=24, cls="mr-3"),
                            "Get in touch",
                            cls="px-4", 
                        ),
                        cls=(ButtonT.primary, "py-3 w-full sm:w-auto sm:min-w-[180px] mt-3 sm:mt-0", "text-lg"),
                        uk_toggle="target: #contact-modal"
                    ),
                    cls="flex flex-col sm:flex-row sm:justify-between items-center space-y-3 sm:space-y-0"
                ),
                cls='space-y-4'
            ),
            cls="flex flex-col sm:flex-row items-center sm:items-start text-center sm:text-left"
        ),
        cls=(CardT.secondary, "mt-8 mx-auto max-w-4xl p-8"))



def BlogCard(blog):
    """Create a preview card for a single blog post"""
    image_section = Div(cls="relative")(Img(src=blog.image_url, alt=blog.title, cls="object-cover w-full h-48"))
    metadata = DivLAligned(cls="space-x-4")(
                            DivHStacked(
                                UkIcon("calendar", height=16, width=16),
                                P(blog.created_at, cls=TextPresets.muted_sm),
                                cls="space-x-2"
                            ),
                            DivHStacked(cls="space-x-2")(UkIcon("eye", height=16, width=16),
                                                        P(f"{blog.views} views", cls=TextPresets.muted_sm))
    )
    
    title_section = Div(cls="space-y-2")(H3(blog.title, cls=TextT.bold), metadata)
    description = P(blog.description, cls=TextPresets.muted_sm)
    tags = Div(cls="flex flex-wrap gap-2")(*[Label(tag.strip(), cls=LabelT.secondary) 
                                            for tag in blog.tags.split(',') if tag.strip()])
    
    read_more = A(
        DivLAligned(
            "Read more",
            UkIcon("arrow-right", height=16, width=16, cls="ml-2"),
        ),
        href=f"/blog/{blog.url_slug}",
        cls=(AT.muted, TextPresets.bold_sm)
    )
    content_section = Div(title_section, description, tags, read_more, cls="space-y-4 p-6")
    return Card(image_section, content_section, cls=(CardT.hover + CardT.secondary, "max-w-sm"))

def HomeSectionHeader(title, description, button_text, button_href):
    view_all_btn = Button(
        DivLAligned(button_text, UkIcon("arrow-right", height=16, width=16), cls="px-4 py-2"),
        cls=(ButtonT.secondary, "hover:shadow-md", "transition-all duration-200", "border border-border", "min-w-[160px]"))

    header = DivFullySpaced(
        Div(
            H2(title, cls=(TextT.bold, "text-2xl")),
            P(description, cls=(TextPresets.muted_sm, "mt-2")),
            cls="space-y-1"
        ),
        view_all_btn, cls="items-center"
    )
    return header

def LatestBlogs(blogs):
    """Create a section displaying the latest blog posts"""
    header = HomeSectionHeader("Latest Posts", "Check out my latest thoughts and tutorials", "View all posts", "/blogposts")    
    blog_grid = Div(cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8 justify-items-center")(
        *[BlogCard(blog) for blog in blogs]
    )
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
    modal_header = DivLAligned(
            UkIcon("mail", height=24, width=24, cls="text-primary mr-3"), H3("Get in Touch", cls=TextT.bold)
        )

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

    name_input = Div(
        LabelInput("Name", id="name",  placeholder="Your name", icon="user",uk_tooltip="Please enter your full name")
    )

    email_input = Div(
        LabelInput("Email", id="email", type="email", placeholder="your.email@example.com", icon="mail",
                   uk_tooltip="I'll use this to respond to your message"
        )
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
            id="subscribe", 
            cls="text-sm",
            input_cls="bg-primary hover:bg-primary-focus border-primary"  # Added primary color classes
        )
    )

    cancel_button = Button(
        DivLAligned(
            UkIcon("x", height=20, width=20, cls="mr-2"), 
            "Cancel",
            cls="px-4"
        ),
        cls=(ButtonT.secondary, "py-3 min-w-[120px]"), 
        uk_toggle="target: #contact-modal"
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
    social_links = [
        ("github", "https://github.com/erikgaas"),
        ("linkedin", "https://www.linkedin.com/in/erikgaas"),
        ("twitter", "https://x.com/erikgaas"),
    ]
    
    social_icons = DivHStacked(
        *[UkIconLink(icon, href=url, height=20, cls="text-gray-300 hover:text-primary transition-colors")
          for icon, url in social_links],
        cls="space-x-6"
    )
    
    return Section(
        DivVStacked(
            DividerSplit(),
            DivCentered(
                social_icons,
                P(f"© {datetime.now().year} Erik Gaasedelen. All rights reserved.", 
                  cls=TextPresets.muted_sm),
                cls="space-y-4 py-8"
            )
        ),
        cls="mt-auto"
    )

def BlogToolbar(tags, active_tag=None, sort_by="newest"):
    search_input = Div(
        Input(
            placeholder="Search posts...",
            cls="w-full sm:w-[300px] bg-secondary border-border text-secondary-foreground hover:bg-secondary/80 focus:bg-secondary/80",
            uk_icon="icon: search"
        ),
        cls="flex-grow sm:flex-grow-0"
    )
    
    sort_options = [
        ("newest", "Newest First"),
        ("oldest", "Oldest First"),
        ("popular", "Most Popular"),
        ("updated", "Recently Updated")
    ]
    
    sort_dropdown = UkSelect(
        *[Option(label, value=value, selected=(value==sort_by))
          for value, label in sort_options],
        cls="w-[200px]",
        placeholder="Sort by"
    )
    
    # Create tag pills that act as toggleable filters
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
        tag_filters,
        cls="space-y-4 mb-8"
    )


def BlogPage(blogs):
    # Extract unique tags from all blogs
    all_tags = set()
    for blog in blogs:
        all_tags.update(tag.strip() for tag in blog.tags.split(','))
    
    header = DivFullySpaced(
        Div(
            H1("Blog", cls=(TextT.bold + TextT.primary, "text-3xl")),
            P("Thoughts, tutorials, and insights", cls=TextPresets.muted_sm),
            cls="space-y-2"
        ),
    )
    
    toolbar = BlogToolbar(sorted(all_tags))
    
    # Updated grid to match home page layout
    blog_grid = Div(
        cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8 justify-items-center"
    )(*[BlogCard(blog) for blog in blogs])

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