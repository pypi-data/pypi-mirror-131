from dlchord2 import const
from dlchord2.parser.chord_parser import ChordParser


def test_parse():
    parser = ChordParser()
    chord_data = parser.parse("B#/C")
    for quality_name, notes in const.CHORD_MAP.items():
        for root_text in const.TONE_TO_INDEX.keys():
            for bass_text in const.TONE_TO_INDEX.keys():
                chord_name = root_text + quality_name + "/" + bass_text
                parser = ChordParser()
                chord_data = parser.parse(chord_name)
                assert root_text == chord_data.root_text
                assert bass_text == chord_data.bass_text
                assert quality_name == chord_data.quality_text
