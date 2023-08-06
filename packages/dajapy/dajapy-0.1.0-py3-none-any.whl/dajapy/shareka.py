from collections import Counter

from sudachipy import dictionary, tokenizer

tokenizer_obj = dictionary.Dictionary().create()


replace_words = [
    ['。', ''],
    ['、', ''],
    [',', ''],
    ['.', ''],
    ['!', ''],
    ['！', ''],
    ['・', ''],
    ['「', ''],
    ['」', ''],
    ['「', ''],
    ['｣', ''],
    ['『', ''],
    ['』', ''],
    [', ', ''],
    ['　', ''],
    ['ッ', ''],
    ['ャ', 'ヤ'],
    ['ュ', 'ユ'],
    ['ョ', 'ヨ'],
    ['ァ', 'ア'],
    ['ィ', 'イ'],
    ['ゥ', 'ウ'],
    ['ェ', 'エ'],
    ['ォ', 'オ'],
    ['ー', '']
]


class Shareka:
    def __init__(self, sentence, kaburi=2):
        self.sentence = sentence
        self.kaburi = kaburi

        self.yomi = None
        self.divided_sentence = None
        self.max_dup = None
        self.is_dajare = None

    def divide(self):
        yomi = ''
        tokens = tokenizer_obj.tokenize(
            text=self.sentence,
            mode=tokenizer.Tokenizer.SplitMode.C)
        for t in tokens:
            yomi += t.reading_form()
        for r in replace_words:
            yomi = yomi.replace(r[0], r[1])
        self.yomi = yomi

        divided_sentence = []
        repeat_num = len(yomi) - (self.kaburi - 1)
        for i in range(repeat_num):
            divided_sentence.append(yomi[i:i+self.kaburi])
        self.divided_sentence = divided_sentence

    def evaluate(self):
        sentence = self.divided_sentence
        if len(sentence) == 0:
            self.is_dajare = False
            return

        collection = Counter(sentence)
        max_dup = collection.most_common()[0][1]
        self.max_dup = max_dup
        max_dup_rate = max_dup / len(sentence)
        if max_dup > 1 and max_dup_rate <= 0.5:
            self.is_dajare = True
            return

        self.is_dajare = False

    def to_dict(self):
        return {
            'sentence': self.sentence,
            'kaburi': self.kaburi,
            'yomi': self.yomi,
            'divided_sentence': self.divided_sentence,
            'max_dup': self.max_dup,
            'is_dajare': self.is_dajare
        }


if __name__ == '__main__':
    dajare = "布団がふっとんだ。"
    # dajare = 'メンターランチで食べたラーメン'
    dajare = 'ハエは速え～'
    shareka = Shareka(dajare, 2)
    shareka.divide()
    shareka.evaluate()
    print(shareka.to_dict())
