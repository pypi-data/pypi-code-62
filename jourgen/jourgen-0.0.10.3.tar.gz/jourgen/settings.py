from jinja2 import FileSystemLoader, Environment
from jourgen.jourgen import TEMPLATES_DIR

common_template_variables = {
    # This can be commented out if you
    # don't want to have them show in your journal
    "site_url": "",
    "your_name": "Y/N",
    "site_title": "Your site's title",
    "email_url": "your@email.com",
    "email_text": "your (at) email (dot) com",
    "twitter_url": "https://twitter.com/<username>",
    "github_url": "https://github.com/<username>",
    "gitlab_url": "https://gitlab.com/<username>",
    "twitch_url": "https://twitch.tv/<username>",
}

templateLoader = FileSystemLoader(searchpath=TEMPLATES_DIR)
templateEnv = Environment(loader=templateLoader)
