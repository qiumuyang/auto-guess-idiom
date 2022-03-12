import json
import string
from pathlib import Path

from fix_pinyin import fix

fix()

idiom_path = Path('data/idiom.json')
syllable_path = Path('data/syllables.json')

with idiom_path.open(encoding='utf8') as f:
    idioms = [i_dict['word']
              for i_dict in json.load(f)
              if len(i_dict['word']) == 4]

with syllable_path.open(encoding='utf8') as f:
    syllables = json.load(f)

GOOD = '1'
BAD = '0'
PART = '2'
UNKNOWN = '3'


def judge_answer(_correct: str, _answer: str) -> str:
    assert len(_correct) == len(_answer), 'correct=' + _correct + ' answer=' + _answer

    length = len(_correct)
    correct = list(_correct)
    answer = list(_answer)
    ret = [BAD] * length

    for i in range(length):
        if correct[i] == answer[i]:
            if correct[i] == ' ':
                ret[i] = ' '
            else:
                ret[i] = GOOD
            correct[i] = '#'
            answer[i] = '#'

    for letter in string.ascii_lowercase:
        while letter in correct and letter in answer:
            idx_c = correct.index(letter)
            idx_a = answer.index(letter)
            ret[idx_a] = PART
            correct[idx_c] = '#'
            answer[idx_a] = '#'

    return ''.join([_ for _ in ret])
