from taggit.utils import _parse_tags

def lowercase_tags(tag_string):
    """Use taggit to parse the lowercased string"""
    return _parse_tags(tag_string.lower())

