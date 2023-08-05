from datetime import datetime
import glob
import os
from shutil import copytree, copy2
from sys import argv
import markdown
from jinja2 import Environment, FileSystemLoader

def get_title_date(fname, md):
    md.reset()
    with open(fname, "r") as f:
        txt = f.read()
        md.convert(txt)
        title = ""
        date = "1999-12-01"
        for k, v in md.Meta.items():
            if k == "title":
                title = v[0]
            elif k == "date":
                date = v[0]
    
    return title, date



def render(fname, md, env, **kwargs):
    md.reset()
    with open(fname, "r") as f:
        txt = f.read()
        html = md.convert(txt)
        title = ""
        template_name = ""
        other_head = ""
        date = "1999-12-01"
        for k, v in md.Meta.items():
            if k == "title":
                title = v[0]
            elif k == "template":
                template_name = v[0]
            elif k == "date":
                date = v[0]
            else:
                other_head += f'<meta name="{k}" content="{v[0]}">\n'

        tmpl = env.get_template(template_name)
        return tmpl.render({
            "title": title,
            "other_head": other_head,
            "toc": md.toc,
            "content": html,
            "date": date,
            "meta": md.Meta,
            "other": kwargs
        })


def generate(src, dst, template):

    md = markdown.Markdown(extensions=["abbr", "footnotes", "tables", "toc", 
                            "attr_list", "meta", "admonition", "fenced_code"])
    env = Environment(
        loader=FileSystemLoader(template)
    )

    copytree(src, dst, copy_function=copy2, dirs_exist_ok=True)

    index_paths = []
    non_removes = set()

    for name in glob.iglob(os.path.join(dst, "**", "*.md"), recursive=True):
        if os.path.basename(name) == "index.md":
            index_paths.append(os.path.dirname(name))
            continue

        try:
            html = render(name, md, env)
            fname = name.replace(".md", ".html")
            with open(fname, "w") as f:
                f.write(html)
        except:
            print(f"{name} could not be compiled!")
            non_removes.add(name)

    
    for path in index_paths:
        posts = []
        for name in glob.iglob(os.path.join(path, "**", "*.md"), recursive=True):
            if name.endswith("index.md"):
                continue
            title, date = get_title_date(name, md)
            url = os.path.relpath(name.replace(".md", ".html"), start=path)
            posts.append((title, date, url))

        posts.sort(key=lambda x: datetime.fromisoformat(x[1]), reverse=True)
        name = os.path.join(path, "index.md")

        try:
            html = render(name, md, env, posts=posts)
            fname = name.replace(".md", ".html")
            with open(fname, "w") as f:
                f.write(html)
        except:
            print(f"{name} could not be compiled!")
            non_removes.add(name)


    for name in glob.iglob(os.path.join(dst, "**", "*.md"), recursive=True):
        if not name in non_removes:
            os.remove(name)
        
    

    


    


if __name__ == "__main__":
    generate(argv[1], argv[2], argv[3])
