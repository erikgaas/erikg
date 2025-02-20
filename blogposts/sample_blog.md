## Making solo webapp development possible

If you're like me, you have a graveyard of personal projects that you started but never finished. It’s not the end of the world—I've learned a lot from unfinished work—but it’s not always satisfying. Recently, I wanted to change that, so I dove deep into React, FastAPI, AWS, and Terraform. Again, I learned a ton, but touching every part of a full-stack app meant that nothing was great, especially web styling. I can try to learn flexbox over and over, yet it never seems to stick in my brain.

Full-stack development with this stack also takes forever. I remember spending five hours just figuring out how to implement third-party OAuth sign-in. Fortunately, there’s a much better way, and I’m very excited to share it with you.

This entire site is built with FastHTML and MonsterUI—two relatively new libraries that make full-stack web app development a breeze. Take this site as an example: it has a database, authentication, contact forms, mobile responsiveness, and light/dark mode—far more than I ever dreamed of implementing in my own project. And, of course, blog support!

It still required effort, but I built all of this in about two weeks of evening work and some weekend free time. I shouldn't have been able to make something like this myself in such a short period. 😄 If I can do it, you can too. There’s so much to cover, but let’s start with a high-level look at what FastHTML and MonsterUI are and why they make me so much more productive.

## Reducing Integration Costs

On my front page, you can see cards displaying the latest blog posts. These query the database and fill in relevant information. In FastAPI, you would typically do something like this to return JSON:

```python
@app.get("/api/blogs")
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
    ]
```

A React app would then consume this JSON payload and transform it into HTML:

```js
function BlogCard({ blog }) {
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
```

But what if you could skip this conversion step and return the HTML directly? That’s exactly what FastHTML does:

```python
@rt("/blogposts")
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
    )
```

Notice how conveniently DOM elements map to Python classes. In the blogs router, I query the database and feed the posts directly into BlogCard objects using list comprehension. Since components are just Python functions, my code is far more modular and, in my opinion, easier to maintain.

## The Power of HTMX

The secret sauce behind FastHTML is HTMX. If you looked at the code above and wondered, “What happens when these DOM elements are returned from a router?”—the answer is HTMX. This library allows DOM elements to make HTTP requests to these endpoints and decide how to handle the returned data (e.g., replacing elements, adding children, etc.).

I've also noticed that all my state management naturally ends up in backend code, making it much easier to track. React often tripped me up when state became too complex to handle effectively.

## Styling with MonsterUI

MonsterUI is a CSS component library for FastHTML. Under the hood, it leverages DaisyUI, FrankenUI, and TailwindCSS. For example, the Card component in MonsterUI is implemented as follows:

```python
def Card(*c, # Components that go in the body (Main content of the card such as a form, and image, a signin form, etc.)
        header=None, # A component that goes in the header (often a `ModalTitle` and description)
        footer=None,  # A component that goes in the footer (often a `ModalCloseButton`)
        body_cls='space-y-6', # classes for the body
        header_cls=(), # classes for the header
        footer_cls=(), # classes for the footer
        cls=(), #class for outermost component
        **kwargs # additional arguments for the `CardContainer`
        )->FT: # Card component
    "Creates a Card with a header, body, and footer"
    header_cls, footer_cls, body_cls, cls = map(stringify, (header_cls, footer_cls, body_cls, cls))
    res = []
    if header: res.append(CardHeader(cls=header_cls)(header))
    res.append(CardBody(cls=body_cls)(*c))
    if footer: res.append(CardFooter(cls=footer_cls)(footer))
    return CardContainer(cls=cls, **kwargs)(*res)
```

I use Card throughout this site, including the homepage, blog, and projects page. Here’s how I created my BlogCard component:

```python
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
```

## Truly Dynamic Content

One thing I love about FastHTML and MonsterUI is that I can create a blog without any limitations. I can publish text, but I can also embed whatever DOM elements I want. Here’s an example I made just for this post: if you log in to my site with GitHub, you’ll be able to see a GitHub insights component customized to your profile!

A traditional blogging platform would never allow that! The opportunities are limitless—code playgrounds, real-time dashboards, recommendation systems—whatever you can dream up. This is another reason I’m so excited about these libraries. In less time, I can do significantly more than I ever could with pure blogging frameworks.

## Resources and Getting Started

My entire personal site is on GitHub, feel free to check it out at [github.com/erikgaas/erikg](https://github.com/erikgaas/erikg/tree/main).

### 1. Explore MonsterUI Components

Visit [MonsterUI](https://monsterui.answer.ai/). Check out the guides and API reference!

### 2. Learn FastHTML Basics

Read the [FastHTML documentation](https://docs.fastht.ml/) docs and [examples](https://github.com/AnswerDotAI/fasthtml/tree/main/examples). There’s also a separate repo with [advanced features](https://github.com/AnswerDotAI/fasthtml-example). One tip: feed these examples to your AI of choice. Some are very well commented which helps the LLMs out a lot. Just be careful of hallucinations. Tools like cursor really want to write FastAPI code for you at first. Just be patient and add enough code for it to shift its thinking.

### 3. Understand HTMX

[HTMX](https://htmx.org/) powers FastHTML’s seamless updates. You don’t have to be an expert, but knowing its basics helps. You can learn more from [this conversation](https://www.youtube.com/watch?v=WuipZMUch18) between Jeremy Howard (FastHTML creator) and Carson Gross (HTMX creator), and also check [Hypermedia Systems](https://hypermedia.systems/) for further insights.
