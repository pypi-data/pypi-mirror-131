from dlchord2 import const
from dlchord2.accidentals import Accidentals
from dlchord2.parser.note_parser import NoteParser


def test_parse():
    for scale_text in const.SCALE_PATTERN:
        for note_text in const.SCALE_PATTERN[scale_text]:
            parser = NoteParser()
            note_data = parser.parse(note_text)

            accidentals_origin = Accidentals(note_text[1:])
            assert accidentals_origin == note_data.accidentals

            note_origin = const.TONE_TO_INDEX[note_text]
            assert note_origin == note_data.note_index


def test_parse_more_than_double_flat():
    parser = NoteParser()

    for i in range(20):
        note_data = parser.parse("C" + (const.ACCIDENTALS_SHARP * i))
        accidentals_origin = Accidentals(const.ACCIDENTALS_SHARP * i)
        assert accidentals_origin == note_data.accidentals

        note_index_origin = i % 12
        assert note_index_origin == note_data.note_index

    for i in range(20):
        note_data = parser.parse("C" + (const.ACCIDENTALS_FLAT * i))
        accidentals_origin = Accidentals(const.ACCIDENTALS_FLAT * i)
        assert accidentals_origin == note_data.accidentals

        note_index_origin = (-i) % 12
        assert note_index_origin == note_data.note_index
