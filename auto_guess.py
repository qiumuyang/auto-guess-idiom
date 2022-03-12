import re
import string
from collections import Counter
from typing import Dict, Iterable, List, Tuple

from pypinyin import lazy_pinyin

from idiom import idioms, GOOD, PART, BAD, UNKNOWN

all_pinyin = {word: lazy_pinyin(word) for word in idioms}

log = True
weights = [1, 1.595]


def get_result_by_scores(word_pinyin: Dict[str, str]) -> Tuple[str, str]:
    word_length = len(list(word_pinyin.values())[0])

    # calculate the time of appearance for each letter in each position
    appearance = [[0 for _ in range(26)] for _ in range(word_length)]
    for pinyin in word_pinyin.values():
        for i, c in enumerate(pinyin):
            appearance[i][ord(c) - ord('a')] += 1

    freq_scores = []
    variance_scores = []

    pinyin_list = list(word_pinyin.values())
    for pinyin in pinyin_list:
        freq_score = 0
        variance_score = len(set(pinyin))
        for i, c in enumerate(pinyin):
            freq_score += appearance[i][ord(c) - ord('a')]

        freq_scores.append(freq_score)
        variance_scores.append(variance_score)

    m_freq = max(freq_scores)
    m_var = max(variance_scores)
    freq_scores = list(map(lambda x: x / m_freq * weights[0], freq_scores))
    variance_scores = list(map(lambda x: x / m_var * weights[1], variance_scores))
    scores = list(map(lambda x, y: x + y, freq_scores, variance_scores))

    idx = scores.index(max(scores))
    word = list(word_pinyin.keys())[idx]
    return word, ' '.join(lazy_pinyin(word))


class AutoIdiom:
    def __init__(self) -> None:
        self.candidates = {}

    def start(self, syllables: Iterable[int]) -> str:
        self.candidates = {
            word: ''.join(all_pinyin[word])
            for word in self.filter_by_syllable(syllables)
        }
        ret = get_result_by_scores(self.candidates)
        if log:
            print('[rest]  %d' % len(self.candidates))
            print('[guess] %s %s' % (ret[0], ret[1]))
        return ret[1]

    @classmethod
    def filter_by_syllable(cls, lengths: Iterable[int]) -> List[str]:
        tuples = list(filter(lambda tup: lengths == [len(_) for _ in tup[1]], all_pinyin.items()))
        return list(zip(*tuples))[0]

    def update(self, guess: str, state: str) -> Tuple[bool, str]:
        # check state foreach letter
        char_state = {s: UNKNOWN for s in string.ascii_lowercase}
        lower_bound = {s: 0 for s in string.ascii_lowercase}
        upper_bound = {s: float('inf') for s in string.ascii_lowercase}
        priority = {
            BAD: 0,
            GOOD: 2,
            PART: 1,
            UNKNOWN: -1,
        }
        for c, s in zip(guess, state):
            if priority[s] > priority[char_state[c]]:
                char_state[c] = s
            if s == GOOD or s == PART:
                lower_bound[c] += 1
        for c, s in zip(guess, state):
            if s == BAD:
                upper_bound[c] = lower_bound[c]

        bad = ''.join([_ for _, s in char_state.items() if s == BAD])
        regex_parts = []
        for c, s in zip(guess, state):
            if s == GOOD:
                regex_parts.append(c)
            elif s == PART or s == BAD:
                regex_parts.append('[^%s]' % (c + bad))
            else:
                regex_parts.append('.')
        regex = ''.join(regex_parts)
        # print(regex)

        pop_keys = []
        for word, pinyin in self.candidates.items():
            if not re.fullmatch(regex, pinyin):  # remove bad pattern
                pop_keys.append(word)
            elif pinyin == guess:  # remove this guess
                pop_keys.append(word)
            else:  # remove letter-count not satisfied
                counter = Counter(pinyin)
                for c in lower_bound:
                    if not (lower_bound[c] <= counter.get(c, 0) <= upper_bound[c]):
                        pop_keys.append(word)
                        break

        for key in pop_keys:
            self.candidates.pop(key)

        if not self.candidates:
            return True, ''

        ret = get_result_by_scores(self.candidates)

        if log:
            print('[rest]  %d' % len(self.candidates))
            print('[guess] %s %s' % (ret[0], ret[1]))
        return len(self.candidates) == 1, ret[1]
