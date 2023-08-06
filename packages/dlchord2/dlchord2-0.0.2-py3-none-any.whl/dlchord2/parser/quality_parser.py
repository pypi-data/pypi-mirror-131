import re

from dlchord2 import const
from dlchord2.exceptions.quality_exceptions import QualityParseError


class QualityParseData(object):
    def __init__(self, qualities, tensions, tensions_parentheses, add_tensions):
        self.__qualities = qualities
        self.__tensions = tensions
        self.__tensions_parentheses = tensions_parentheses
        self.__add_tensions = add_tensions

    @property
    def qualities(self):
        """
        テンションを含まないクオリティ部分のみのテキストリストを取得します。
        :return: クオリティのテキストリスト
        :rtype: list[str]
        """
        return self.__qualities

    @property
    def tensions(self):
        """
        かっこ外のテンションのリストを取得します。
        :return: かっこ外のテンションのリスト
        :rtype: list[str]
        """
        return self.__tensions

    @property
    def tensions_parentheses(self):
        """
        かっこ内のテンションのリストを取得します。
        :return: かっこ内のテンションのリスト
        :rtype: list[str]
        """
        return self.__tensions_parentheses

    @property
    def add_tensions(self):
        """
        アド・テンションを取得します。
        :return: アド・テンション
        :rtype: list[Note]
        """
        return self.__add_tensions


class QualityParser(object):
    """
    コードクオリティを解析するクラス
    """

    def __find_tension_parentheses(self, quality_text):
        """
        かっこ内のテンションノートを探します。
        :param quality_text: コードクオリティのテキスト
        :type quality_text: str
        :return: かっこ内のテンションのリスト
        :rtype: list[str]
        """
        match = re.search(r"(\()(.*?)(\))", quality_text)
        if match is None:
            return []

        if len(match.groups()) < 3:
            return []

        tensions_raw_text = match.group(2)
        tensions_text = tensions_raw_text.split(",")
        tensions = []

        for tension_text in tensions_text:
            tension = tension_text.strip()

            if tension not in const.TENSION_TO_INDEX:
                raise QualityParseError("かっこ内のテンション {} が不明です".format(tension))

            tensions.append(tension)
        return tensions

    def __find_tension(self, quality_text):
        """
        かっこ外のテンションノートを探します。
        :param quality_text: コードクオリティのテキスト
        :type quality_text: str
        :return: かっこ外のテンションのリスト
        :rtype: list[str]
        """
        exclude_parentheses = re.sub(r"(\()(.*?)(\))", "", quality_text)

        if "add" in exclude_parentheses:
            return ""

        match_tensions = re.findall("9|11|13|[-+b#]5|2|4|6|(?<![-+b#])5", exclude_parentheses)

        for tension in match_tensions:
            if tension not in const.TENSION_TO_INDEX:
                raise QualityParseError("かっこ外のテンション {} が不明です".format(tension))

        return match_tensions

    def __find_add_tension(self, quality_text):
        """
        アド・テンションを取得します。
        :param quality_text: コードクオリティのテキスト
        :type quality_text: str
        :return: アド・テンションノートのリスト
        :rtype: list[str]
        """
        match = re.findall(r"add9|add11|add4|add2", quality_text)

        add_tension_list = []
        for tension in match:
            add_tension_list.append(tension.replace("add", ""))

        return add_tension_list

    def __find_quality(self, quality_text):
        """
        テンションを含まないクオリティを取得します。
        :param quality_text: コードクオリティのテキスト
        :type quality_text: str
        :return: クオリティのリスト
        :rtype: list[str]
        """
        qualities = []
        match = re.findall(r"aug|dim|sus", quality_text)
        if match:
            qualities.extend(match)
            quality_text = re.sub(r"aug|dim|sus", "", quality_text)

        match = re.findall(r"m|M", quality_text)
        if match:
            qualities.extend(match)
            quality_text = re.sub(r"m|M", "", quality_text)

        return qualities

    def __exists_seventh(self, quality_text, tensions):
        if "7" in quality_text:
            return True

        for tension in tensions:
            if tension == "13":
                return True
            elif tension == "11":
                return True
            elif tension == "9" and "6" not in tensions:
                return True

        return False

    def parse(self, quality_text):
        tensions_parentheses = self.__find_tension_parentheses(quality_text)
        tensions = self.__find_tension(quality_text)
        add_tensions = self.__find_add_tension(quality_text)
        qualities = self.__find_quality(quality_text)

        exists_seventh = self.__exists_seventh(quality_text, tensions)
        if exists_seventh:
            tensions.append("7")

        quality_data = QualityParseData(qualities, tensions, tensions_parentheses, add_tensions)
        return quality_data
