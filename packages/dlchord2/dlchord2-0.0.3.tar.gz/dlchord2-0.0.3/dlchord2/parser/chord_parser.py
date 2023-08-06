from dlchord2 import const


class ChordParseData(object):
    def __init__(self, root_text, bass_text, quality_text):
        self.__root_text = root_text
        self.__bass_text = bass_text
        self.__quality_text = quality_text

    @property
    def root_text(self):
        return self.__root_text

    @property
    def bass_text(self):
        return self.__bass_text

    @property
    def quality_text(self):
        return self.__quality_text


class ChordParser(object):
    """
    コードをルート、クオリティ、ベースに分解するクラス。
    """

    def parse(self, chord_text):
        split_text = chord_text.split("/")
        root_text = chord_text[0]
        bass_text = ""
        accidentals_text = ""

        if len(split_text) > 1:
            bass_text = split_text[1]

        res = split_text[0][1:]
        for i in range(len(res)):
            if res[i] != const.ACCIDENTALS_SHARP and res[i] != const.ACCIDENTALS_FLAT:
                break
            accidentals_text += res[i]

        root_text += accidentals_text
        quality_text = res[len(accidentals_text):]

        # ベースがない場合はルート音がベースになります
        if bass_text == "":
            bass_text = root_text

        return ChordParseData(root_text, bass_text, quality_text)

