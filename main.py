import random

import bs4 as bs4

from vv.blocks import VV


def test(question: str):
    vv = VV(question)
    print(vv.generate())


def main2():
    questions_choice = [
        'Як краще досягати успіху - самотужки чи в колективі?',
        'Яка праця більше варта поваги – фізична чи інтелектуальна?',
        'Ким краще бути в сучасному світі – романтиком чи раціоналістом?',
        'Що ж важче: будувати надхмарні споруди чи жити в них?',
        'Вища освіта всім чи її мають здобувати лише кращі?',
    ]

    for e in questions_choice:
        test(e)

    print('')

    questions_can_or_not = [
        'Чи вища освіта може замінити практичний досвід?',
        'Чи має право наука абстрагуватися від питань моралі?',
        'Чи можливе ідеальне суспільство без ідеальної сім’ї?',
        'Чи можна подолати проблему батьків / дітей (старшого / молодшого покоління)?',
        'Чи можлива в суспільному житті гармонія?',
        'Чи не призведе розвиток науки до деградації духовності людини?'
    ]

    for e in questions_can_or_not:
        test(e)


def main():
    test('Як краще досягати успіху - самотужки чи в колективі?',)


if __name__ == '__main__':
    main()