from hiccough import html


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
