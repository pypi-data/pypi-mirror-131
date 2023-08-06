from dlchord2 import const
from dlchord2.parser.accidentals_parser import AccidentalsParser, AccidentalsType

accidentals_pattern = {
    "C": (0, AccidentalsType.NONE),
    "Db": (-1, AccidentalsType.FLAT),
    "C#": (1, AccidentalsType.SHARP),
    "D": (0, AccidentalsType.NONE),
    "Eb": (-1, AccidentalsType.FLAT),
    "D#": (1, AccidentalsType.SHARP),
    "E": (0, AccidentalsType.NONE),
    "F": (0, AccidentalsType.NONE),
    "Gb": (-1, AccidentalsType.FLAT),
    "F#": (1, AccidentalsType.SHARP),
    "G": (0, AccidentalsType.NONE),
    "Ab": (-1, AccidentalsType.FLAT),
    "G#": (1, AccidentalsType.SHARP),
    "A": (0, AccidentalsType.NONE),
    "Bb": (-1, AccidentalsType.FLAT),
    "A#": (1, AccidentalsType.SHARP),
    "B": (0, AccidentalsType.NONE),
    "B#": (1, AccidentalsType.SHARP),
    "Dbb": (-2, AccidentalsType.FLAT),
    "C##": (2, AccidentalsType.SHARP),
    "Ebb": (-2, AccidentalsType.FLAT),
    "Fb": (-1, AccidentalsType.FLAT),
    "D##": (2, AccidentalsType.SHARP),
    "E#": (1, AccidentalsType.SHARP),
    "F##": (2, AccidentalsType.SHARP),
    "Abb": (-2, AccidentalsType.FLAT),
    "Bbb": (-2, AccidentalsType.FLAT),
    "G##": (2, AccidentalsType.SHARP),
    "Cb": (-1, AccidentalsType.FLAT)
}


def test_parse():
    for scale_text in const.SCALE_PATTERN:
        for note in const.SCALE_PATTERN[scale_text]:
            parser = AccidentalsParser()
            accidentals_data = parser.parse(note[1:])

            accidentals_origin = note[1:]
            assert accidentals_origin == accidentals_data.accidentals

            accidentals_type_origin = accidentals_pattern[note][1]
            assert accidentals_type_origin == accidentals_data.accidentals_type

            accidentals_trans_num_origin = accidentals_pattern[note][0]
            assert accidentals_trans_num_origin == accidentals_data.transpose_num
