from dlchord2.parser.accidentals_parser import AccidentalsParser


class Accidentals(object):
    def __init__(self, accidentals):
        """
        :param accidentals: ルート音を含まない、調号のみのテキスト
        :type accidentals: str
        """

        parser = AccidentalsParser()
        self.__accidentals_data = parser.parse(accidentals)

    def __eq__(self, other):
        if not isinstance(other, Accidentals):
            raise TypeError("{} オブジェクトとAccidentalsオブジェクトを比較できません".format(type(other)))

        if self.transpose_num == other.transpose_num:
            return True

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __unicode__(self):
        return self.text

    def __str__(self):
        return self.text

    def __repr__(self):
        return "<Accidentals: {}>".format(self.text)

    @property
    def text(self):
        """
        調号のテキストを取得します。
        :return: 調号のテキスト
        :rtype: str
        """
        return self.__accidentals_data.accidentals

    @property
    def type(self):
        """
        調号の種類を取得します。
        :return: 調号の種類
        :rtype: AccidentalsType
        """
        return self.__accidentals_data.accidentals_type

    @property
    def transpose_num(self):
        """
        調号の変化量を取得します。
        :return: 調号の変化量
        :rtype: int
        """
        return self.__accidentals_data.transpose_num
