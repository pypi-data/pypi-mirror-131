"""
Allows making calculations.
"""
from json import load
from os import path, getcwd
from random import choice
from verbcalc.core.dispatcher import Dispatcher, InvalidExpressionException
from verbcalc.core.translator.translator import translate


DEFAULT_DISPATCHER = Dispatcher()
DEFAULT_ANSWERS_PATH = '../data/answers.json'


def calculate(sentence: str,
              dispatcher: Dispatcher = DEFAULT_DISPATCHER,
              path_to_answers: str = DEFAULT_ANSWERS_PATH,
              silent: bool = False
              ) -> str:
    """
    Calculates result from sentence.

    Parameters:
        sentence:
            Sentence to take calculation from.

        dispatcher:
            Dispatcher object to use, if none provided it will use default one.

        path_to_answers:
            Contains path to the answers .json file.

        silent:
            Returns only the answer instead of an entire answer sentence

    Returns:
        Calculated sentence.
    """

    try:
        result = dispatcher.dispatch(translate(sentence).split())
        answer = str(int(result)) if result % 1 == 0 else str(result)

        if silent:
            return answer

        else:
            if path_to_answers is DEFAULT_ANSWERS_PATH:
                actual_path = path.join(path.dirname(__file__),
                                        path_to_answers)
            else:
                actual_path = path.join(getcwd(), path_to_answers)
            with open(actual_path, encoding='UTF-8') as file:
                answer_sentences = load(file).get('answers')
            return choice(answer_sentences) + ' ' + answer

    except ZeroDivisionError:
        return 'You cannot divide by zero!'
    except InvalidExpressionException:
        return 'Your expression is invalid'
