from abc import ABC, abstractmethod

from old.question_type import transform_text

question_classes_list = []


class Question(ABC):
    orig_str: str

    def __init__(self, txt: str):
        self.orig_str = txt

    def get_orig_str(self):
        return self.orig_str

    @abstractmethod
    def get_type_str(self):
        pass

    @abstractmethod
    def parse(self):
        pass


class ChoiceQuestion(Question):
    def __init__(self, txt: str):
        super().__init__(txt)

        assert self.is_type_of_it(txt)

        self.parse()

    @staticmethod
    def is_type_of_it(txt: str) -> bool:
        pass

    def get_type_str(self):
        return 'CHOICE'

    def parse(self):
        work_str = transform_text(self.orig_str)

        first_delimeter = work_str.find(':')
        if first_delimeter == -1:
            first_delimeter = work_str.find('-')

        if first_delimeter != -1:
            work_str = work_str[first_delimeter + 1:]

        self.data['choices'] = work_str.split('чи')

        for i in range(len(self.data['choices'])):
            self.data['choices'][i] = self.data['choices'][i].strip()
