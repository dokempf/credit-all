import jinja2
import json
import os


def generate_context(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    # Maybe rearrange data here, so that it is easier to use
    # from the templating language.

    return data


def render_output(datafile, template, outputfile):
    # Locate the templates directory correctly
    path, _ = os.path.split(__file__)
    template_path = os.path.join(path, "templates")

    # Construct the Jinja environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_path),
        keep_trailing_newline=True,
    )

    # Construct the data context for the template rendering
    ctx = generate_context(datafile)

    # Render the template
    rendering = env.get_template(template).render(**ctx)

    # And maybe write it to a file:
    if outputfile is not None:
        with open(outputfile, 'w') as outfile:
            outfile.write(rendering)

    return rendering
