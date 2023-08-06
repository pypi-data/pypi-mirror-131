from unittest.mock import MagicMock

from hiccough import html

import hiccough


def test_simple_div():
    assert html(["div"]) == "<div></div>"


def test_class_shorthand():
    assert html(["div.class"]) == '<div class="class"></div>'


def test_nesting_and_class():
    assert (
        html(
            [
                "div.container>div.section>div.box",
                ["form", ["input", None, {"type": "checkbox"}]],
            ]
        )
        == '<div class="container"><div class="section"><div class="box"><form><input type="checkbox"></input></form></div></div></div>'
    )


def test_multi_class():
    assert html(["div.a.b"]) == '<div class="a b"></div>'


def test_class_merging():
    assert (
        html(["div.class-a", None, {"class": "class-b"}])
        == '<div class="class-b class-a"></div>'
    )


def test_id_shorthand():
    assert html(["div#name"]) == '<div id="name"></div>'


def test_multi_id():
    assert html(["div#name#blah"]) == '<div id="name"></div>'


def test_main():
    hiccough.html = MagicMock(return_value="")
    assert hiccough.main(["hiccough", '["div"]']) == 0
    hiccough.html.assert_called_with(["div"])


def test_main_missing_arg():
    hiccough.html = MagicMock(return_value="")
    assert hiccough.main(["hiccough"]) == 1
    hiccough.html.assert_not_called()
