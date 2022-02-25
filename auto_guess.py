import re
import string
from collections import Counter
from typing import Dict, Iterable, List, Tuple

import numpy
from numpy import ndarray
from pypinyin import lazy_pinyin

from idiom import idioms, GOOD, PART, BAD

all_pinyin = {word: lazy_pinyin(word) for word in idioms}

log = True


def get_entropy(appearance: List[List[int]]) -> ndarray:
    arr = numpy.array(appearance, dtype='int')
    total = numpy.sum(arr, axis=1)
    if numpy.any(total) == 0:
        total = numpy.ones_like(total)

    total = numpy.expand_dims(total, axis=1).repeat(arr.shape[1], axis=1)
    prob = arr / total
    log_prob = numpy.where(prob > 0, numpy.log2(prob), 0)
    return -numpy.sum(prob * log_prob, axis=1)


def get_result_by_scores(word_pinyin: Dict[str, str], weights: Tuple[float] = (1, 0.5, 0.6)) -> Tuple[str, str]:
    # weights are set arbitrarily

    word_count = len(word_pinyin)
    word_length = len(list(word_pinyin.values())[0])

    # calculate the time of appearance for each letter in each position
    appearance = [[0 for _ in range(26)] for _ in range(word_length)]
    for pinyin in word_pinyin.values():
        for i, c in enumerate(pinyin):
            appearance[i][ord(c) - ord('a')] += 1

    entropy = get_entropy(appearance)
    scores = {}
    for word, pinyin in word_pinyin.items():
        entropy_score = 0
        freq_score = 0
        for i, c in enumerate(pinyin):
            app_at_i = appearance[i].copy()
            app_at_i[ord(c) - ord('a')] = 0
            entropy_score = 0
            freq_score = 0
            entropy_score += entropy[i] - get_entropy([app_at_i])[0]
            freq_score += appearance[i][ord(c) - ord('a')] / word_count / word_length
        variance_score = len(set(pinyin)) / len(pinyin)

        extra_freq = min(1.0, 10 / word_count)
        extra_var = max(1.0, 0.05 * word_count)
        scores[word] = (entropy_score * weights[0],
                        freq_score * weights[1] * extra_freq,
                        variance_score * weights[2] * extra_var)

    tup = max(list(scores.items()), key=lambda t: sum(t[1]))
    word = tup[0]
    return word, ' '.join(lazy_pinyin(word))


class AutoIdiom:
    def __init__(self) -> None:
        self.all_pinyin = all_pinyin
        self.candidates = {}
        self.last_length = 0

    def start(self, syllables: Iterable[int]) -> str:
        self.candidates = {
            word: ''.join(self.all_pinyin[word])
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
        char = {s: 3 for s in string.ascii_lowercase}
        contain = {s: 0 for s in string.ascii_lowercase}
        priority = [0, 2, 1, -1]
        for c, s in zip(guess, state):
            s = int(s)
            if priority[s] > priority[char[c]]:
                char[c] = s
            if s == 2:
                contain[c] += 1

        bad = ''.join([_ for _, s in char.items() if s == 0])
        regex_parts = []
        for c, s in zip(guess, state):
            if s == GOOD:
                regex_parts.append(c)
            elif s == PART:
                regex_parts.append('[^%s]' % (c + bad))
            elif s == BAD and bad:  # in case bad is empty string
                regex_parts.append('[^%s]' % bad)
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
                for c, num in contain.items():
                    if counter.get(c, 0) < num:
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
