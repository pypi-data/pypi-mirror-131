# %%
from posix import environ
from .questions_utils import parse_yaml
from .questions_utils import create_cells
from .gui import create_gui
import nbformat as nbf
from urllib.request import urlretrieve
import tempfile
import os
import sys
# %%
# Ask for a token
token = os.environ['AICORE_TEACHING_TOOLS_TOKEN'] if 'AICORE_TEACHING_TOOLS_TOKEN' in os.environ else input(
    'Please, introduce your Token: ')
pathway = sys.argv[1] if len(sys.argv) > 1 else 'Essential'
# Characteristics of the notebook
lesson_ids, out_name = create_gui(token, pathway=pathway)
lessons_list = []

with tempfile.TemporaryDirectory(dir='.') as tmpdirname:
    for lesson_id in lesson_ids:
        URL = f'https://aicore-questions.s3.amazonaws.com/{lesson_id}.yaml'
        urlretrieve(URL, f'{tmpdirname}/{lesson_id}.yaml')
        lessons_list.append(f'{tmpdirname}/{lesson_id}.yaml')

    # Create the notebook
    nb = nbf.v4.new_notebook()
    questions = parse_yaml(file=lessons_list)
    cells = create_cells(questions)
    nb['cells'] = cells

    with open(out_name, 'w') as f:
        nbf.write(nb, f)

# %%
