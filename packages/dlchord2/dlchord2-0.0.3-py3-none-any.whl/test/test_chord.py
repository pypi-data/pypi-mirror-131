import copy

from dlchord2 import const
from dlchord2.chord import Chord
from dlchord2.note import Note


def test_root():
    for quality_name, notes in const.CHORD_MAP.items():
        for root_text in const.TONE_TO_INDEX.keys():
            for bass_text in const.TONE_TO_INDEX.keys():
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)
                assert const.TONE_TO_INDEX[root_text] == chord.root.note_index


def test_bass():
    for quality_name, notes in const.CHORD_MAP.items():
        for root_text in const.TONE_TO_INDEX.keys():
            for bass_text in const.TONE_TO_INDEX.keys():
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)
                assert const.TONE_TO_INDEX[bass_text] == chord.bass.note_index


def test_quality():
    for quality_name, notes in const.CHORD_MAP.items():
        for root_text in const.TONE_TO_INDEX.keys():
            for bass_text in const.TONE_TO_INDEX.keys():
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)
                assert quality_name == chord.quality.raw_quality_text


def test_is_on_chord():
    for quality_name, notes in const.CHORD_MAP.items():
        for root_text in const.TONE_TO_INDEX.keys():
            for bass_text in const.TONE_TO_INDEX.keys():
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)
                is_on_chord = Note(root_text) != Note(bass_text)
                assert is_on_chord == chord.is_on_chord

    for quality_name, notes in const.CHORD_MAP.items():
        for root_text in const.TONE_TO_INDEX.keys():
            chord_name = root_text + quality_name
            chord = Chord(chord_name)
            assert not chord.is_on_chord


def test_transposed():
    tones = const.TONE_TO_INDEX.keys()
    qualities = const.CHORD_MAP.items()
    for quality_name, notes in qualities:
        for root_text in tones:
            for bass_text in tones:
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)

                for i in range(1):
                    transposed_chord = chord.transposed(i)
                    transposed_chord_name = (Note(root_text).transposed(i).raw_note_text +
                                             quality_name + "/" +
                                             Note(bass_text).transposed(i).raw_note_text)
                    transposed_chord_origin = Chord(transposed_chord_name)

                    assert transposed_chord_origin == transposed_chord


def test_get_notes():
    tones = const.TONE_TO_INDEX.keys()
    qualities = const.CHORD_MAP.items()
    for quality_name, notes in qualities:
        for root_text in tones:
            for bass_text in tones:
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)

                note_indexes = {note.note_index for note in chord.get_notes()}
                notes_origin = list(copy.copy(notes))

                for i in range(len(notes_origin)):
                    notes_origin[i] += Note(root_text).note_index
                    notes_origin[i] %= 12

                if chord.is_on_chord:
                    notes_origin.insert(0, Note(bass_text).note_index)

                assert set(notes_origin) == note_indexes


def test_reconfigured():
    tones = const.TONE_TO_INDEX.keys()
    qualities = const.CHORD_MAP.items()
    for quality_name, notes in qualities:
        for root_text in tones:
            for bass_text in tones:
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)

                assert chord == chord.reconfigured()
