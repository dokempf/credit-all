import json


def generate_context(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    # Maybe rearrange data here, so that it is easier to use
    # from the templating language.

    return data


def render_output():
