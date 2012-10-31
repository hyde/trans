A simple hyde website derived from the BASIC layout
that provides support for a multilingual site.

# Setup

```
mkvirtualenv hyde --no-site-packages
pip install -r requirements.txt
```

# Working

```
# Generate the site
hyde gen -r

# Serve
hyde serve
```

# Translations

Uses babel for translations.

This can be vastly improved. One of the major goals of
hyde 1.0 is to make it absolutely simple to create
multi language sites. So, expect a lot of improvements
in this area soon.

## Extract

```
pybabel extract -F babel.cfg -o strings/messages.pot .
```


## Initialize

Using the `ru` locale as an example:

```
pybabel init -l ru -i strings/messages.pot -d .
```

Now you can edit the catalog file at `./strings/ru/LC_MESSAGES/messages.po`

## Compile

```
pybabel compile -f -d ./strings
```

## Update from template

```
pybabel update -i ./strings/messages.pot -d ./strings
```

# References

1. [Jinja2 Translations](http://jinja.pocoo.org/docs/templates/#i18n-in-templates)
2. [Jinja2 i18N](http://jinja.pocoo.org/docs/extensions/#i18n-extension)
3. [Jinja2 Babel integration](http://jinja.pocoo.org/docs/integration/#babel-integration)
4. [Babel](http://babel.edgewall.org/wiki/Documentation)