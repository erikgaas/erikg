## Making solo webapp development possible

If you're like me, you have a graveyard of personal projects that you have started and never finished. It's not the end of the world, I've learned a lot from unfinished work, but it's not always satisfying. Lately I wanted to change that so I went deep into React, FastAPI, AWS, and Terraform. Again, I learned a ton, but touching all parts of the fullstack app means that nothing is great. Especially for web styling. I can try to learn flexbox over and over and still not have it stick in my brain. And fullstack development with this stack takes forever. I remember it took me 5 hours to figure out how to use 3rd party Oauth sign in. Fortunately there is a much better way and I'm very excited to share it with you.

This whole site is built with FastHTML and MonsterUI. They are quite new libraries and they make making a fullstack webapp a breeze. Take this site as an example. It has a database, authentication, contact forms, mobile responsiveness, and light/dark mode. Far more than I would ever dreamed being able to put into my own site. And of course blog support! It was still a chunk of work but this took me about two weeks of evening work and some weekend free time. I shouldn't be able to make something like this myself in such a short amount of time. 😄 If I can do it you can too. There is so much to go over, but allow me to talk high level about what FastHTML and MonsterUI are and why they make me so much more productive.

## Reducing Integration Costs

On my front page you can see cards which show the latest blog posts. This queries the database and fills in the relevant information. In FastAPI you would do something like this and it would return JSON to you:

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

A React app would consume this JSON payload and transform it into your desired HTML code.

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

But what if you could just skip all this conversion step and return the HTML directly. This is exactly what FastHTML does:

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

Notice how conveniently DOM elements map to Python classes. In the blogposts router I can perform the DB query and then feed the posts directly into BlogCard objects using a python list comprehension. Given that components are just Python functions, my code can be way more modular and, in my opinion, easier to maintain.

There is way more that should be covered, but for now I'll leave you with this: the secret sauce for FastHTML is HTMX. You may have looked at the above code and wondered "What does it mean to just return some DOM element fragments in a router? Where does it go?" It is the HTMX library which allows DOM elements themselves to make HTTP requests to these endpoints and then choose what to do with the result when they are returned. For example a DOM fragment could replace an element, be added to children, as a parent, etc.

I've noticed also that all my state management seems to wind up in "backend" code making it much easier for me to track. React would consistently trip me up when state would become too complex for me to handle.

## Styling with MonsterUI

MonsterUI is like a CSS component library for FastHTML. Under the hood it leverages DaisyUI, FrankenUI, and TailwindCSS. "Card" for example is class written in MonsterUI and its sourcecode looks like this:

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

I use Card all over the place in this site. You can see them on the homepage and the blog and projects page. For example here is how I created my BlogCard:

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

Those familiar with Tailwind will see the CSS classes sprinkled in this code. You can also see how easy it is to modularize code into different variables. I could certainly improve this, but if you start with the return Card statement, it is easy to relate what the Card looks like to the code behind it.

## Truly Dynamic Content

One thing I love about FastHTML and MonsterUI is I can create a blog without any limitations. I can publish text, but I can also add in whatever DOM elements I want. Here's an example I made just for this post. If you login to my site with GitHub you will be logged in and be able to see this GitHub insights component customized to your profile!

Medium would never be able to do that! The opportunities ar limitless. Code playgrounds, real time dashboards, recommendation systems, whatever you can come up with. This is another reason I'm so excited about these libraries. In less time I can do significantly more than what I was able to do in pure blogging frameworks.

## Resources and Getting Started

My entire personal site is on GitHub, feel free to check it out at [github.com/erikgaas/erikg](https://github.com/erikgaas/erikg/tree/main).

### 1. Explore MonsterUI Components

Visit [MonsterUI](https://monsterui.answer.ai/). Check out the guides and API reference!

### 2. Learn FastHTML Basics

Read the [FastHTML documentation](https://docs.fastht.ml/) docs and [examples](https://github.com/AnswerDotAI/fasthtml/tree/main/examples). There’s also a separate repo with [advanced features](https://github.com/AnswerDotAI/fasthtml-example). One tip: feed these examples to your AI of choice. Some are very well commented which helps the LLMs out a lot. Just be careful of hallucinations. Tools like cursor really want to write FastAPI code for you at first. Just be patient and add enough code for it to shift its thinking.

### 3. Understand HTMX

[HTMX](https://htmx.org/) powers FastHTML’s seamless updates. You don’t have to be an expert, but knowing its basics helps. You can learn more from [this conversation](https://www.youtube.com/watch?v=WuipZMUch18) between Jeremy Howard (FastHTML creator) and Carson Gross (HTMX creator), and also check [Hypermedia Systems](https://hypermedia.systems/) for further insights.
