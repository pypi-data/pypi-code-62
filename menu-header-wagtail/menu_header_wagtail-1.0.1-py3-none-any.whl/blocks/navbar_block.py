from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from django.utils.translation import gettext as _


class NavBaseLinkBlock(blocks.StructBlock):
    display_text = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Text Menu'),
    )


class NavPageLinkBlock(NavBaseLinkBlock):
    """
    Page link.
    """
    page = blocks.PageChooserBlock(
        label=_('Page'),
    )

    class Meta:
        template = 'menu_header_wagtail/menu/page_link_block.html'
        label = _('URL Page')


class NavDocumentLinkBlock(NavBaseLinkBlock):
    """
    Document link.
    """
    document = DocumentChooserBlock(
        label=_('Document'),
    )

    class Meta:
        template = 'menu_header_wagtail/menu/document_link_block.html'
        label = _('URL Document')


class NavExternalLinkBlock(NavBaseLinkBlock):
    """
    External link.
    """
    link = blocks.CharBlock(
        required=False,
        label=_('URL'),
    )

    class Meta:
        template = 'menu_header_wagtail/menu/external_link_block.html'
        label = _('URL External')


class NavSubLinkBlock(blocks.StructBlock):
    sub_links = blocks.StreamBlock(
        [
            ('page_link', NavPageLinkBlock()),
            ('external_link', NavExternalLinkBlock()),
            ('document_link', NavDocumentLinkBlock()),
        ],
        required=False,
        label=_('Sub menú'),
    )


class NavPageLinkWithSubLinkBlock(NavSubLinkBlock, NavPageLinkBlock):
    """
    Page link with option for sub-links or showing child pages.
    """
    open_page_new_window = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_('Open in a new page'),
        help_text=_('Select if you want to open in a new tab when user clicks'),
    )

    class Meta:
        label = _('URL page with submenu')


class NavDocumentLinkWithSubLinkBlock(NavSubLinkBlock, NavDocumentLinkBlock):
    """
    Document link with option for sub-links.
    """

    class Meta:
        label = _('URL Document with submenu')


class NavExternalLinkWithSubLinkBlock(NavSubLinkBlock, NavExternalLinkBlock):
    """
    External link with option for sub-links.
    """

    class Meta:
        label = _('External URL with submenu')

