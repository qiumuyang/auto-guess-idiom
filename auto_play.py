from random import sample, seed

from pypinyin import lazy_pinyin
from tqdm import tqdm

import auto_guess
from idiom import idioms, judge_answer

auto_guess.log = False
seed(114514)


def test(test_percent: float = 1):
    testcases = sample(idioms, k=round(len(idioms) * test_percent))

    stat = {}
    guess_total = 0
    with tqdm(total=len(testcases), unit='word', desc='Guess') as pbar:
        for i, word in enumerate(testcases):
            pinyin = lazy_pinyin(word)
            truth = ' '.join(pinyin)
            auto = auto_guess.AutoIdiom()

            # start
            length = [len(_) for _ in pinyin]
            answer = auto.start(length)

            guess_time = 1
            while 1:
                judge = judge_answer(truth, answer)
                # print(answer)
                # print(judge)
                if answer == truth:
                    break
                answer = answer.replace(' ', '')
                judge = judge.replace(' ', '')
                stop, answer = auto.update(answer, judge)
                guess_time += 1

            stat.setdefault(guess_time, set()).add(word)
            guess_total += guess_time
            pbar.update(1)
            pbar.set_postfix({'average': '%.4f' % (guess_total / (i + 1))})

    for i, words in sorted(stat.items(), key=lambda t: t[0]):
        print(i, len(words), '' if len(words) > 10 else ' '.join(words))

    print('average:', '%.4f' % (guess_total / len(testcases)))


if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--weight', nargs=len(auto_guess.weights), type=float)
    parser.add_argument('-p', '--percent', type=float, default=0.2)
    args = parser.parse_args(sys.argv[1:])

    # auto_guess.enable_dynamic = args.dynamic
    if args.weight:
        auto_guess.weights = args.weight
    print('[Weight] ', auto_guess.weights)
    test(args.ratio)
