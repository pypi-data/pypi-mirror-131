from unittest.mock import MagicMock, patch

from hiccough import html
import pytest
import hiccough
import sys
import copy

from hiccough import build_body_and_attr


def test_simple_div():
    assert html(["div"]) == "<div></div>"


def test_class_shorthand():
    assert html(["div.class"]) == '<div class="class"></div>'


def test_nesting_and_class():
    assert (
        html(
            [
                "div.container>div.section>div.box",
                ["form", ["input", {"type": "checkbox"}]],
            ]
        )
        == '<div class="container"><div class="section"><div class="box"><form><input type="checkbox"></input></form></div></div></div>'
    )


def test_multi_class():
    assert html(["div.a.b"]) == '<div class="a b"></div>'


def test_class_merging():
    assert (
        html(["div.class-a", {"class": "class-b"}])
        == '<div class="class-b class-a"></div>'
    )


def test_id_shorthand():
    assert html(["div#name"]) == '<div id="name"></div>'


def test_multi_id():
    assert html(["div#name#blah"]) == '<div id="name"></div>'


# def test_main():
#     hic = copy.copy(hiccough)
#     hic.html = MagicMock(return_value="")
#     testargs = ["hiccough", '["div"]']
#     with patch.object(sys, "argv", testargs):
#         assert hic.main() == 0
#         hic.html.assert_called_with(["div"])


# def test_main_missing_arg():
#     hiccough.html = MagicMock(return_value="")
#     testargs = ["hiccough"]
#     with patch.object(sys, "argv", testargs):
#         assert hiccough.main() == 1
#         hiccough.html.assert_not_called()


def test_multiple_children():
    assert (
        html(["html", ["head", ["script", {"rel": "stylesheet"}]], ["body>p", "hello"]])
        == '<html><head><script rel="stylesheet"></script></head><body><p>hello</p></body></html>'
    )


def test_multiple_attr():
    assert (
        html(["div", {"id": "not-id", "other": "a"}, {"id": "id", "another": "b"}])
        == '<div id="id" other="a" another="b"></div>'
    )


def test_attr_attaches_to_nested_child():
    assert (
        html(["div>div", {"style": "color: red;"}])
        == '<div><div style="color: red;"></div></div>'
    )


def test_build_body_and_attr():
    assert build_body_and_attr(["test", {"type": "button"}, "thing"]) == (
        "testthing",
        {"type": "button"},
    )


def test_simple_attribute():
    assert (
        html(["div", "", {"style": "color: red;"}]) == '<div style="color: red;"></div>'
    )


def test_simple_nest():
    assert html(["body>p", "hello"]) == "<body><p>hello</p></body>"


def test_new_bug():
    assert (
        html(["div>div>div#target.button", "hello"])
        == '<div><div><div class="button" id="target">hello</div></div></div>'
    )
