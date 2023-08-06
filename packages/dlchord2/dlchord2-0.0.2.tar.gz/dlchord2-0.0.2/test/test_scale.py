from dlchord2 import const
from dlchord2.note import Note
from dlchord2.scale import Scale


def test_scale_text():
    for scale_text in const.SCALE_PATTERN.keys():
        scale = Scale(scale_text)

        assert scale_text == scale.scale_text


def test_scale_list():
    for scale_text in const.SCALE_PATTERN.keys():
        scale = Scale(scale_text)

        assert const.SCALE_PATTERN[scale_text] == scale.scale_list


def test_get_note_text():
    for scale_text in const.SCALE_PATTERN.keys():
        scale = Scale(scale_text)

        for idx in range(12):
            assert const.SCALE_PATTERN[scale_text][idx] == scale.get_note_text(idx)


def test_get_tone_text_absolute():
    for scale_text in const.SCALE_PATTERN.keys():
        scale = Scale(scale_text)

        for idx in range(12):
            note_origin = Note(const.SCALE_PATTERN["C"][idx])
            note_test = Note(scale.get_note_text_absolute(idx))
            assert note_origin == note_test
