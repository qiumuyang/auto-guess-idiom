from pypinyin import load_phrases_dict

fix_string = '''
层出迭见 céng chū dié xiàn
层出叠见 céng chū dié xiàn
层见错出 céng xiàn cuò chū
层见叠出 céng xiàn dié chū
情见势竭 qíng xiàn shì jié
时隐时见 shí yǐn shí xiàn
闲见层出 xián xiàn céng chū

犯而勿校 fàn ér wù jiào
同年而校 tóng nián ér jiào
校短推长 jiào duǎn tuī cháng
铢铢校量 zhū zhū jiào liàng

口谐辞给 kǒu xié cí jǐ

冯河暴虎 píng hé bào hǔ
十寒一暴 shí hán yī pù

剪发被褐 jiǎn fà pī hè
夜行被绣 yè xíng pī xiù

薄情无义 bó qíng wú yì
道微德薄 dào wēi dé bó
德薄才鲜 dé bó cái xiǎn
德浅行薄 dé qiǎn xíng bó
雕虫薄技 diāo chóng bó jì
根孤伎薄 gēn gū jì bó
寡情薄意 guǎ qíng bó yì
厚往薄来 hòu wǎng bó lái
门衰祚薄 mén shuāi zuò bó
命薄缘悭 mìng bó yuán qiān
轻薄无礼 qīng bó wú lǐ
轻薄无行 qīng bó wú xíng
轻薄无知 qīng bó wú zhī
轻赋薄敛 qīng fù bó liǎn
轻傜薄赋 qīng yāo bó fù
轻徭薄赋 qīng yāo bó fù
轻繇薄赋 qīng yāo bó fù
轻徭薄税 qīng yáo bó shuì
日薄桑榆 rì bó sāng yú
日薄虞渊 rì bó yú yuān
身微力薄 shēn wēi lì bó
势孤力薄 shì gū lì bó
帏薄不修 wéi bó bù xiū
西山日薄 xī shān rì bó
轻口薄舌 qīng kǒu bó shé

得薄能鲜 dé bó néng xiǎn
鲜廉寡耻 xiǎn lián guǎ chǐ
'''.strip()


def fix():
    check = {}

    dic = {}
    for line in fix_string.splitlines():
        if line.isspace():
            continue

        _ = line.split(' ')
        word = _[0]
        syllables = _[1:]
        dic[word] = [[_] for _ in syllables]
        check[word] = ' '.join(syllables)

    load_phrases_dict(dic)


fix()
