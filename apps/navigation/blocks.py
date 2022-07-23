from wagtail.blocks import CharBlock, StreamBlock, StructBlock
from wagtail_link_block.blocks import LinkBlock


class QuickLinkBlock(StructBlock):
    link = LinkBlock(label=False)
    link_text = CharBlock(label="Link text")

    class Meta:
        icon = "link"
        label = "Quick link"
        template = "blocks/quick_link_block.html"


class LinksBlock(StreamBlock):
    link = QuickLinkBlock(label="link", required=False)
