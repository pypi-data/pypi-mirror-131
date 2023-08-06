from dlchord2 import const
from dlchord2.accidentals import Accidentals
from dlchord2.exceptions.note_exceptions import NoteParseError


class NoteParseData(object):
    """
    ノート解析データを格納するクラス
    """
    def __init__(self, accidentals, note_index):
        self._accidentals = accidentals
        self._note_index = note_index

    @property
    def accidentals(self):
        """
        ノートの調号を取得します。
        :return: ノートの調号
        :rtype: Accidentals
        """
        return self._accidentals

    @property
    def note_index(self):
        """
        ノートの音階インデックスを取得します。
        このインデックスは調号による変化量を含んでいます。
        :return: ノートの音階インデックス
        :rtype: int
        """
        return self._note_index


class NoteParser(object):
    """
    ノートを解析するクラス
    """

    def parse(self, raw_note_text):
        """
        生のノートテキストから、調号、ルート音を解析します。
        :param raw_note_text: 生のノートテキスト
        :type raw_note_text: str
        :return: ノート解析データ
        :rtype: NoteParseData
        """

        note_text_length = len(raw_note_text)
        if note_text_length == 0:
            raise NoteParseError("ノートのテキストが入力されていません")

        root_note_text = raw_note_text[0]
        if root_note_text not in const.TONE_TO_INDEX:
            raise NoteParseError("存在しないルート音です。")

        note_index = const.TONE_TO_INDEX[root_note_text]
        accidentals = Accidentals(raw_note_text[1:])

        note_index = (note_index + accidentals.transpose_num) % 12
        note_parse_data = NoteParseData(accidentals, note_index)

        return note_parse_data
