from dlchord2 import const
from dlchord2.exceptions.scale_exceptions import ScaleNotFoundError


class Scale(object):
    def __init__(self, scale_text):
        self.__scale_text = scale_text
        if self.__scale_text not in const.SCALE_PATTERN:
            raise ScaleNotFoundError("指定したスケール {} が見つかりません。".format(scale_text))

        self.__scale_list = const.SCALE_PATTERN[self.__scale_text]

    def __str__(self):
        return self.scale_text

    def __unicode__(self):
        return self.scale_text

    def __eq__(self, other):
        if not isinstance(other, Scale):
            raise TypeError("{} オブジェクトとScaleオブジェクトを比較できません".format(type(other)))

        if self.scale_text == other.scale_text and self.scale_list == other.scale_list:
            return True

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<Scale: {}>".format(self.scale_text)

    @property
    def scale_text(self):
        """
        スケールをテキストで取得します。
        :return: スケール
        :rtype: str
        """
        return self.__scale_text

    @property
    def scale_list(self):
        """
        スケールのノートのテキストリストを取得します。
        :return: ノートのテキストリスト
        :rtype: list[str]
        """
        return self.__scale_list

    def get_note_text(self, index):
        """
        指定したインデックスのノートのテキストを取得します。
        インデックスは、現在設定されているスケールから見たインデックスを指します。
        indexが0でCスケールの場合、取得されるノートテキストはCになります。
        indexが0でDbスケールの場合、取得されるノートテキストはDbになります。
        :param index: 現在設定されているスケールから見たインデックス
        :type index: int
        :return: ノートのテキスト
        :rtype: str
        """
        if index < 0 or index > 11:
            raise ScaleNotFoundError("範囲外のインデックスが指定されました。")

        return self.__scale_list[index]

    def get_note_text_absolute(self, absolute_index):
        """
        現在のスケールを移動させ、Cが先頭になるように並びかえられたスケールで、ノートのテキストを取得します。
        indexが0でCスケールの場合、取得されるノートテキストはCになります。
        indexが0でDbスケールの場合、取得されるノートテキストはCになります。
        :param absolute_index:
        :type absolute_index:
        :return: ノートのテキスト
        :rtype: str
        """
        if absolute_index < 0 or absolute_index > 11:
            raise ScaleNotFoundError("範囲外のインデックスが指定されました。")

        index = (absolute_index - const.SCALE_TO_INDEX[self.scale_text]) % 12
        return self.__scale_list[index]
