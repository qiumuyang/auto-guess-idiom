# Auto Guess Idiom

自动完成拼音猜成语

> 灵感来源于 Wordle 及其衍生版本 [拼音猜成语](https://pinyincaichengyu.com/)
>
> 数据来源于仓库 [chinese-xinhua](https://github.com/pwxcoo/chinese-xinhua)

### 1 游戏规则

根据已有猜测和对应提示，在若干步内猜出目标成语

提示类型:

+ 0 - 字母不存在于成语中
+ 1 - 字母和位置正确
+ 2 - 字母存在但位置不正确

### 2 游玩模式

运行以下命令即可开始游玩

```
python interactive_play.py
```

+ 输出：谜面(字母个数由若干个'W'给出)，提示(由'012'给出)
+ 输入：小写拼音

**注意：这里没有检测输入的合法性，同时谜面和提示将会同步复制到剪切板**

### 3 解答模式

运行以下命令即可开始自动答题

```
python interactive_auto_guess.py
```

+ 输出：剩余候选成语个数，推荐猜测的成语
+ 输入：字母个数(e.g.'2344')，上轮推荐猜测成语的答题情况(e.g. '01200000')

**注意：在给出推荐成语后，该成语的拼音将会复制到剪切板**

### 4 其他

+ 同时运行以上两种模式，可以便捷地达成左右互搏(~~不是~~)
+ `auto_play.py`实现了自动左右互搏并统计了平均猜出成语所用次数，可以借此判断`auto_guess.py`中候选成语选择函数参数的有效性