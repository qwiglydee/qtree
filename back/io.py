from back.types import Model, Data, Effect
from back.templates import templates

NEXT_BTN = {"next": bool}


def output(template: str) -> Effect:
    return Effect(template)


def update(data: Data) -> Effect:
    return Effect(V=data)


def input(fields: Model) -> Effect:
    return Effect(I=fields)


def message(html: str) -> Effect:
    return Effect(html, I=NEXT_BTN)


def page(filename, data=None) -> Effect:
    template = templates.get_template(filename)
    if data is None:
        data = {}
    return Effect(template, data, NEXT_BTN)


def form(filename, data, fields) -> Effect:
    template = templates.get_template(filename)
    if data is None:
        data = {}
    fields.update(NEXT_BTN)
    return Effect(template, data, fields)
