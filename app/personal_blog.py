from monsterui.all import *
from fasthtml.common import *
from ghapi.all import GhApi
from app.api import *
import dotenv

dotenv.load_dotenv()

def PY(*c, **kwargs):
    curr_cls = kwargs.pop("cls", TextT.secondary + TextT.lg + TextT.muted)
    return P(*c, cls=curr_cls, **kwargs)

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

def GithubInsights(auth=None, token=None):
    gh_icon = UkIcon("github", height=24, cls="text-primary")
    login_cta = Div(
        H4("GitHub Insights", cls=TextPresets.bold_sm),
        P("Log in with GitHub to see your personalized stats!", cls=TextPresets.muted_sm)
    )
    not_logged_in = Card(DivLAligned(gh_icon, login_cta, cls="gap-4"), cls="p-6 my-8")
    if not auth: return not_logged_in

    def get_user_stats(username):
        api = GhApi(token=token)
        user = api.users.get_by_username(username)

        repos = api.repos.list_for_user(username)
        langs = {}
        for repo in repos[:5]:
            if repo.language:
                langs[repo.language] = langs.get(repo.language, 0) + 1

        top_langs = sorted(langs.items(), key=lambda x: x[1], reverse=True)[:3]

        return {
            'repos': user.public_repos,
            'followers': user.followers,
            'following': user.following,
            'created_at': user.created_at[:10],
            'top_languages': top_langs
        }
    
    try:
        user = get_user(auth)
        stats = get_user_stats(user.username)

        profile_header = DivLAligned(
            gh_icon,
            H4("Your GitHub Profile", cls=TextPresets.bold_sm),
            cls="gap-4 mb-4"
        )

        stat_counters = [
            DivVStacked(
                P(label, cls=TextPresets.muted_sm),
                H3(str(stats[key]), cls=TextT.bold)
            )
            for label, key in [
                ("Public Repos", 'repos'),
                ("Followers", 'followers'),
                ("Following", 'following')
            ]
        ]
        
        stats_grid = Grid(*stat_counters, cols=3, gap=4)
        
        language_labels = DivHStacked(cls="gap-2 mt-2")(
            *[Label(f"{lang} ({count})", cls=LabelT.primary) 
              for lang, count in stats['top_languages']],
        )

        languages_section = Div(H4("Top Languages", cls=TextPresets.bold_sm), language_labels)
        member_since = P(f"GitHub member since {stats['created_at']}", cls=(TextPresets.muted_sm, "mt-4"))
        
        return Card(profile_header, stats_grid, DividerSplit(), languages_section, member_since, cls="p-6 my-8")
    except Exception as e:
        alert_icon = UkIcon("alert-triangle")
        alert_text = P("Unable to fetch GitHub stats at the moment.", cls="text-white")
        error_alert = Alert(DivLAligned(alert_icon, alert_text), cls=AlertT.warning)
        return Card(error_alert, cls="p-6 my-8")
    
def BuildPersonalSiteBlogPost(auth=None, token=None):
    sections = [
        ("Making solo webapp development possible", "intro"),
        ("Removing Barriers", "barriers"),
        ("Truly Dynamic Content", "dynamic"),
        ("Resources and Getting Started", "resources")
    ]
    
    intro = Section(
        H1("Making solo webapp development possible", cls=(TextT.lg + TextT.muted + TextT.primary, "text-3xl mb-6")),
        PY("I've never been as productive building a webapp as I am now. This entire blog runs on my personal site, built with FastHTML and MonsterUI. I've tried many leading frontend frameworks over the years, only to get bogged down by their complexity."),
        Br(),
        PY("Before this, my go-to stack was FastAPI and React—yet even adding a third-party OAuth login felt like an all-day affair. The tools themselves are powerful; it's the sprawling ecosystems that overwhelmed me as a solo developer wanting a full-featured app: database, business logic, and a customizable UI."),
        Br(),
        PY("Then I discovered FastHTML and MonsterUI. Yes, they're more frameworks you might not have heard of—but here's why they're worth a look. Simply put, this site is the first time I've built exactly what I envisioned: it has databases, authentication, contact forms, mobile responsiveness, and theme support. Getting here with other stacks took far too much time, if it ever happened at all. Now, I'm excited to share how straightforward it can be once you have the right tools in hand. If I can do this, so can you."),
        id="intro",
        cls="mb-12"
    )
    
    barriers = Section(
        H2("Removing Barriers", cls=(TextT.lg + TextT.muted + TextT.primary, "text-2xl mb-4")),
        PY("What does a \"barrier\" look like in practice? Let's walk through a simple scenario—displaying blog post cards—to see how FastHTML compares to a standard FastAPI and React setup."),
        Br(),
        PY("Consider a basic example: displaying blog post cards. With FastAPI, you typically write an endpoint returning JSON:"),
        CodeBlock("""@app.get("/api/blogs")
    async def get_blogs():
        return [
            {
                "title": "Making solo webapp development possible",
                "description": "Building modern web apps without the complexity...",
                "created_at": "2024-01-20T10:00:00",
                "views": 142,
                "tags": ["python", "web-development", "tutorial"]
            }
            # ... more blog posts
        ]""", language="python"),
        PY("Then you'd transform that JSON into HTML in React:"),
        CodeBlock("""function BlogCard({ blog }) {
    return (
        <div className="card">
        <h3>{blog.title}</h3>
        <p>{blog.description}</p>
        <div className="metadata">
            <span>{formatDate(blog.created_at)}</span>
            <span>{blog.views} views</span>
        </div>
        <div className="tags">
            {blog.tags.map((tag) => (
            <span key={tag} className="tag">
                {tag}
            </span>
            ))}
        </div>
        </div>
    );
    }

    function BlogList() {
    const [blogs, setBlogs] = useState([]);

    useEffect(() => {
        fetch("/api/blogs")
        .then((res) => res.json())
        .then((data) => setBlogs(data));
    }, []);

    return (
        <div className="blog-grid">
        {blogs.map((blog) => (
            <BlogCard key={blog.id} blog={blog} />
        ))}
        </div>
    );
    }""", code_cls="language-javascript"),
        PY("With FastHTML, you skip the JSON step and directly return styled HTML:"),
        CodeBlock("""@rt("/blogposts")
    def blogs(auth):
        posts = get_blog_posts()
        return Div(
            *[BlogCard(blog) for blog in posts],
            cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        )

    def BlogCard(blog):
        return Card(
            PostTags(blog.tags),
            H3(blog.title, cls=TextT.bold),
            P(blog.description, cls=TextPresets.muted_sm),
            DivLAligned(
                PostMetrics(blog.content, blog.views),
                cls="justify-between items-center"
            ),
            cls=CardT.hover + CardT.secondary
        )""", language="python"),
        PY("Combined with HTMX, FastHTML can serve a full page or just the snippet needed to update an existing page section. Whether you're loading more posts or filtering by tag, FastHTML returns new cards on demand—no JSON conversion, no separate state management, no extra styling system. You simply define the HTML in Python and let HTMX slot it right into place."),
        id="barriers",
        cls="mb-12"
    )
    
    dynamic = Section(
        H2("Truly Dynamic Content", cls=(TextT.lg + TextT.muted + TextT.primary, "text-2xl mb-4")),
        PY("\"Why not just use Medium or another blogging platform?\" They do handle plenty of complexity, but they also limit your options. With FastHTML, you can add truly interactive components that go beyond any preset template."),
        Br(),
        PY("For example, I recently added a dynamic GitHub insights panel to my posts. It's not just static text—it queries GitHub live and returns up-to-date information. Try doing that on Medium! Because FastHTML lets you embed any custom component, you can drop in code playgrounds, real-time data visualizations, or personalized recommendations right alongside your written content."),
        Br(),
        PY("That's where FastHTML really shines: it's not just about making simple development easier, but about bringing once-complex features within reach. The same component system that handles basic blog posts can also power complex, dynamic, authenticated content without getting in your way."),
        id="dynamic",
        cls="mb-12"
    )
    
    resources = Section(
        H2("Resources and Getting Started", cls=(TextT.lg + TextT.muted + TextT.primary, "text-2xl mb-4")),
        PY("My entire personal site is on GitHub if you want a working example:"),
        Br(),
        PY(A("github.com/erikgaas/erikg", href="https://github.com/erikgaas/erikg/tree/main", cls=AT.primary)),

        H3("1. Explore MonsterUI Components", cls=(TextT.bold + TextT.muted + TextT.primary, "text-xl mt-8 mb-4")),
        PY("Start with ", 
        A("MonsterUI", href="https://monsterui.answer.ai/", cls=AT.primary),
        ". There you will get a lot of inspiration for what is possible with a very small amount of code. The styling is based on FrankenUI, DaisyUI, and TailwindCSS, so it is all based on state of the art technology."),
        
        H3("2. Learn FastHTML Basics", cls=(TextT.bold + TextT.muted + TextT.primary, "text-xl mt-8 mb-4")),
        PY("Check out the ", 
        A("FastHTML documentation", href="https://docs.fastht.ml/", cls=AT.primary),
        ". Don't forget to explore the ",
        A("examples", href="https://github.com/AnswerDotAI/fasthtml/tree/main/examples", cls=AT.primary),
        ". There is even an additional separate repo with ",
        A("advanced features", href="https://github.com/AnswerDotAI/fasthtml-example", cls=AT.primary),
        ". One really important tip is to take these examples and add them as context to your favorite AI assistant. Just be cautious of hallucinations."),
        
        H3("3. Understand HTMX", cls=(TextT.bold + TextT.muted + TextT.primary, "text-xl mt-8 mb-4")),
        PY(A("HTMX", href="https://htmx.org/", cls=AT.primary),
        " powers FastHTML's seamless updates. While you don't need to be an HTMX expert to use FastHTML, understanding its principles will help you build more sophisticated applications."),
        Br(),
        PY("I really enjoyed watching this ",
        A("conversation", href="https://www.youtube.com/watch?v=WuipZMUch18", cls=AT.primary),
        " between FastHTML creator Jeremy Howard and HTMX creator Carson Gross. For an even deeper dive, check out ",
        A("Hypermedia Systems", href="https://hypermedia.systems/", cls=AT.primary),
        " to understand the underlying philosophy."),
        
        Alert(
            DivLAligned(
                UkIcon("info", cls="text-white"), 
                Div(
                    H4("Ready to start building?", cls="text-white"),
                    PY("Feel free to reach out if you have questions or want to share what you're building!", 
                    cls="text-white")
                )
            ),
            cls=(AlertT.info, "mt-8")
        ),
        
        id="resources",
        cls="mb-12"
    )
    
    gh_integration = GithubInsights(auth=auth, token=token)
    
    content = Div(intro, barriers, dynamic, gh_integration, resources, cls="prose max-w-none")
    
    return Div(
        TableOfContents(sections),
        content,
        cls="container mx-auto max-w-3xl px-4 py-8 relative"
    )
