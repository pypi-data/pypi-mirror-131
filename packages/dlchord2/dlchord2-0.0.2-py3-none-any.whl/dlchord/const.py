from collections import OrderedDict

ACCIDENTALS_SHARP = "#"
ACCIDENTALS_FLAT = "b"

TENSION_TO_INDEX = {
    "2": 2,
    "9": 2,
    "4": 5,
    "11": 5,
    "6": 9,
    "13": 9,
    "#9": 3,
    "b9": 1,
    "#11": 6,
    "b13": 8,
    "+9": 3,
    "-9": 1,
    "+11": 6,
    "-13": 8,
    "7": 10,
    "-5": 6,
    "b5": 6,
    "5": 7
}

TONE_TO_INDEX = {"C": 0, "B#": 0, "Dbb": 0, "Db": 1, "C#": 1, "D": 2, "Ebb": 2, "C##": 2,
                 "Eb": 3, "D#": 3, "E": 4, "D##": 4, "Fb": 4, "F": 5, "E#": 5,
                 "Gb": 6, "F#": 6, "G": 7, "F##": 7, "Abb": 7, "Ab": 8,
                 "G#": 8, "A": 9, "G##": 9, "Bbb": 9, "Bb": 10, "A#": 10, "B": 11, "Cb": 11}

SCALE_INDEXES = [0, 2, 4, 5, 6, 9, 11]

C_MAJOR_SCALE = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
C_SHARP_MAJOR_SCALE = ["C#", "D", "D#", "E", "E#", "F#", "F##", "G#", "A", "A#", "B", "B#"]
D_FLAT_MAJOR_SCALE = ["Db", "Ebb", "Eb", "Fb", "F", "Gb", "G", "Ab", "Bbb", "Bb", "Cb", "C"]
D_MAJOR_SCALE = ["D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B", "C", "C#"]
E_FLAT_MAJOR_SCALE = ["Eb", "Fb", "F", "Gb", "G", "Ab", "A", "Bb", "Cb", "C", "Db", "D"]
E_MAJOR_SCALE = ["E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#"]
F_MAJOR_SCALE = ["F", "Gb", "G", "Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E"]
F_SHARP_MAJOR_SCALE = ["F#", "G", "G#", "A", "A#", "B", "B#", "C#", "D", "D#", "E", "E#"]
G_FLAT_MAJOR_SCALE = ["Gb", "Abb", "Ab", "Bbb", "Bb", "Cb", "C", "Db", "Ebb", "Eb", "Fb", "F"]
G_MAJOR_SCALE = ["G", "Ab", "A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#"]
A_FLAT_MAJOR_SCALE = ["Ab", "Bbb", "Bb", "Cb", "C", "Db", "D", "Eb", "Fb", "F", "Gb", "G"]
A_MAJOR_SCALE = ["A", "Bb", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
B_FLAT_MAJOR_SCALE = ["Bb", "Cb", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A"]
B_MAJOR_SCALE = ["B", "C", "C#", "D", "D#", "E", "E#", "F#", "G", "G#", "A", "A#"]
C_FLAT_MAJOR_SCALE = ["Cb", "Dbb", "Ebb", "Eb", "Fb", "F", "Gb", "Abb", "Ab", "Bbb", "Bb"]

A_MINOR_SCALE = ["A", "Bb", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
E_MINOR_SCALE = ["E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#"]
B_MINOR_SCALE = ["B", "C", "C#", "D", "D#", "E", "E#", "F#", "G", "G#", "A", "A#"]
F_SHARP_MINOR_SCALE = ["F#", "G", "G#", "A", "A#", "B", "B#", "C#", "D", "D#", "E", "E#"]
C_SHARP_MINOR_SCALE = ["C#", "D", "D#", "E", "E#", "F#", "F##", "G#", "A", "A#", "B", "B#"]
G_SHARP_MINOR_SCALE = ["G#", "A", "A#", "B", "B#", "C#", "C##", "D#", "E", "E#", "F#", "F##"]
D_SHARP_MINOR_SCALE = ["D#", "E", "E#", "F#", "F##", "G#", "G##", "A#", "B", "B#", "C#", "C##"]
A_SHARP_MINOR_SCALE = ["A#", "B", "B#", "C#", "C##", "D#", "D##", "E#", "F#", "F##", "G#", "G##"]
D_MINOR_SCALE = ["D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B", "C", "C#"]
G_MINOR_SCALE = ["G", "Ab", "A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#"]
C_MINOR_SCALE = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
F_MINOR_SCALE = ["F", "Gb", "G", "Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E"]
B_FLAT_MINOR_SCALE = ["Bb", "Cb", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A"]
E_FLAT_MINOR_SCALE = ["Eb", "Fb", "F", "Gb", "G", "Ab", "A", "Bb", "Cb", "C", "Db", "D"]
A_FLAT_MINOR_SCALE = ["Ab", "Bbb", "Bb", "Cb", "C", "Db", "D", "Eb", "Fb", "F", "Gb", "G"]

SCALE_TO_INDEX = {
    "C": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "Gb": 6,
    "F#": 6,
    "G": 7,
    "Ab": 8,
    "A": 9,
    "Bb": 10,
    "B": 11,
    "Cm": 0,
    "C#m": 1,
    "Dm": 2,
    "D#m": 3,
    "Ebm": 3,
    "Em": 4,
    "Fm": 5,
    "F#m": 6,
    "Gm": 7,
    "G#m": 8,
    "Abm": 8,
    "Am": 9,
    "A#m": 10,
    "Bbm": 10,
    "Bm": 11,
}
SCALE_PATTERN = {
    "C": C_MAJOR_SCALE,
    "C#": C_SHARP_MAJOR_SCALE,
    "Db": D_FLAT_MAJOR_SCALE,
    "D": D_MAJOR_SCALE,
    "Eb": E_FLAT_MAJOR_SCALE,
    "E": E_MAJOR_SCALE,
    "F": F_MAJOR_SCALE,
    "Gb": G_FLAT_MAJOR_SCALE,
    "F#": F_SHARP_MAJOR_SCALE,
    "G": G_MAJOR_SCALE,
    "Ab": A_FLAT_MAJOR_SCALE,
    "A": A_MAJOR_SCALE,
    "Bb": B_FLAT_MAJOR_SCALE,
    "B": B_MAJOR_SCALE,
    "Cm": C_MINOR_SCALE,
    "C#m": C_SHARP_MINOR_SCALE,
    "Dm": D_MINOR_SCALE,
    "D#m": D_SHARP_MINOR_SCALE,
    "Ebm": E_FLAT_MINOR_SCALE,
    "Em": E_MINOR_SCALE,
    "Fm": F_MINOR_SCALE,
    "F#m": F_SHARP_MINOR_SCALE,
    "Gm": G_MINOR_SCALE,
    "G#m": G_SHARP_MINOR_SCALE,
    "Abm": A_FLAT_MINOR_SCALE,
    "Am": A_MINOR_SCALE,
    "A#m": A_SHARP_MINOR_SCALE,
    "Bbm": B_FLAT_MINOR_SCALE,
    "Bm": B_MINOR_SCALE
}

CHORD_MAP = OrderedDict((
    # 2 notes
    ('5', (0, 7)),
    # 3 notes
    ('', (0, 4, 7)),
    ('m', (0, 3, 7)),
    ('dim', (0, 3, 6)),
    ('aug', (0, 4, 8)),
    ('sus2', (0, 2, 7)),
    ('sus4', (0, 5, 7)),
    # 4 notes
    ('6', (0, 4, 7, 9)),
    ('7', (0, 4, 7, 10)),
    ('M7', (0, 4, 7, 11)),
    ('m6', (0, 3, 7, 9)),
    ('m7', (0, 3, 7, 10)),
    ('mM7', (0, 3, 7, 11)),
    ('7-5', (0, 4, 6, 10)),
    ('M7-5', (0, 4, 6, 11)),
    ('m7-5', (0, 3, 6, 10)),
    ('mM7-5', (0, 3, 6, 11)),
    ('aug7', (0, 4, 8, 10)),
    ('augM7', (0, 4, 8, 11)),
    ('aug(b9)', (0, 4, 8, 1)),
    ('7sus4', (0, 5, 7, 10)),
    ('dim7', (0, 3, 6, 9)),
    ('add9', (0, 4, 7, 2)),
    ('add11', (0, 4, 7, 5)),
    ('madd9', (0, 3, 7, 2)),

    # 5 notes
    ('69', (0, 4, 7, 9, 2)),
    ('7(9)', (0, 4, 7, 10, 2)),
    ('7(13)', (0, 4, 7, 10, 9)),
    ('7(b9)', (0, 4, 7, 10, 1)),
    ('7(#9)', (0, 4, 7, 10, 3)),
    ('7(#11)', (0, 4, 7, 10, 6)),
    ('7(b13)', (0, 4, 7, 10, 8)),
    ('7-5(9)', (0, 4, 6, 10, 2)),
    ('7-5(#9)', (0, 4, 6, 10, 3)),
    ('7-5(b13)', (0, 4, 6, 10, 8)),
    ('M7(9)', (0, 4, 7, 11, 2)),
    ('M7(13)', (0, 4, 7, 11, 9)),
    ('M7(#11)', (0, 4, 7, 11, 6)),
    ('M7(b9)', (0, 4, 7, 11, 1)),
    ('m69', (0, 3, 7, 9, 2)),
    ('m7(9)', (0, 3, 7, 10, 2)),
    ('m7(11)', (0, 3, 7, 10, 5)),
    ('m7(13)', (0, 3, 7, 10, 9)),
    ('m7(b9)', (0, 3, 7, 10, 1)),
    ('m7-5(9)', (0, 3, 6, 10, 2)),
    ('m7-5(11)', (0, 3, 6, 10, 5)),
    ('mM7(9)', (0, 3, 7, 11, 2)),
    ('mM7(13)', (0, 3, 7, 11, 9)),
    ('aug7(9)', (0, 4, 8, 10, 2)),
    ('augM7(#9)', (0, 4, 8, 11, 3)),

    # 6 notes
    ('7(9, 11)', (0, 4, 7, 10, 2, 5)),
    ('7(9, 13)', (0, 4, 7, 10, 2, 9)),
    ('7(9, b13)', (0, 4, 7, 10, 2, 8)),
    ('7(9, #11)', (0, 4, 7, 10, 2, 6)),
    ('7(b9, 13)', (0, 4, 7, 10, 1, 9)),
    ('7(b9, b13)', (0, 4, 7, 10, 1, 8)),
    ('7(b9, #9)', (0, 4, 7, 10, 1, 3)),
    ('7(b9, #11)', (0, 4, 7, 10, 1, 6)),
    ('7(#9, 13)', (0, 4, 7, 10, 3, 9)),
    ('7(#9, b13)', (0, 4, 7, 10, 3, 8)),
    ('7(#9, #11)', (0, 4, 7, 10, 3, 6)),
    ('7(#11, 13)', (0, 4, 7, 10, 6, 9)),
    ('m7(9, 11)', (0, 3, 7, 10, 2, 5)),
    ('m7(9, 13)', (0, 3, 7, 10, 2, 9)),
    ('M7(9, 11)', (0, 4, 7, 11, 2, 5)),
    ('M7(9, 13)', (0, 4, 7, 11, 2, 9)),

    # 7 notes
    ('7(9, 11, 13)', (0, 4, 7, 10, 2, 5, 9)),
    ('7(9, #11, 13)', (0, 4, 7, 10, 2, 6, 9)),
    ('7(b9, #11, 13)', (0, 4, 7, 10, 1, 6, 9)),
    ('m7(9, 11, 13)', (0, 3, 7, 10, 2, 5, 9)),
    ('M7(9, 11, 13)', (0, 4, 7, 11, 2, 5, 9)),

))
