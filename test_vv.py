import unittest
from old.question_type import QuestionType
from old.question_type import determine_question_type


class TestQuestionTypes(unittest.TestCase):

    def test_correct_questions(self):
        test_cases = [
            ('Як краще досягати успіху - самотужки чи в колективі?', QuestionType.CHOICE),
            ('Що ж важче: будувати надхмарні споруди чи жити в них?', QuestionType.CHOICE),

            ('Чи можливе ідеальне суспільство без ідеальної сім\'ї?', QuestionType.CAN_OR_NOT),
            ('Чи має право наука абстрагуватися від питань моралі?', QuestionType.CAN_OR_NOT),

            ('За якими критеріями краще обирати професію?', QuestionType.WHICH),
            ('Які чинники впливають на формування людини як особистості?', QuestionType.WHICH),
            ('Що руйнує сім’ю?', QuestionType.WHICH),
            ('Що робить групу людей нацією?', QuestionType.WHICH),
            ('У чому цінність мистецтва?', QuestionType.WHICH),

            ('Чому занепадають цивілізації?', QuestionType.WHY),
            ('Чому важливо знати уроки історії?', QuestionType.WHY),

            ('На скільки людині варто дослухатися до думки оточення про неї?', QuestionType.HOW_MUCH),
        ]

        for txt, type in test_cases:
            self.assertEqual(determine_question_type(txt), type, msg='Testing: "' + txt + '"')

    @unittest.skip("Складно відрізнити. Треба змінювати алгоритм")
    def test_non_questions(self):
        test_cases = [
            '213124114',
            'ADJNV NFlS FAD KLAD SALD',
            'ДЛВАЫ ФЫЛДЖВЬ',
            'лырдв жжл ываыв ау  у  у'
        ]

        for txt in test_cases:
            self.assertRaises(ValueError, determine_question_type, txt)

    @unittest.skip("Складно відрізнити. Треба змінювати алгоритм")
    def test_non_vv_question(self):
        test_cases = [
            'Де скласти іспит в останніх числах жовтня?',
            'у місті Києві:',
            'Київський національний університет будівництва і архітектури – 34',
            'Запрошуємо ознайомитися з відповідями на поширені запитання: ',
            'Про затвердження Графіка особистого прийому громадян керівництвом і посадовими особами структурних підрозділів апарату Національної комісії зі стандартів державної мови під час дії карантинних обмежень',
            'Національна комісія зі стандартів державної мови (далі - Комісія) здійснює опрацювання та утвердження стандартів української мови як державної, розроблення методів перевірки рівня її володіння.'
            'Дава́ти (підно́сити) гарбуза́ — відмовляти кому-небудь у сватанні.',
            'Горо́х з капу́стою — що-небудь таке, в чому важко розібратися; щось невпорядковане, незрозуміле, наплутане. ',
            'Які з цих висловів знали?',
            'Якими б доповнили цей перелік?',
            'Де ти з\'їси цю чашу жиру?',
            'Правила вживання «приймати»'
        ]

        for txt in test_cases:
            self.assertRaises(ValueError, determine_question_type, txt)

    def test_non_str_questions(self):
        test_cases = [
            10,
            9.8,
            2 + 3j,
            [],
            [10, 20],
            ['a', 'b'],
            True,
            False,
            None
        ]

        for txt in test_cases:
            self.assertRaises(TypeError, determine_question_type, txt)
