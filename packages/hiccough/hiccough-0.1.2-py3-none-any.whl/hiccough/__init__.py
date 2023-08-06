from typing import Any, Dict, List, Tuple, Union
from enum import Enum
import sys
import logging


logger = logging.getLogger("hiccough")
logger.addHandler(logging.NullHandler())

Tag = str
Id = str
Classes = List[str]
Attributes = Dict


class ParseError(Exception):
    pass


def html(val):
    """
    Accepts a list based tree of html nodes of the format
    [tag : str, body: Union[str, list], dict]
    where the tag is the html tag, the body is either text content
    or more nested html and dict is the tag attributes
    """
    logger.info(f"Invoked with {val}")
    # Return string values as is
    if isinstance(val, str):
        return val

    tag, *rest = val
    body, attr = build_body_and_attr(rest)

    attributes = ""

    ## handle custom tag stuff
    tag, rest_tag, tag_attr = tag_handler(tag, attr)

    if rest_tag:
        logger.info(f"Rest Args{[rest_tag, body, attr]}")
        body = html([rest_tag, body, attr])
        attr = {}
        logger.info(f"Rest Body{body}")

    if "class" in attr and "class" in tag_attr:
        attr["class"] += " " + tag_attr["class"]
        del tag_attr["class"]
    elif "class" in tag_attr:
        attr["class"] = tag_attr["class"]
        del tag_attr["class"]
    attr.update(tag_attr)
    logger.info(f"Attr {attr}")
    logger.info(f"TagAttr {tag_attr}")
    for key, val in attr.items():
        attributes += f' {key}="{val}"'
    logger.info(f"Tag : {tag}")
    logger.info(f"Attributes : {attributes}")
    logger.info(f"Body : {body}")
    return f"<{tag}{attributes}>{body}</{tag}>"


RestTag = str


def tag_handler(tag: str, attr: Attributes) -> Tuple[Tag, RestTag, Attributes]:
    # Get first actual tag
    tag, *rest_tags = tag.split(">")
    tag, id, classes = parse_tag(tag)
    temp_attr = {}
    if classes:
        temp_attr["class"] = " ".join(classes)
    if id:
        temp_attr["id"] = id
    rest_tags_txt = ">".join(rest_tags)
    res = (tag, rest_tags_txt, temp_attr)
    logger.info(f"Tag response {res}")
    return res


class TagParserState(Enum):
    TAG = 1
    CLASS = 2
    ID = 3


def parse_tag(tag_str: str) -> Tuple[Tag, Id, Classes]:
    """
    Parses an individual tag of the shorthand div.class-a.class-b#id
    and returns
    """
    if ">" in tag_str:
        raise ParseError(f"Receive nested tag {tag_str}")
    tag: Tag = None
    classes: Classes = []
    id: Id = None

    buffer = ""
    current_state = TagParserState.TAG
    for char in tag_str:
        if char == ".":
            if current_state == TagParserState.TAG:
                tag = buffer

            if current_state == TagParserState.CLASS:
                classes.append(buffer)

            if current_state == TagParserState.ID and not id:
                id = buffer
            buffer = ""
            current_state = TagParserState.CLASS
        elif char == "#":
            if current_state == TagParserState.TAG:
                tag = buffer

            if current_state == TagParserState.CLASS:
                classes.append(buffer)

            if current_state == TagParserState.ID and not id:
                id = buffer
            buffer = ""
            current_state = TagParserState.ID
        else:
            buffer += char

    # empty the buffer
    if current_state == TagParserState.TAG:
        tag = buffer

    if current_state == TagParserState.CLASS:
        classes.append(buffer)

    if current_state == TagParserState.ID and not id:
        id = buffer
    return (tag, id, classes)


def build_body_and_attr(items: List[Any]) -> Tuple[str, Dict]:
    body = ""
    attr = {}
    for item in items:
        # Item is a body element
        if isinstance(item, list):
            body += html(item)
        elif isinstance(item, str):
            body += item
        # Item is an attribute dict
        elif isinstance(item, dict):
            attr.update(item)
        else:
            raise Exception(f"Invalid form exception at: {item} Type: {type(item)}")
    return (body, attr)


def pad_list_none(list: List, pad_size: int):
    """
    Pads a list to the required size with None
    """
    return list + [None] * (pad_size - len(list))


def main() -> int:
    """Echo the input arguments to standard output"""
    if len(sys.argv) == 1:
        print("Missing second arg for generating html", file=sys.stderr)
        return 1

    arg = eval(sys.argv[1])
    print(html(arg))
    return 0


if __name__ == "__main__":
    sys.exit(main())
