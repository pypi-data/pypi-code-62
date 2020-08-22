import logging
import os
import re
from importlib import import_module
from importlib.util import module_from_spec, spec_from_file_location

from bs4 import BeautifulSoup, PageElement
from weasyprint import HTML, urls

from .cover import make_cover
from .options import Options
from .preprocessor import get_combined as prep_combined
from .styles import style_for_print
from .themes import generic as generic_theme
from .toc import make_indexes
from .utils.soup_util import clone_element
from .utils.emoji_util import fix_twemoji
from .utils.section import get_section_path


class Generator(object):

    def __init__(self, options: Options):
        self._options = options

        self._theme = self._load_theme_handler()
        self._nav = None
        self._head = None

    def on_nav(self, nav):
        """ on_nav """
        self._nav = nav
        if nav:
            self._options.logger.debug(f'theme: {self._theme}')

    def on_post_page(self, output_content: str, page, pdf_path: str) -> str:
        """ on_post_page """

        def is_excluded(url: str) -> bool:
            return url in self._options.exclude_pages

        if is_excluded(page.url):
            self.logger.info(f'Page skipped: [{page.title}]({page.url})')
            return f"<!-- skipped '{page}' -->"
        else:
            self.logger.debug(f' (post: [{page.title}]({page.url})')

        soup = self._soup_from_content(output_content, page)

        self._remove_empty_tags(soup)

        if not self._head:
            self._head = soup.find('head')
            # self.logger.debug(f'{self._head}')

        # for 'material'
        article = soup.find('article')
        if article:
            article = clone_element(article)

        # for 'mkdocs' theme
        if not article:
            main = soup.find('div', attrs={'role': 'main'})
            if main:
                article = soup.new_tag('article')
                for child in main.contents:
                    article.append(clone_element(child))

        if article:
            # remove 'headerlink' if exists.
            for a in article.select('a.headerlink'):
                a.decompose()
            for a in article.select('a.md-content__button'):
                a.decompose()
            setattr(page, 'pdf-article', article)
        else:
            self.logger.warning(f'Missing article: [{page.title}]({page.url})')

        return self._theme.inject_link(output_content, pdf_path)

    def on_post_build(self, config, output_path):
        soup = BeautifulSoup(
            '<html><head></head><body></body></html>', 'html.parser')
        if self._head:
            soup.html.insert(0, self._head)

        def add_stylesheet(stylesheet: str):
            if stylesheet:
                style_tag = soup.new_tag('style')
                style_tag.string = stylesheet
                soup.head.append(style_tag)
            pass

        add_stylesheet(style_for_print(self._options))
        add_stylesheet(self._theme.get_stylesheet())

        for page in self._nav:
            content = self._get_content(soup, page)
            if content:
                soup.body.append(content)

        make_indexes(soup, self._options)
        make_cover(soup, self._options)

        fix_twemoji(soup, self._options.logger)

        if self._options.debug_html:
            self._link_check(soup)
            print(f'{soup}')

        html = HTML(string=str(soup))
        render = html.render()

        abs_pdf_path = os.path.join(config['site_dir'], output_path)
        os.makedirs(os.path.dirname(abs_pdf_path), exist_ok=True)

        self.logger.info(f'Output a PDF to "{abs_pdf_path}".')
        render.write_pdf(abs_pdf_path)

    # ------------------------
    def _remove_empty_tags(self, soup: PageElement):

        def is_blank(el):
            if len(el.get_text(strip=True)) != 0:
                return False
            elif el.find(['img', 'svg']):
                return False
            else:
                return True

        includes = ['article', 'p']
        while True:
            hit = False
            for x in soup.find_all():
                if x.name in includes and is_blank(x):
                    # self.logger.debug(f'Strip: {x}')
                    x.extract()
                    hit = True
            if not hit:
                break

    def _page_path_for_id(self, page):
        """ normalize to directory urls style"""

        if page.is_section:
            path = get_section_path(page)
        else:
            path = page.url

        path = '.' if not path or path == 'index.html' else path
        if path.endswith('index.html'):
            path = re.sub(r'index\.html$', '', path)
        elif path.endswith('.html'):
            path = re.sub(r'\.html$', '/', path)
        return path

    def _soup_from_content(self, content: str, page):
        soup = BeautifulSoup(content, 'html.parser')

        try:
            abs_dest_path = page.file.abs_dest_path
            src_path = page.file.src_path
        except AttributeError:
            abs_dest_path = page.abs_output_path
            src_path = page.input_path

        path = os.path.dirname(abs_dest_path)
        os.makedirs(path, exist_ok=True)
        filename = os.path.splitext(os.path.basename(src_path))[0]
        base_url = urls.path2url(os.path.join(path, filename))

        return prep_combined(soup, base_url, page.file.url)

    def _get_content(self, soup: PageElement, page):

        def shift_heading(elem, page):
            for i in range(7, 0, -1):
                while True:
                    h = elem.find(f'h{i}')
                    if not h:
                        break
                    h.name = f'h{i + 1}'

            page_path = self._page_path_for_id(page)
            h1 = soup.new_tag('h1', id=f'{page_path}')
            h1.append(page.title)
            elem.insert(0, h1)
            return elem

        def cleanup_class(classes: []):
            if classes and len(classes):
                excludes = ['md-content__inner']
                return [c for c in classes if not (c in excludes)]
            return classes

        article = getattr(page, 'pdf-article', None)
        if article:

            page_path = self._page_path_for_id(page)
            article['id'] = f'{page_path}:'  # anchor for each page.
            article['data-url'] = f'/{page_path}'
            return article

        elif page.children:

            new_article = soup.new_tag('article')
            found = False
            for c in page.children:
                content = self._get_content(soup, c)
                if content:
                    new_article.append(content)
                    found = True

            if not found:
                return None

            child_classes = None
            for child_article in new_article.find_all('article'):
                child_article.name = 'section'
                classes = child_article.get('class')
                if classes and not child_classes:
                    child_classes = classes
                child_article['class'] = cleanup_class(classes)

            page_path = self._page_path_for_id(page)
            new_article['id'] = f'{page_path}:'  # anchor for each page.
            new_article['data-url'] = f'/{page_path}'
            if child_classes:
                new_article['class'] = child_classes

            if self._options.heading_shift:
                return shift_heading(new_article, page)
            return new_article

        return None

    # -------------------------------------------------------------

    @property
    def logger(self) -> logging:
        return self._options.logger

    def _load_theme_handler(self):
        theme = self._options.theme_name
        custom_handler_path = self._options.theme_handler_path
        module_name = '.' + (theme or 'generic').replace('-', '_')
        if custom_handler_path:
            try:
                spec = spec_from_file_location(
                    module_name, os.path.join(
                        os.getcwd(), custom_handler_path))
                mod = module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod
            except FileNotFoundError as e:
                self.logger.error(
                    f'Could not load theme handler {theme}'
                    f' from custom directory "{custom_handler_path}": {e}')
                pass

        try:
            return import_module(module_name, 'mkdocs_with_pdf.themes')
        except ImportError as e:
            self.logger.error(f'Could not load theme handler {theme}: {e}')
            return generic_theme

    # -------------------------------------------------------------

    def _link_check(self, soup):
        from urllib.parse import urlparse

        anchors = set(map(lambda el: '#' + el['id'], soup.find_all(id=True)))

        '''
        from pprint import pprint as pp
        pp(anchors)
        '''

        missing = set()
        for el in soup.find_all('a', href=True):
            href = el['href']
            target_url = urlparse(href)

            if target_url.scheme or target_url.netloc:
                continue
            if href in anchors:
                continue

            missing.add(href)

        if len(missing):
            self.logger.error(f'Missing {len(missing)} link(s):')
            for link in sorted(missing):
                self.logger.warning(f'  | {link}')
            self.logger.info('  | --- found anchors:')
            for anchor in sorted(anchors):
                self.logger.info(f'  | {anchor}')
