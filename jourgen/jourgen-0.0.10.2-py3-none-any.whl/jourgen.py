import os
import click
from datetime import datetime
from glob import glob
from markdown import Markdown
from shutil import copytree, rmtree, copyfile
from livereload import Server

SITE_DIR = 'site'
PAGES_DIR = 'pages'
STATIC_DIR = 'static'
TEMPLATES_DIR = 'templates'
POSTS_DIR = 'posts'


def generate_statics():
    """Generate statics folder for the built site"""
    # Copy static folder
    site_static_path = os.path.join(SITE_DIR, STATIC_DIR)

    try:
        rmtree(site_static_path)
    except FileNotFoundError:  # This is raised if no static folder is created
        pass

    copytree(
        STATIC_DIR,
        site_static_path
    )


def should_render_post(filename):
    """Returns true if a post with given `filename`
        should be rendered
    """
    fmt = "%Y-%m-%d"
    return '-'.join(filename.split('/')[-1].split('-')
                    [:3]) <= datetime.now().strftime(fmt)


def get_post_list():
    # Get list of posts
    post_list = []
    posts = filter(
        should_render_post,
        sorted(glob(os.path.join(POSTS_DIR, '*')), reverse=True)
    )

    # Generate post
    for post in posts:
        f = open(post, 'r')
        md = Markdown(extensions=['meta', 'pymdownx.superfences'])

        md.convert(f.read())
        meta = md.Meta
        site_post = os.path.join(post.replace('.md', '.html'))

        post_data = {
            'title': meta['title'][0],
            'date': meta['date'][0],
            'href': site_post
        }

        post_list.append(post_data)
    return post_list


def generate_index(templateEnv, common_template_variables):
    """Generate index page for the site"""

    template_name = 'index.html'
    index_variables = {
        'post_list': get_post_list()
    }
    template = templateEnv.get_template(template_name)
    out = template.render(**common_template_variables, **index_variables)
    with open(os.path.join(SITE_DIR, template_name), 'w') as f:
        f.write(out)


def generate_about(templateEnv):
    """Generate about page for the site"""
    template_name = 'about.html'
    template = templateEnv.get_template(template_name)
    out = template.render(**common_template_variables)
    with open(os.path.join(SITE_DIR, template_name), 'w') as f:
        f.write(out)


def clean_site_dir():
    try:
        rmtree(SITE_DIR)
    except FileNotFoundError:  # This is raised if no site folder is created
        pass

    os.mkdir(SITE_DIR)


def generate_posts(templateEnv, common_template_variables):
    # Get list of posts
    posts = glob(os.path.join(POSTS_DIR, '*'))
    os.mkdir(os.path.join(SITE_DIR, POSTS_DIR))

    # Generate post
    for post in posts:
        f = open(post, 'r')
        md = Markdown(extensions=['meta', 'pymdownx.superfences'])

        html = md.convert(f.read())
        meta = md.Meta

        template = templateEnv.get_template('post.html')
        out = template.render(
            title=meta['title'][0],
            date=meta['date'][0],
            body=html,
            **common_template_variables
        )
        site_post = os.path.join(SITE_DIR, post.replace('.md', '.html'))

        with open(site_post, 'w') as post_file:
            post_file.write(out)


def generate_page(body_name,
                  templateEnv,
                  common_template_variables,
                  template_name="page.html"):
    """Generate page for the site"""
    f = open(os.path.join(PAGES_DIR, f'{body_name}.md'))

    md = Markdown(extensions=['meta', 'pymdownx.superfences'])
    html = md.convert(f.read())
    meta = md.Meta

    template = templateEnv.get_template(template_name)

    template_variables = {
        'title': meta['title'][0],
        'body': html
    }
    out = template.render(**common_template_variables, **template_variables)

    page_path = os.path.join(SITE_DIR, f'{body_name}.html')

    with open(page_path, 'w') as page_site:
        page_site.write(out)
    template = templateEnv.get_template(template_name)
    out = template.render(**common_template_variables)
    with open(os.path.join(SITE_DIR, template_name), 'w') as f:
        f.write(out)


def build_site(templateEnv, common_template_variables):
    clean_site_dir()
    generate_statics()
    generate_index(templateEnv, common_template_variables)
    generate_page('about', templateEnv, common_template_variables)
    # generate_about()
    generate_posts(templateEnv=templateEnv,
                   common_template_variables=common_template_variables)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path')
def start(path):
    """Start your journal

    PATH is where journal will start, it defaults to the current path
    """

    if not os.path.isdir(path):
        os.makedirs(path)

    abs_path = os.path.abspath(path)

    """
    I need to copy

    - settings
    - manage
    - site folder
    - posts folder
    - pages folder
    - templates folder
    - static folder
    """
    src_dir = os.path.dirname(__file__)
    src_dst_dirs = [
        (os.path.join(src_dir, dirname), os.path.join(abs_path, dirname))
        for dirname in
        [PAGES_DIR, POSTS_DIR, TEMPLATES_DIR, STATIC_DIR]
    ]

    src_settings = os.path.join(src_dir, 'settings.py')
    dst_settings = os.path.join(abs_path, 'settings.py')

    src_manage = os.path.join(src_dir, 'manage.py')
    dst_manage = os.path.join(abs_path, 'manage.py')

    try:

        for src, dst in src_dst_dirs:
            copytree(src, dst)

        copyfile(src_settings, dst_settings)
        copyfile(src_manage, dst_manage)
    except FileExistsError:
        print(
            f"{abs_path} seems to be a journal already, please use an empty directory")


if __name__ == "__main__":
    cli()
