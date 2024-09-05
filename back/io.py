from back.templates import templates


def output(template):
    return {"T": template}


def update(data):
    return {"V": data}


def input(fields):
    return {"I": fields}


def message(html):
    return {"T": html, "I": {"next": bool}}


def page(filename, data=None):
    template = templates.get_template(filename)
    if data is None:
        data = {}
    return {"T": template, "V": data, "I": {"next": bool}}


def form(filename, data, fields):
    template = templates.get_template(filename)
    if data is None:
        data = {}
    fields["next"] = bool
    return {"T": template, "V": data, "I": fields}
