import functools
from vv.questions_parser import *
from vv.finder import *
from vv.markers import *
from vv.questions import *

# Власне висловлення у BNF
#
# <власне_висловлення> ::= АБЗАЦ <теза>
#                          АБЗАЦ <аргумент>
#                          АБЗАЦ <приклад_із_літератури>
#                          АБЗАЦ <аргумент>
#                          АБЗАЦ <приклад_із_життя>
#                          АБЗАЦ <висновок> ;
#
# <теза> ::= <речення_гачок>
#            <слово_маркер_теза> <речення_тези> ;
# <речення_тези> ::= <своя_думка> [ ',' <теза_арг_початок> <коротко_про_арг1> <теза_арг_сполучник> <коротко_про_ар2> ] ;
#
# <аргумент> ::= <слово_маркер_аргумент> <речення_аргументу>* ;
#
# <приклад_із_літератури> ::= <слово_маркер_приклад> <речення_джерело_приклада> <речення_приклада>* ;
#
# <приклад_із_життя> ::= <речення_приклада>* ;
#
# <висновок> ::= <слово_маркер_висновок> <речення_висновку> ;
#
#
# Алгоритм:
# 1. Визначити тип тези.
# 2. Розпарсити тезу. (як?)


def make_sentence(txt: str) -> str:
    work = transform_text(txt.split('.')[0].strip())
    work = filter(lambda x: x != '', work.split(' '))
    work = map(lambda x: x.strip(), work)
    work = functools.reduce(lambda a, b: a + ' ' + b, work)
    work = work[0].upper() + work[1:]
    if work[-1] != '!' and work[-1] != '?' and work[-1] != '.':
        work += '.'
    return work


def choose_two_sentences(strs: [str]) -> [str]:
    chosen = random.choice(list(range(len(strs))))
    if chosen != 0:
        chosen -= 1

    result = [make_sentence(strs[chosen]), make_sentence(strs[chosen + 1])]
    return result


class Thesis:
    question: Question
    arguments: list

    choice: str
    can_or_not: bool

    sentence: str

    def __init__(self, question: Question):
        self.question = question
        self.arguments = []

        if isinstance(self.question, ChoiceQuestion):
            self.choice = random.choice(self.question.get_choices())
        elif isinstance(self.question, CanOrNotQuestion):
            self.can_or_not = random.choice([True, False])

        if isinstance(self.question, ChoiceQuestion):
            self.sentence = self.question.about + ' ' + self.choice
        elif isinstance(self.question, CanOrNotQuestion):
            self.sentence = ('не ' if not self.can_or_not else '') + self.question.term

    def add_arguments(self, argument1, argument2):
        self.arguments.append(argument1)
        self.arguments.append(argument2)

    def generate(self) -> str:
        marker = random.choice(marker_teza)
        result = marker + ' ' + self.sentence

        if len(self.arguments) != 0:
            result += ', ' + random.choice(marker_teza_subargs_start) + ' '
            result += self.arguments[0].short_form
            result += ' ' + random.choice(marker_teza_subargs_delim) + ' '
            result += self.arguments[1].short_form

        result += '.'

        gachok = self.generate_gachok()
        result = gachok + ' ' + result

        return result

    def generate_gachok(self) -> str:
        while True:
            strings = find_some_info(self.question.orig_str)
            if len(strings) < 1:
                continue
            return make_sentence(strings[0])


class Argument:
    teza: Thesis
    short_form: str
    long_form: str
    is_first: bool

    sentence1: str
    sentence2: str

    def __init__(self, teza: Thesis, is_first: bool):
        self.teza = teza
        self.is_first = is_first
        self.create_self()

    def create_self(self):
        choose_something = []
        while True:
            strs = find_some_info(self.teza.sentence)
            half_len = len(strs) // 2
            strs_to_choose = strs[half_len // 2:-(half_len // 2)]
            if len(strs_to_choose) <= 2:
                continue
            else:
                choose_something = map(lambda x: map(lambda y: y.strip(), x.split('.')),
                                       strs_to_choose)
                choose_something = [item for sublist in choose_something for item in sublist]
                break

        def filter_func(txt: str):
            if len(txt) < 4:
                return False
            elif txt.isdigit():
                return False
            elif txt.count('"') != 0 or txt.count("'") != 0:
                return False
            else:
                return True

        choose_something = list(filter(filter_func, choose_something))
        chosen_sentences = choose_two_sentences(choose_something)

        self.sentence1 = chosen_sentences[0]
        self.sentence2 = chosen_sentences[1]

        self.short_form = self.sentence1[0].lower() + self.sentence1[1:-1]

        self.long_form = self.short_form + '. ' + self.sentence2

    def generate(self) -> str:
        result = 'По-перше, ' if self.is_first else 'По-друге, '
        result += self.long_form

        return result


class Example:
    teza: Thesis
    argument: Argument
    is_life: bool

    def __init__(self, teza: Thesis, argument: Argument, is_life: bool):
        self.teza = teza
        self.argument = argument
        self.is_life = is_life

    def generate(self) -> str:
        marker = random.choice(marker_example_life if self.is_life else marker_example_literature)
        result = marker + ' '

        if self.is_life:
            result += self.generate_life()
        else:
            result += self.generate_lit()

        return result

    def generate_life(self):
        links = find_links(self.argument.short_form + ' приклад з власного життя')
        found_info = []
        for link in links:
            ps = find_some_info_in_link(link)
            sentences = []
            for p in ps:
                sentences += p.split('.')
            found_info += list(filter(lambda txt: txt.find(' я ') != -1, sentences))

        chosen = choose_two_sentences(found_info)

        sentence1 = chosen[0][0].lower() + chosen[0][1:]
        sentence2 = chosen[1]

        return sentence1 + ' ' + sentence2

    def generate_lit(self):
        return ''


class Finale:
    teza: Thesis

    def __init__(self, teza: Thesis):
        self.teza = teza

    def generate(self) -> str:
        result = random.choice(marker_finish) + ' ' + self.teza.sentence
        return result + '.'


class VV:
    question: Question

    def __init__(self, question_txt: str):
        parser = QuestionParser(question_txt)
        self.question = parser.parse()

    def generate(self) -> str:
        teza = Thesis(self.question)
        argument1 = Argument(teza, True)
        argument2 = Argument(teza, False)
        life_lit = random.choice([[True, False], [False, True]])
        example1 = Example(teza, argument1, life_lit[0])
        example2 = Example(teza, argument2, life_lit[1])
        teza.add_arguments(argument1, argument2)
        finale = Finale(teza)

        teza_str = teza.generate()
        argument1_str = argument1.generate()
        argument2_str = argument2.generate()
        example1_str = example1.generate()
        example2_str = example2.generate()
        finale_str = finale.generate()

        tab = ' ' * 4
        whole = tab + teza_str + '\n' + \
                tab + argument1_str + '\n' + \
                tab + example1_str + '\n' + \
                tab + argument2_str + '\n' + \
                tab + example2_str + '\n' + \
                tab + finale_str + '\n'

        return whole
