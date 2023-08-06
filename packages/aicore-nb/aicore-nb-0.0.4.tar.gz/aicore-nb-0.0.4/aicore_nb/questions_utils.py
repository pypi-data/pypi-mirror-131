from typing import List
import yaml
import nbformat as nbf


def parse_yaml(file='.questions.yaml') -> List[dict]:

    if isinstance(file, list):
        questions = []
        for f in file:
            with open(f, 'r') as stream:
                data_loaded = yaml.safe_load(stream)
            questions.extend(data_loaded['questions'])

    elif isinstance(file, str):
        with open(file, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
        questions = data_loaded['questions']

    else:
        raise ValueError('"file" has to be a list or a string')

    return questions


def create_cells(questions: List[dict]):
    cells = []

    for n, question in enumerate(questions, start=1):
        text = f'## Question {n}. \n {question["question"]}'
        cells.append(nbf.v4.new_markdown_cell(text))
        if "answer" in question:
                answer = question["answer"]
                text = f" \n <details> \n <summary> Click here to see the solution </summary> \n{answer} \n</details> \n"               
                cells.append(nbf.v4.new_markdown_cell(text))

    return cells
