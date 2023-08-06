from dlchord2.note import Note
from dlchord2.parser.quality_parser import QualityParser


class Quality(object):
    def __init__(self, quality_text):
        self.__raw_quality_text = quality_text
        parser = QualityParser()
        self.__quality_data = parser.parse(quality_text)

        self.__tension_notes = [Note.create_from_tension(tension)
                                for tension in self.__quality_data.tensions]
        self.__tension_parentheses_notes = [Note.create_from_tension(tension)
                                            for tension in self.__quality_data.tensions_parentheses]
        self.__add_tension_notes = [Note.create_from_tension(tension)
                                    for tension in self.__quality_data.add_tensions]

    @property
    def raw_quality_text(self):
        """
        生のクオリティテキストを取得します。
        :return: 生のクオリティテキスト
        :rtype: str
        """
        return self.__raw_quality_text

    @property
    def qualities(self):
        """
        クオリティのリストを取得します。
        :return: クオリティのリスト
        :rtype: list[str]
        """
        return self.__quality_data.qualities

    @property
    def tension_parent_notes(self):
        """
        かっこ内のテンションノートのリストを取得します。
        :return: かっこ内のテンションノートのリスト
        :rtype: list[Note]
        """
        return self.__tension_parentheses_notes

    @property
    def tension_notes(self):
        """
        かっこ外のテンションノートのリストを取得します。
        このテンションノートリストは、テンションのヒエラルキー構造処理(最上位のテンション以下のテンションを作成する処理)は行われません。
        :return: かっこ外のテンションノートのリスト
        :rtype: list[Note]
        """
        return self.__tension_notes

    @property
    def add_tension_notes(self):
        """
        アド・テンションノートのリストを取得します。
        :return: アド・テンションノートのリスト
        :rtype: list[Note]
        """
        return self.__add_tension_notes

    def __get_quality_value(self):
        """
        コードクオリティの構成音に与える変化量を取得します。
        :return: コードクオリティの構成音に与える変化量
        :rtype: list[int]
        """
        quality_value = [0, 0, 0, 0]
        for quality in self.qualities:
            if quality == "M":
                quality_value[3] += 1
            elif quality == "m":
                quality_value[1] -= 1
            elif quality == "dim":
                quality_value[1] -= 1
                quality_value[2] -= 1
                quality_value[3] -= 1
            elif quality == "aug":
                quality_value[2] += 1

        return quality_value

    def get_hierarchy_tensions_all(self):
        """
        テンションのヒエラルキー構造処理をし、すべてのテンションを取得します。
        :return: かっこ内、かっこ外、すべてのテンションのリスト
        :rtype: list[str]
        """
        tensions = []

        for tension in self.__quality_data.tensions:
            # 階層構造のないテンション
            if tension == "4" or tension == "6" or tension == "2":
                tensions.append(tension)

            # 最上位
            elif tension == "13":
                tensions.append("13")
                tensions.append("11")
                tensions.append("9")
            elif tension == "11":
                tensions.append("11")
                tensions.append("9")
            elif tension == "9":
                tensions.append("9")
            else:
                tensions.append(tension)

        tensions.extend(self.__quality_data.tensions_parentheses)
        tensions.extend(self.__quality_data.add_tensions)

        return list(set(tensions))

    def get_notes(self):
        """
        このクオリティから表されるノートのリストを取得します。
        :return: ノートのリスト
        :rtype: list[Note]
        """

        quality_notes = [Note("C"), Note("E"), Note("G"), Note("Bb")]

        # 7thの無効化
        quality_notes[3].disabled = True

        # クオリティによるノートの変化
        quality_values = self.__get_quality_value()
        for i, value in enumerate(quality_values):
            quality_notes[i] = quality_notes[i].transposed(value)

        # 直接変更されるクオリティによる変化
        qualities = self.qualities
        for qua in qualities:
            if qua == "sus":
                quality_notes[1].disabled = True

        # テンションの追加
        tensions = self.get_hierarchy_tensions_all()
        for tension in tensions:
            # -5や#5は既存のノートを変化させる
            if tension == "-5" or tension == "b5":
                quality_notes[2] = quality_notes[2].transposed(-1)
                continue
            elif tension == "+5" or tension == "#5":
                quality_notes[2] = quality_notes[2].transposed(1)
                continue
            elif tension == "5":
                quality_notes[1].disabled = True
                continue
            elif tension == "7":
                quality_notes[3].disabled = False
                continue

            tension_note = Note.create_from_tension(tension)
            quality_notes.append(tension_note)

        # 無効のノートを削除
        notes = [note for note in quality_notes if not note.disabled]
        return notes
