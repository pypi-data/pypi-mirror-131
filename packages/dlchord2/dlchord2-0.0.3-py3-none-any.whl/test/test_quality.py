from dlchord2 import const
from dlchord2.note import Note
from dlchord2.quality import Quality

test_quality_pattern = {
    # qualities, tensions, tensions_parentheses, add_tensions
    '5': ([], ["5"], [], []),
    # 3 notes
    '': ([], [], [], []),
    'm': (["m"], [], [], []),
    'dim': (["dim"], [], [], []),
    'aug': (["aug"], [], [], []),
    'sus2': (["sus"], ["2"], [], []),
    'sus4': (["sus"], ["4"], [], []),
    # 4 notes
    '6': ([], ["6"], [], []),
    '7': ([], ["7"], [], []),
    'M7': (["M"], ["7"], [], []),
    'm6': (["m"], ["6"], [], []),
    'm7': (["m"], ["7"], [], []),
    'mM7': (["m", "M"], ["7"], [], []),
    '7-5': ([], ["7", "-5"], [], []),
    'M7-5': (["M"], ["7", "-5"], [], []),
    'm7-5': (["m"], ["7", "-5"], [], []),
    'mM7-5': (["m", "M"], ["7", "-5"], [], []),
    'aug7': (["aug"], ["7"], [], []),
    'augM7': (["aug", "M"], ["7"], [], []),
    'aug(b9)': (["aug"], [], ["b9"], []),
    '7sus4': (["sus"], ["7", "4"], [], []),
    'dim7': (["dim"], ["7"], [], []),
    'add9': ([], [], [], ["9"]),
    'add11': ([], [], [], ["11"]),
    'madd9': (["m"], [], [], ["9"]),

    # 5 notes
    '69': ([], ["6", "9"], [], []),
    '7(9)': ([], ["7"], ["9"], []),
    '7(13)': ([], ["7"], ["13"], []),
    '7(b9)': ([], ["7"], ["b9"], []),
    '7(#9)': ([], ["7"], ["#9"], []),
    '7(#11)': ([], ["7"], ["#11"], []),
    '7(b13)': ([], ["7"], ["b13"], []),
    '7-5(9)': ([], ["7", "-5"], ["9"], []),
    '7-5(#9)': ([], ["7", "-5"], ["#9"], []),
    '7-5(b13)': ([], ["7", "-5"], ["b13"], []),
    'M7(9)': (["M"], ["7"], ["9"], []),
    'M7(13)': (["M"], ["7"], ["13"], []),
    'M7(#11)': (["M"], ["7"], ["#11"], []),
    'M7(b9)': (["M"], ["7"], ["b9"], []),
    'm69': (["m"], ["6", "9"], [], []),
    'm7(9)': (["m"], ["7"], ["9"], []),
    'm7(11)': (["m"], ["7"], ["11"], []),
    'm7(13)': (["m"], ["7"], ["13"], []),
    'm7(b9)': (["m"], ["7"], ["b9"], []),
    'm7-5(9)': (["m"], ["7", "-5"], ["9"], []),
    'm7-5(11)': (["m"], ["7", "-5"], ["11"], []),
    'mM7(9)': (["m", "M"], ["7"], ["9"], []),
    'mM7(13)': (["m", "M"], ["7"], ["13"], []),
    'aug7(9)': (["aug"], ["7"], ["9"], []),
    'augM7(#9)': (["aug", "M"], ["7"], ["#9"], []),

    # 6 notes
    '7(9, 11)': ([], ["7"], ["9", "11"], []),
    '7(9, 13)': ([], ["7"], ["9", "13"], []),
    '7(9, b13)': ([], ["7"], ["9", "b13"], []),
    '7(9, #11)': ([], ["7"], ["9", "#11"], []),
    '7(b9, 13)': ([], ["7"], ["b9", "13"], []),
    '7(b9, b13)': ([], ["7"], ["b9", "b13"], []),
    '7(b9, #9)': ([], ["7"], ["b9", "#9"], []),
    '7(b9, #11)': ([], ["7"], ["b9", "#11"], []),
    '7(#9, 13)': ([], ["7"], ["#9", "13"], []),
    '7(#9, b13)': ([], ["7"], ["#9", "b13"], []),
    '7(#9, #11)': ([], ["7"], ["#9", "#11"], []),
    '7(#11, 13)': ([], ["7"], ["#11", "13"], []),
    'm7(9, 11)': (["m"], ["7"], ["9", "11"], []),
    'm7(9, 13)': (["m"], ["7"], ["9", "13"], []),
    'M7(9, 11)': (["M"], ["7"], ["9", "11"], []),
    'M7(9, 13)': (["M"], ["7"], ["9", "13"], []),
    # 7 notes
    '7(9, 11, 13)': ([], ["7"], ["9", "11", "13"], []),
    '7(9, #11, 13)': ([], ["7"], ["9", "#11", "13"], []),
    '7(b9, #11, 13)': ([], ["7"], ["b9", "#11", "13"], []),
    'm7(9, 11, 13)': (["m"], ["7"], ["9", "11", "13"], []),
    'M7(9, 11, 13)': (["M"], ["7"], ["9", "11", "13"], []),
}


def test_qualities():
    for quality_text in test_quality_pattern:
        quality_data = test_quality_pattern[quality_text]
        quality = Quality(quality_text)

        assert quality_data[0] == quality.qualities


def test_tension_parent_notes():
    for quality_text in test_quality_pattern:
        quality_data = test_quality_pattern[quality_text]
        tension_parent_notes = [Note.create_from_tension(qua) for qua in quality_data[2]]
        tension_parent_notes = sorted(tension_parent_notes, key=lambda x: x.note_index)
        quality = Quality(quality_text)

        assert tension_parent_notes == sorted(quality.tension_parent_notes, key=lambda x: x.note_index)


def test_tension_notes():
    for quality_text in test_quality_pattern:
        quality_data = test_quality_pattern[quality_text]
        tension_notes = [Note.create_from_tension(qua) for qua in quality_data[1]]
        tension_notes = sorted(tension_notes, key=lambda x: x.note_index)
        quality = Quality(quality_text)

        assert tension_notes == sorted(quality.tension_notes, key=lambda x: x.note_index)


def test_add_tension_notes():
    for quality_text in test_quality_pattern:
        quality_data = test_quality_pattern[quality_text]
        tension_notes = [Note.create_from_tension(qua) for qua in quality_data[3]]
        tension_notes = sorted(tension_notes, key=lambda x: x.note_index)
        quality = Quality(quality_text)

        assert tension_notes == sorted(quality.add_tension_notes, key=lambda x: x.note_index)


def test_get_hierarchy_tensions_all():
    for quality_text in test_quality_pattern:
        quality_data = test_quality_pattern[quality_text]
        tension_notes = quality_data[1] + quality_data[2] + quality_data[3]
        tension_notes = set(tension_notes)
        quality = Quality(quality_text)

        assert tension_notes == set(quality.get_hierarchy_tensions_all())

    quality = Quality("9")
    assert {"7", "9"} == set(quality.get_hierarchy_tensions_all())
    quality = Quality("11")
    assert {"7", "9", "11"} == set(quality.get_hierarchy_tensions_all())
    quality = Quality("13")
    assert {"7", "9", "11", "13"} == set(quality.get_hierarchy_tensions_all())


def test_get_notes():
    for quality_name, notes in const.CHORD_MAP.items():
        quality = Quality(quality_name)
        note_indexes = [note.note_index for note in quality.get_notes()]
        assert set(notes) == set(note_indexes)
