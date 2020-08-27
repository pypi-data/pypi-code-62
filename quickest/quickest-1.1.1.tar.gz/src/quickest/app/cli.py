import logging
import numpy as np
from pyfiglet import Figlet

from PyInquirer import style_from_dict, Token, prompt, Separator


mockmsg = "placeholder message"

menu_style = style_from_dict(
    {
        Token.Separator: "#cc5454",
        Token.QuestionMark: "#673ab7 bold",
        Token.Selected: "#cc5454",  # default
        Token.Pointer: "#673ab7 bold",
        Token.Instruction: "",  # default
        Token.Answer: "#f44336 bold",
        Token.Question: "",
    }
)


def splash(text):
    figlet = Figlet(font="speed")
    print(figlet.renderText(text))


def print_progress_bar(current_step, total_steps, width=100):
    progress_bar_ticks = int(np.floor((current_step / total_steps) * width))
    progress_bar_spaces = width - progress_bar_ticks - 1
    percentage = int(np.ceil(float(current_step) / float(total_steps) * 100))

    if current_step == total_steps - 1:
        endchar = "\n"
    else:
        endchar = "\r"
    percentage_spacing = 3 - len(str(percentage))

    print(
        "|{}>{}| [{}{}%]".format(
            progress_bar_ticks * "-",
            progress_bar_spaces * " ",
            percentage_spacing * " ",
            percentage,
        ),
        end=endchar,
        flush=True,
    )


def app_menu(choices):
    """[summary]

    Args:
        choices (list of string): 

    Returns:
        [string]: The chosen member of the list
    """

    choice_list = []
    for choice in choices:
        choice_list.append({"name": choice})

    questions = [
        {
            "type": "list",
            "message": "What do you want to do?",
            "name": "application",
            "choices": choice_list,
            "validate": lambda answer: "You must choose at least one."
            if len(answer) == 0
            else True,
        }
    ]

    answer = prompt(questions, style=menu_style)
    return answer['application']


def list_menu(options):
    """[summary]

    Args:
        options (dictionary): A dictionary where each value is a list of options

    Returns:
        [dictionary]: A dictionary with the same keys as the input dictionary 
        but each value is a single choice from each list of options
    """

    questions = []

    for key in options:
        questions.append({
                        "type": "list",
                        "name": key,
                        "message": "Choose {}".format(key),
                        "choices": options[key],
                    })

    answers = prompt(questions, style=menu_style)

    return answers


def input_prompt(msg="Enter input", default="."):

    FIELD='ble'
    user_prompt = msg + " [{}]".format(default)
    question = [
        {
            'type' : 'input',
            'name' : FIELD,
            'message' : user_prompt
        }
    ]
    user_input = prompt(question)[FIELD]
    if not user_input:
        return default 
    else:
        return user_input

    