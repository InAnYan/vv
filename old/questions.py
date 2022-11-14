from old.question_type import QuestionType, transform_text


class Question:
    type: QuestionType
    data: dict

    def __init__(self, txt: str):
        self.type = self.determine_type(txt)
        self.orig_str = txt

        if self.type == QuestionType.CHOICE:
            self.parse_choice_question()
        elif self.type == QuestionType.WHY:
            self.parse_why_question()
        elif self.type == QuestionType.WHICH:
            self.parse_which_question()
        elif self.type == QuestionType.CAN_OR_NOT:
            self.parse_canornot_question()
        elif self.type == QuestionType.HOW_MUCH:
            self.parse_howmuch_question()

    def get_type(self):
        return self.type

    def get_orig_str(self):
        return self.orig_str

    def parse_choice_question(self):
        work_str = transform_text(self.orig_str)

        first_delimeter = work_str.find(':')
        if first_delimeter == -1:
            first_delimeter = work_str.find('-')

        if first_delimeter != -1:
            work_str = work_str[first_delimeter + 1:]

        self.data['choices'] = work_str.split('чи')

        for i in range(len(self.data['choices'])):
            self.data['choices'][i] = self.data['choices'][i].strip()
