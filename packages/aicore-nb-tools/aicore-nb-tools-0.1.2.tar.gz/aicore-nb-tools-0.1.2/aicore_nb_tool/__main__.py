#%%
from .questions_utils import parse_yaml
from .questions_utils import create_cells
from .questions_utils import read_args
from .gui import create_gui
import nbformat as nbf
from urllib.request import urlretrieve
import tempfile

args = read_args()

if args.token is None:
    token = input('Please, introduce your Token: ')
else:
    token = args.token

# Characteristics of the notebook
if args.create_groups:
    cohort, lesson_ids, out_name, first_room, students_per_room = create_gui(token, pathway=args.pathway)
else:
    cohort, lesson_ids, out_name = create_gui(token, pathway=args.pathway, create_groups=False)

lessons_list = []

with tempfile.TemporaryDirectory(dir='.') as tmpdirname:
    for lesson_id in lesson_ids:
        URL = f'https://aicore-questions.s3.amazonaws.com/{lesson_id}.yaml'
        urlretrieve(URL, f'{tmpdirname}/{lesson_id}.yaml')
        lessons_list.append(f'{tmpdirname}/{lesson_id}.yaml')
        
    # Create the notebook
    nb = nbf.v4.new_notebook()
    questions = parse_yaml(file=lessons_list)
    if args.create_groups:
        cells = create_cells(questions, cohort, first_room, students_per_room)
    else:
        cells = create_cells(questions, cohort, init_room=0, students_per_room='', create_groups=False)
    nb['cells'] = cells

    with open(out_name, 'w') as f:
        nbf.write(nb, f)
