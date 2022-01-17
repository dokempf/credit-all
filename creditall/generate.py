import jinja2
import json
import os
import re

from creditall.paths import get_template_loader, read_allcontributorsrc


# Internal registry of embeddings of rendering snippets into documents.
# The keys of the dictionary are the file extensions this embedding is
# used with, the second one is a tuple with the following elements:
# * A regular expression that is expected to match if and only if a reasonable
#   substitution can be done with the file can be done. Also, it needs to
#   define exactly two groups:
#     * The first one is the one where the user specified which template to use
#     * The second one is the content that will be overriden
# * A string that specifies the default template for this extension
_embeddings = {
    # In CSV files, we always substitute the full file and always use the default template
    ".csv": (r"()((?s:.)*)", "contributors.csv"),
    # Markdown embeddings are realized with a <!-- ALL-CONTRIBUTORS-LIST:START --><!-- ALL-CONTRIBUTORS-LIST:END --> separator
    ".md": (
        r"(?s:.)*<!-- ALL-CONTRIBUTORS-LIST:START ([^\ ]*) .*-->\n((?s:.)*)<!-- ALL-CONTRIBUTORS-LIST:END(?s:.)*",
        "README.md",
    ),
    # Latex embeddings are realized with % ALL-CONTRIBUTORS-LIST:START  % ALL-CONTRIBUTORS-LIST:END separator
    ".tex": (
        r"(?s:.)*% ALL-CONTRIBUTORS-LIST:START ([^\ ]*) .*\n((?s:.)*)% ALL-CONTRIBUTORS-LIST:END(?s:.)*",
        "publication.tex",
    ),
}


def render_file(targetfile):
    # Load the target file
    with open(targetfile) as f:
        content = f.read()

    # Determine the file extension
    _, ext = os.path.splitext(targetfile)

    # Find the substitution section in the content
    match_expr, default_template = _embeddings[ext]
    match = re.match(match_expr, content)

    # If there was no match, we throw an error
    if not match:
        raise ValueError(f"Could not find contributors section in {targetfile}")

    # Process match groups from regular expression
    template, replace_content = match.groups()
    template = template.strip()
    if template == "":
        template = default_template

    # Construct the Jinja environment for the replacement
    env = jinja2.Environment(
        loader=get_template_loader(),
        keep_trailing_newline=True,
    )

    # Load the data and do the rendering
    data = read_allcontributorsrc()
    rendering = env.get_template(template).render(**data)

    # Substitute the rendering into the original document and write it to file
    new_content = content.replace(replace_content, rendering)
    with open(targetfile, "w") as f:
        f.write(new_content)
