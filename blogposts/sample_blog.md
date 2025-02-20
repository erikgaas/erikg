## Making solo webapp development possible

I’ve never been as productive building a webapp as I am now. This entire blog runs on my personal site, built with FastHTML and MonsterUI. I’ve tried many leading frontend frameworks over the years, only to get bogged down by their complexity. Before this, my go-to stack was FastAPI and React—yet even adding a third-party OAuth login felt like an all-day affair. The tools themselves are powerful; it’s the sprawling ecosystems that overwhelmed me as a solo developer wanting a full-featured app: database, business logic, and a customizable UI.

Then I discovered FastHTML and MonsterUI. Yes, they’re more frameworks you might not have heard of—but here’s why they’re worth a look. Simply put, this site is the first time I’ve built exactly what I envisioned: it has databases, authentication, contact forms, mobile responsiveness, and theme support. Getting here with other stacks took far too much time, if it ever happened at all. Now, I’m excited to share how straightforward it can be once you have the right tools in hand. If I can do this, so can you.

## Removing Barriers

What does a “barrier” look like in practice? Let’s walk through a simple scenario—displaying blog post cards—to see how FastHTML compares to a standard FastAPI and React setup.

Consider a basic example: displaying blog post cards. With FastAPI, you typically write an endpoint returning JSON:

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

Then you’d transform that JSON into HTML in React:

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
}
```

With FastHTML, you skip the JSON step and directly return styled HTML:

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

Combined with HTMX, FastHTML can serve a full page or just the snippet needed to update an existing page section. Whether you’re loading more posts or filtering by tag, FastHTML returns new cards on demand—no JSON conversion, no separate state management, no extra styling system. You simply define the HTML in Python and let HTMX slot it right into place.

## Truly Dynamic Content

“Why not just use Medium or another blogging platform?” They do handle plenty of complexity, but they also limit your options. With FastHTML, you can add truly interactive components that go beyond any preset template.

For example, I recently added a dynamic GitHub insights panel to my posts. It’s not just static text—it queries GitHub live and returns up-to-date information. Try doing that on Medium! Because FastHTML lets you embed any custom component, you can drop in code playgrounds, real-time data visualizations, or personalized recommendations right alongside your written content.

That’s where FastHTML really shines: it’s not just about making simple development easier, but about bringing once-complex features within reach. The same component system that handles basic blog posts can also power complex, dynamic, authenticated content without getting in your way.

## Resources and Getting Started

My entire personal site is on GitHub if you want a working example: [github.com/erikgaas/erikg](https://github.com/erikgaas/erikg/tree/main).

### 1. Explore MonsterUI Components

Visit [MonsterUI](https://monsterui.answer.ai/) to see how little code you need for polished UIs. It layers on FrankenUI, DaisyUI, and TailwindCSS—modern tools that give you plenty of flexibility.

### 2. Learn FastHTML Basics

Check the [FastHTML documentation](https://docs.fastht.ml/) docs and [examples](https://github.com/AnswerDotAI/fasthtml/tree/main/examples). There’s also a separate repo with [advanced features](https://github.com/AnswerDotAI/fasthtml-example). A tip: feeding these examples to your AI assistant can speed learning, though watch out for hallucinations.

### 3. Understand HTMX

[HTMX](https://htmx.org/) powers FastHTML’s seamless updates. You don’t have to be an expert, but knowing its basics helps. You can learn more from [this conversation](https://www.youtube.com/watch?v=WuipZMUch18) between Jeremy Howard (FastHTML creator) and Carson Gross (HTMX creator), and also check [Hypermedia Systems](https://hypermedia.systems/) for further insights.
