import pyperclip

from auto_guess import AutoIdiom
from idiom import BAD, GOOD, PART

auto: AutoIdiom = None
pinyin = ''
prompt = 'state > '

while 1:
    if auto is not None:
        print(' ' * len(prompt) + pinyin)
        state = input(prompt).replace(' ', '')
        assert all(_ in [BAD, GOOD, PART] for _ in state)

        stop, pinyin = auto.update(pinyin, state)
        pyperclip.copy(pinyin)
        pinyin = pinyin.replace(' ', '')
        if stop:
            auto = None
    else:
        x = input('syllables > ')
        auto = AutoIdiom()
        pinyin = auto.start([int(_) for _ in x])
        pyperclip.copy(pinyin)
        pinyin = pinyin.replace(' ', '')
