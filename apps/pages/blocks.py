from wagtail.blocks import RichTextBlock, StreamBlock


class HomePageStreamBlock(StreamBlock):
    text = RichTextBlock()
