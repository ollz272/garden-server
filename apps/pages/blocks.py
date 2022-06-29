from wagtail.blocks import StreamBlock, RichTextBlock


class HomePageStreamBlock(StreamBlock):
    text = RichTextBlock()
