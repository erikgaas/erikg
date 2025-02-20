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
        ("Reducing Integration Costs", "integration"),
        ("The Power of HTMX", "htmx"),
        ("Styling with MonsterUI", "styling"),
        ("Truly Dynamic Content", "dynamic"),
        ("Resources and Getting Started", "resources")
    ]
    
    intro = Section(
        H1("Making solo webapp development possible", cls=(TextT.lg + TextT.muted + TextT.primary, "text-3xl mb-6")),
        PY("If you're like me, you have a graveyard of personal projects that you started but never finished. It's not the end of the world—I've learned a lot from unfinished work—but it's not always satisfying. Recently, I wanted to change that, so I dove deep into React, FastAPI, AWS, and Terraform. Again, I learned a ton, but touching every part of a full-stack app meant that nothing was great, especially web styling. I can try to learn flexbox over and over, yet it never seems to stick in my brain."),
        Br(),
        PY("Full-stack development with this stack also takes forever. I remember spending five hours just figuring out how to implement third-party OAuth sign-in. Fortunately, there's a much better way, and I'm very excited to share it with you."),
        Br(),
        PY("This entire site is built with FastHTML and MonsterUI—two relatively new libraries that make full-stack web app development a breeze. Take this site as an example: it has a database, authentication, contact forms, mobile responsiveness, and light/dark mode—far more than I ever dreamed of implementing in my own project. And, of course, blog support!"),
        Br(),
        PY("It still required effort, but I built all of this in about two weeks of evening work and some weekend free time. I shouldn't have been able to make something like this myself in such a short period. 😄 If I can do it, you can too. There's so much to cover, but let's start with a high-level look at what FastHTML and MonsterUI are and why they make me so much more productive."),
        id="intro",
        cls="mb-12"
    )
    
    integration = Section(
        H2("Reducing Integration Costs", cls=(TextT.lg + TextT.muted + TextT.primary, "text-2xl mb-4")),
        PY("On my front page, you can see cards displaying the latest blog posts. These query the database and fill in relevant information. In FastAPI, you would typically do something like this to return JSON:"),
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
        PY("A React app would then consume this JSON payload and transform it into HTML:"),
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
}""", code_cls="language-javascript"),
        PY("But what if you could skip this conversion step and return the HTML directly? That's exactly what FastHTML does:"),
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
        PY("Notice how conveniently DOM elements map to Python classes. In the blogs router, I query the database and feed the posts directly into BlogCard objects using list comprehension. Since components are just Python functions, my code is far more modular and, in my opinion, easier to maintain."),
        id="integration",
        cls="mb-12"
    )

    htmx = Section(
        H2("The Power of HTMX", cls=(TextT.lg + TextT.muted + TextT.primary, "text-2xl mb-4")),
        PY("The secret sauce behind FastHTML is HTMX. If you looked at the code above and wondered, \"What happens when these DOM elements are returned from a router?\"—the answer is HTMX. This library allows DOM elements to make HTTP requests to these endpoints and decide how to handle the returned data (e.g., replacing elements, adding children, etc.)."),
        Br(),
        PY("I've also noticed that all my state management naturally ends up in backend code, making it much easier to track. React often tripped me up when state became too complex to handle effectively."),
        id="htmx",
        cls="mb-12"
    )
    
    styling = Section(
        H2("Styling with MonsterUI", cls=(TextT.lg + TextT.muted + TextT.primary, "text-2xl mb-4")),
        PY("One of the biggest challenges in web development is creating a polished, professional-looking UI. MonsterUI solves this by providing a comprehensive set of pre-styled components that work seamlessly with FastHTML."),
        Br(),
        PY("Instead of wrestling with CSS classes and flexbox layouts, you can focus on composition. Here's a simple example of creating a card with MonsterUI:"),
        CodeBlock("""def UserProfile(user):
    return Card(
        DivLAligned(
            Avatar(user.image),
            H3(user.name, cls=TextT.bold),
            cls="gap-4"
        ),
        P(user.bio, cls=TextPresets.muted_sm),
        cls=CardT.hover
    )""", language="python"),
        PY("Notice how the styling is declarative and semantic. Instead of remembering CSS class combinations, you use preset styles like CardT.hover or TextPresets.muted_sm. These presets are carefully designed to work together, ensuring consistent spacing, typography, and interactions across your application."),
        Br(),
        PY("MonsterUI also handles responsive design automatically. Components like Grid and DivLAligned adapt to different screen sizes without requiring complex media queries. This means you can build mobile-friendly layouts with minimal effort."),
        id="styling",
        cls="mb-12"
    )
    
    dynamic = Section(
        H2("Truly Dynamic Content", cls=(TextT.lg + TextT.muted + TextT.primary, "text-2xl mb-4")),
        PY("One thing I love about FastHTML and MonsterUI is that I can create a blog without any limitations. I can publish text, but I can also embed whatever DOM elements I want. Here’s an example I made just for this post: if you log in to my site with GitHub, you’ll be able to see a GitHub insights component customized to your profile!"),
        Br(),
        PY("A traditional blogging platform would never allow that! The opportunities are limitless—code playgrounds, real-time dashboards, recommendation systems—whatever you can dream up. This is another reason I’m so excited about these libraries. In less time, I can do significantly more than I ever could with pure blogging frameworks."),
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
    
    content = Div(intro, integration, htmx, styling, dynamic, gh_integration, resources, cls="prose max-w-none")
    
    return Div(
        TableOfContents(sections),
        content,
        cls="container mx-auto max-w-3xl px-4 py-8 relative"
    )
