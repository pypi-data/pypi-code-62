from django.db import models
from django.utils.translation import gettext as _

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from menu_header_wagtail.blocks.navbar_block import NavPageLinkWithSubLinkBlock, NavDocumentLinkWithSubLinkBlock, \
    NavExternalLinkWithSubLinkBlock

NAVIGATION_BLOCKS = [
    ('page_link', NavPageLinkWithSubLinkBlock()),
    ('external_link', NavExternalLinkWithSubLinkBlock()),
    ('document_link', NavDocumentLinkWithSubLinkBlock()),
]


@register_snippet
class HeaderPage(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name header'),
        help_text=_('This option allows you to create different menus for different pages')
    )
    logo_type = models.CharField(
        choices=[
            ('text', _('Text')),
            ('image', _('Image')),
        ],
        default='text',
        verbose_name='Logo type',
        max_length=10,
    )
    image_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Image logo'),
        help_text='Max height 50px'
    )
    text_logo = models.CharField(
        null=True,
        blank=True,
        verbose_name='Text Logo',
        max_length=100,
    )
    header_fixed = models.BooleanField(verbose_name='Header fixed?', default=True)

    navigation = StreamField(NAVIGATION_BLOCKS, null=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('logo_type'),
        FieldPanel('text_logo'),
        ImageChooserPanel('image_logo'),
        FieldPanel('header_fixed'),
        StreamFieldPanel('navigation')
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Header page')
        verbose_name_plural = _('Headers Page')
