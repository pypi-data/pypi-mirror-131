from dlchord2.accidentals import Accidentals
from dlchord2 import const
from dlchord2.parser.accidentals_parser import AccidentalsType


def test_text():
    for i in range(20):
        accidentals = Accidentals(const.ACCIDENTALS_SHARP * i)
        accidentals_text_origin = const.ACCIDENTALS_SHARP * i
        assert accidentals_text_origin == accidentals.text

    for i in range(20):
        accidentals = Accidentals(const.ACCIDENTALS_FLAT * i)
        accidentals_text_origin = const.ACCIDENTALS_FLAT * i
        assert accidentals_text_origin == accidentals.text


def test_type():
    accidentals = Accidentals("")
    accidentals_type_origin = AccidentalsType.NONE
    assert accidentals_type_origin == accidentals.type

    for i in range(1, 20):
        accidentals = Accidentals(const.ACCIDENTALS_SHARP * i)
        accidentals_type_origin = AccidentalsType.SHARP
        assert accidentals_type_origin == accidentals.type

    for i in range(1, 20):
        accidentals = Accidentals(const.ACCIDENTALS_FLAT * i)
        accidentals_type_origin = AccidentalsType.FLAT
        assert accidentals_type_origin == accidentals.type


def test_transpose_num():
    accidentals = Accidentals("")
    accidentals_trans_num_origin = 0
    assert accidentals_trans_num_origin == accidentals.transpose_num

    for i in range(1, 20):
        accidentals = Accidentals(const.ACCIDENTALS_SHARP * i)
        accidentals_trans_num_origin = i
        assert accidentals_trans_num_origin == accidentals.transpose_num

    for i in range(1, 20):
        accidentals = Accidentals(const.ACCIDENTALS_FLAT * i)
        accidentals_trans_num_origin = -i
        assert accidentals_trans_num_origin == accidentals.transpose_num

