from dlchord2 import const
from dlchord2.accidentals import Accidentals
from dlchord2.note import Note
from dlchord2.scale import Scale


def test_create_from_index_note():
    for i in range(12):
        note = Note.create_from_index_note(i)


def test_create_from_tension():
    tensions = const.TENSION_TO_INDEX.keys()

    for tension in tensions:
        note = Note.create_from_tension(tension)


def test_transposed():
    for scale_text in const.SCALE_PATTERN.keys():
        scale_origin = Scale(scale_text)

        for note_text in const.SCALE_PATTERN[scale_text]:
            note = Note(note_text, scale_text=scale_text)

            for i in range(12):
                note_transposed = note.transposed(steps=i, scale_text=scale_text)

                note_index_origin = note.note_index
                assert (note_index_origin + i) % 12 == note_transposed.note_index

                assert scale_origin == note_transposed.scale

            for i in range(0, -12, -1):
                note_transposed = note.transposed(steps=i, scale_text=scale_text)

                note_index_origin = note.note_index
                assert (note_index_origin + i) % 12 == note_transposed.note_index

                assert scale_origin == note_transposed.scale


def test_disabled():
    note = Note("C")
    assert not note.disabled

    note.disabled = True
    assert note.disabled


def test_note_index():
    for scale_text in const.SCALE_PATTERN.keys():
        for note_text in const.SCALE_PATTERN[scale_text]:
            note = Note(note_text, scale_text=scale_text)

            note_index_origin = const.TONE_TO_INDEX[note_text]
            assert note_index_origin == note.note_index


def test_raw_note_text():
    for scale_text in const.SCALE_PATTERN.keys():
        for note_text in const.SCALE_PATTERN[scale_text]:
            note = Note(note_text, scale_text=scale_text)

            assert note_text == note.raw_note_text


def test_normed_note_text():
    for scale_text in const.SCALE_PATTERN.keys():
        for note_text in const.SCALE_PATTERN[scale_text]:
            note = Note(note_text, scale_text=scale_text)

            assert note_text == note.normed_note_text


def test_accidentals():
    for scale_text in const.SCALE_PATTERN.keys():
        for note_text in const.SCALE_PATTERN[scale_text]:
            note = Note(note_text, scale_text=scale_text)

            accidentals_origin = Accidentals(note_text[1:])
            assert accidentals_origin == note.accidentals


def test_scale():
    for scale_text in const.SCALE_PATTERN.keys():
        for note_text in const.SCALE_PATTERN[scale_text]:
            note = Note(note_text, scale_text=scale_text)

            scale_origin = Scale(scale_text)
            assert scale_origin == note.scale
