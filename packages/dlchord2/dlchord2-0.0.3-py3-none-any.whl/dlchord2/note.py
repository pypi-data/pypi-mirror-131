from dlchord2 import const
from dlchord2.parser.note_parser import NoteParser
from dlchord2.scale import Scale


class Note(object):
    def __init__(self, note_text, scale_text="C"):
        self.__raw_note_text = note_text
        self.__is_disabled = False

        parser = NoteParser()
        self.__note_data = parser.parse(self.__raw_note_text)

        if scale_text is None:
            scale_text = "C"

        self.__scale = Scale(scale_text)

    def __eq__(self, other):
        if not isinstance(other, Note):
            raise TypeError("{} オブジェクトとNoteオブジェクトを比較できません。".format(type(other)))

        if self.note_index == other.note_index:
            return True

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __unicode__(self):
        return self.raw_note_text

    def __str__(self):
        return self.raw_note_text

    def __repr__(self):
        return "<Note: {}>".format(self.raw_note_text)

    @classmethod
    def create_from_index_note(cls, index):
        """
        インデックスからノートを作成します。
        :param index: ノートの音階のインデックス
        :type index: int
        :return: ノート
        :rtype: Note
        """
        if index < 0 or index > 11:
            raise ValueError("テンションノートインデックスに指定できるのは、0から11までの数値です")

        note_text = const.C_MAJOR_SCALE[index]
        note = cls(note_text)
        return note

    @classmethod
    def create_from_tension(cls, tension_text):
        """
        テンションノートテキストからノートを作成します
        :param tension_text: テンションノートテキスト
        :type tension_text: str
        :return: テンションノート
        :rtype: Note
        """

        if tension_text not in const.TENSION_TO_INDEX:
            raise ValueError("解析できない不明なテンションノート: {} が渡されました".format(tension_text))

        tension_note = cls.create_from_index_note(const.TENSION_TO_INDEX[tension_text])
        return tension_note

    def transposed(self, steps, scale_text=None):
        """
        ノートを転調します。
        このノートを直接変更はせずに、転調したノートを新たに生成し、返します。
        scale_textがNoneの場合は、現在のノートに設定されているスケールを使用します。
        :param steps: 転調する数
        :type steps: int
        :param scale_text: 転調後のノートに適用するスケール
        :type scale_text: str
        :return: 転調後のノート
        :rtype: Note

        """

        transposed_note_index = (self.note_index + steps) % 12
        if scale_text is None:
            scale_text = self.__scale.scale_text

        transposed_note = Note(self.__scale.get_note_text_absolute(transposed_note_index), scale_text)
        transposed_note.disabled = self.disabled
        return transposed_note

    @property
    def disabled(self):
        """
        ノートが無効になっているかを取得します。
        :return: ノートが無効になっているか
        :rtype: bool
        """
        return self.__is_disabled

    @disabled.setter
    def disabled(self, disabled):
        """
        ノートを無効にするかを設定します。
        :param disabled: ノートを無効にする場合はTrue, それ以外はFalse
        :type disabled: bool
        """
        self.__is_disabled = disabled

    @property
    def note_index(self):
        """
        ノートのインデックスを取得します。
        ノートのインデックスは、Cを0として、Bを11とする音階のインデックスです。
        :return: ノートのインデックス
        :rtype: int
        """
        return self.__note_data.note_index

    @property
    def raw_note_text(self):
        """
        正規化されていないノートのテキストを取得します。
        :return: 正規化されていないノートのテキスト
        :rtype: str
        """
        return self.__raw_note_text

    @property
    def normed_note_text(self):
        """
        このノートに設定されているスケールで正規化したノートのテキストを取得します。
        :return: スケールで正規化したノートのテキスト
        :rtype: str
        """
        return self.scale.get_note_text_absolute(self.note_index)

    @property
    def accidentals(self):
        """
        調号を取得します。
        :return: 調号
        :rtype: Accidentals
        """
        return self.__note_data.accidentals

    @property
    def scale(self):
        """
        このノートに設定されているスケールを取得します。
        :return: このノートに設定されているスケール
        :rtype: Scale
        """
        return self.__scale

