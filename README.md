# Генератор власних висловлень
Дуже дивна програма, але цікава.

Не вміє придумувати аргументи та приклади, бере інформацію з Інтернету.

No AI.

## Ідея
Коли мене вчили писати ВВ у 2022 році, я помітив, що його можна записати за допомогою EBNF.

Різні типи питань мають різну структуру тез.

## Алгоритм
1. З'ясувати тип питання. (Детальніше: `questions.py`).
2. Відповідно до типу питання виокремити значущі частини.
3. Згенерувати тезу.
4. Згенерувати аргумент №1.
5. Згенерувати аргумент №2.
6. Згенерувати приклад №1.
7. Згенерувати приклад №1.
8. Згенерувати висновки.

При створенні аргументів та прикладів програма обирає слово-маркер та бере інформацію з Інтернету.

## Файли
- `blocks.py`: генератор ВВ та його частин.
- `bnf.txt`: спроба описати структуру ВВ у BNF.
- `finder.py`: шукач інформації з Інтернету.
- `markers.py`: слова-маркери для частин ВВ.
- `questions.py`: основні типи питань (тут багато задокументовано).
- `questions_parser.py`: парсер питань.

