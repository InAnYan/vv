import re
from vv.questions import *


def transform_text(txt: str) -> str:
    return re.sub('[?.!,"<>»«()[]{}/\\\']', '', txt.lower()).replace('–', '-')


class QuestionParser:
    questions_keywords = {
        ChoiceQuestion:   [':', ',', 'чи'],
        CanOrNotQuestion: ['чи', 'може', 'можливо', 'призведе', 'призведуть', 'призвести', 'можлива', 'можна', 'можливе', 'треба', 'необхідно', 'має'],
        WhyQuestion:      ['за', 'якими', 'критерії', 'критеріями', 'критеріями', 'чинники', 'що', 'у', 'чому'],
        WhichQuestion:    ['чому'],
        HowMuchQuestion:  ['на', 'скільки']
    }

    orig_str: str

    def __init__(self, txt: str):
        if type(txt) is not str:
            raise TypeError("'txt' should be a str")

        self.orig_str = txt

    def parse(self):
        question_type = self.determine_question_type()
        if question_type == ChoiceQuestion:
            return self.parse_choice_question()
        elif question_type == CanOrNotQuestion:
            return self.parse_canornot_question()
        elif question_type == WhyQuestion:
            return self.parse_why_question()
        elif question_type == WhichQuestion:
            return self.parse_which_question()
        elif question_type == HowMuchQuestion:
            return self.parse_howmuch_question()

    def parse_choice_question(self) -> ChoiceQuestion:
        work_str = transform_text(self.orig_str)

        first_delimeter = work_str.find(':')
        if first_delimeter == -1:
            first_delimeter = work_str.find('-')

        if first_delimeter != -1:
            work_str = work_str[first_delimeter + 1:]

        choices = work_str.split('чи')

        for i in range(len(choices)):
            choices[i] = choices[i].strip()

        if first_delimeter == -1:
            return ChoiceQuestion(self.orig_str, '<не вдалося виділити \'about\'>', choices)

        about = transform_text(self.orig_str)[0:first_delimeter]

        if about.startswith('як') or about.startswith('що'):
            about = about[2:].strip()

        if about.startswith('ким'):
            about = about[3:].strip()

        if len(about) >= 2 and about[0].isalpha() and about[1] == ' ':
            about = about[2:].strip()

        return ChoiceQuestion(self.orig_str, about, choices)

    def parse_canornot_question(self) -> CanOrNotQuestion:
        term = transform_text(self.orig_str)

        if term.startswith('чи'):
            term = term[3:]

        if term.startswith('не'):
            term = term[3:]

        return CanOrNotQuestion(self.orig_str, term)

    def parse_why_question(self) -> WhyQuestion:
        pass

    def parse_which_question(self) -> WhichQuestion:
        pass

    def parse_howmuch_question(self) -> HowMuchQuestion:
        pass

    def determine_question_type(self) -> type:
        transformed_txt = transform_text(self.orig_str)
        split_txt = transformed_txt.split(' ')
        words = list(filter(lambda x: x != '', split_txt))

        types_dict = {
            ChoiceQuestion:   0,
            CanOrNotQuestion: 0,
            WhyQuestion:      0,
            WhichQuestion:    0,
            HowMuchQuestion:  0
        }

        i = 0
        while i < len(words):
            for ques_type, keywords in self.questions_keywords.items():
                for keyword in keywords:
                    if isinstance(keyword, str):
                        if words[i] == keyword:
                            types_dict[ques_type] += 1
                    else:
                        assert False
            i += 1

        sorted_items = sorted(types_dict.items(), key=lambda x: x[1], reverse=True)
        picked_res = []
        for e in sorted_items:
            if len(picked_res) == 0:
                picked_res.append(e)
            elif e[1] == picked_res[-1]:
                picked_res.append(e)
            else:
                break

        if len(picked_res) != 1 or picked_res[0][1] == 0:
            raise ValueError("'txt' is not a valid question or function has failed to determine type of question")

        return picked_res[0][0]