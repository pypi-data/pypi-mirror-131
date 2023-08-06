# hiccough
Hiccough is a simple html templating tool heavily inspired by https://github.com/weavejester/hiccup. It allows for the generation of 
html strings from nested lists of python like so
```
hiccough.html(["div.myclass", ["p", "Hello World!"]])
=> '<div class="myclass"><p>Hello World!</p></div>'
```


## Nesting Shorthand
Hiccough supports a nesting syntax via `>` for multiple nested tags
with only classes and ids. 
```
html(["div.a>div.b>div.c", "It's divs all the way down!"])
=>'<div class="a"><div class="b"><div class="c"></div>It's divs all the way down!</div></div>'
```

## CLI
Hiccough currently support execution on the cli with the first argument being
a string that evals to a python list matching what would get passed to `html/1`