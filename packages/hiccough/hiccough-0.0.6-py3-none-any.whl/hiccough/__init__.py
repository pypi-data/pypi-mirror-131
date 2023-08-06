from typing import List, Union
import sys


def html(val: Union[str, List]):
    """
    Accepts a list based tree of html nodes of the format
    [tag : str, body: Union[str, list], dict]
    where the tag is the html tag, the body is either text content
    or more nested html and dict is the tag attributes
    """
    if isinstance(val, str):
        return val

    tag, body, attr = pad_list_none(val, 3)
    if not attr:
        attr = {}
    attributes = ""
    ## handle custom tag stuff
    tag, *rest = tag.split(">")
    tag_sub = tag.split(".")
    if len(tag_sub) > 1:
        tag = tag_sub[0]
        if attr and "class" in attr.keys():
            attr["class"] += " " + " ".join(tag_sub[1:])
        else:
            attr["class"] = " ".join(tag_sub[1:])
    tag, id, *_ = pad_list_none(tag.split("#"), 3)
    print(tag)
    if id:
        attr["id"] = id
    body = "" if not len(val) >= 2 or not val[1] else html(val[1])
    if rest:
        body = html([">".join(rest), body])
    for key, val in attr.items():
        attributes += f' {key}="{val}"'
    return f"<{tag}{attributes}>{body}</{tag}>"


def pad_list_none(list: List, pad_size: int):
    """
    Pads a list to the required size with None
    """
    return list + [None] * (pad_size - len(list))


def main(args) -> int:
    """Echo the input arguments to standard output"""
    if len(args) == 1:
        print("Missing second arg for generating html", file=sys.stderr)
        return 1

    arg = eval(args[1])
    print(html(arg))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.arg))  # next section explains the use of sys.exit
