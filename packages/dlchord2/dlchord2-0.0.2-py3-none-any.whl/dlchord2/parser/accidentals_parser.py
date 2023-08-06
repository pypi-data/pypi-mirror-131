from enum import Enum

from dlchord2.const import ACCIDENTALS_SHARP, ACCIDENTALS_FLAT
from dlchord2.exceptions.accidentals_exceptions import AccidentalsParseError


class AccidentalsType(Enum):
    """
    調号の種類を表す列挙体
    """
    NONE = 0
    SHARP = 1
    FLAT = 2


class AccidentalsParseData(object):
    """
    調号を解析したデータを格納するクラス
    """

    def __init__(self, accidentals, accidentals_type, transpose_num):
        self._accidentals = accidentals
        self._accidentals_type = accidentals_type
        self._transpose_num = transpose_num

    @property
    def accidentals(self):
        """
        調号のテキストを取得します。
        :return: 生の調号のテキスト
        :rtype: str
        """
        return self._accidentals

    @property
    def accidentals_type(self):
        """
        調号の種類を取得します。
        :return: 調号の種類
        :rtype: AccidentalsType
        """
        return self._accidentals_type

    @property
    def transpose_num(self):
        """
        調号の変化量を取得します。
        :return: 調号の変化量
        :rtype: int
        """
        return self._transpose_num


class AccidentalsParser(object):
    """
    調号を解析するクラス
    """

    def parse(self, accidentals_text):
        """
        調号を解析します。
        :param accidentals_text: ルート音を含まない調号テキスト
        :type accidentals_text: str
        :return: 調号解析データ
        :rtype: AccidentalsParseData
        """

        sharp_num = accidentals_text.count(ACCIDENTALS_SHARP)
        flat_num = accidentals_text.count(ACCIDENTALS_FLAT)

        if sharp_num > 0 and flat_num > 0:
            raise AccidentalsParseError("異なる調号は重複して存在することはできません。")

        accidentals_type = AccidentalsType.NONE
        trans_num = 0
        if sharp_num > 0:
            accidentals_type = AccidentalsType.SHARP
            trans_num = sharp_num

        elif flat_num > 0:
            accidentals_type = AccidentalsType.FLAT
            trans_num = -flat_num

        accidentals_parse_data = AccidentalsParseData(
            accidentals_text,
            accidentals_type,
            trans_num)
        return accidentals_parse_data
