from dlchord2 import const
from dlchord2.chord import Chord
from dlchord2.utils import match_quality, notes_to_chords, note_indexes_to_chords


def test_match_quality():
    for quality_name, notes in const.CHORD_MAP.items():
        is_match, quality = match_quality(notes)
        assert quality_name == quality


def test_notes_to_chords():
    tones = const.TONE_TO_INDEX.keys()
    qualities = const.CHORD_MAP.items()
    for quality_name, notes in qualities:
        for root_text in tones:
            for bass_text in tones:
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)

                chord_list = notes_to_chords(chord.get_notes())
                assert chord_list[0] == chord


def test_note_indexes_to_chords():
    tones = const.TONE_TO_INDEX.keys()
    qualities = const.CHORD_MAP.items()
    for quality_name, notes in qualities:
        for root_text in tones:
            for bass_text in tones:
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)

                chord_list = note_indexes_to_chords([note.note_index for note in chord.get_notes()])
                assert chord_list[0] == chord
