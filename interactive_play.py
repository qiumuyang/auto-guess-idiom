from random import choice

import pyperclip
from pypinyin import lazy_pinyin

from idiom import idioms, judge_answer

while 1:
    word = choice(idioms)
    pinyin = lazy_pinyin(word)
    print(' '.join(['W' * len(_) for _ in pinyin]))

    pyperclip.copy(''.join([str(len(_)) for _ in pinyin]))
    joined = ' '.join(pinyin)

    guess_time = 0
    answer = ''
    while answer != joined:
        answer = input('> ')
        guess_time += 1
        judge = judge_answer(joined, answer)
        pyperclip.copy(judge)
        print('  ' + judge)
    print('times: %d, %s' % (guess_time, word))
