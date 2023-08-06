from dlchord2 import const
from dlchord2 import chord as chd
from dlchord2.note import Note


def __chord_sort_func(chord):
    eval_score = 0
    if Note.create_from_tension("5") in chord.quality.tension_notes:
        eval_score -= 1

    if chord.bass in chord.quality.add_tension_notes:
        eval_score -= 1

    if chord.is_on_chord:
        eval_score -= 1

    seventh_index = 10
    if chord.bass.note_index == (chord.root.note_index + seventh_index) % 12:
        if Note.create_from_tension("7") in chord.quality.tension_notes:
            eval_score += 1

    return eval_score


def match_quality(notes, omit_five_note=False, omit_third_note=False):
    """
    ノートのリストから一致するクオリティを検索します。
    :param notes: ノートのリスト
    :type notes: list[int]
    :param omit_five_note: 5度のノートを省略して検索するかどうか
    :type omit_five_note: bool
    :param omit_third_note: 3度のノートを省略して検索するかどうか
    :type omit_third_note: bool
    :return: マッチしたらTrueとクオリティを返します。それ以外の場合はFalseと""を返します。
    :rtype: tuple(bool, str)
    """
    relative_notes = []
    for i in range(len(notes)):
        relative_notes.append((notes[i] - notes[0]) % 12)

    relative_notes = set(relative_notes)

    for quality_name, notes_origin in const.CHORD_MAP.items():
        notes_origin = set(notes_origin)
        if relative_notes == notes_origin:
            return True, quality_name

        omitted_notes = relative_notes.copy()
        # 5度の音を省略して検索
        if omit_five_note:
            five_note_index = 7
            if five_note_index in omitted_notes:
                omitted_notes.remove(five_note_index)
            if five_note_index in notes_origin:
                notes_origin.remove(five_note_index)

            if omitted_notes == notes_origin:
                return True, quality_name

        # 3度の音を省略して検索
        if omit_third_note:
            third_note_index = 4
            if third_note_index in omitted_notes:
                omitted_notes.remove(third_note_index)
            if third_note_index in notes_origin:
                notes_origin.remove(third_note_index)

            if omitted_notes == notes_origin:
                return True, quality_name

    return False, ""


def notes_to_chords(notes, sort_func=__chord_sort_func):
    """
    ノーツリストから該当するコードの候補のリストを取得します。
    :param notes: ノーツリスト
    :type notes: list[Note]
    :param sort_func: コードをソートするときに使用する関数
    :type sort_func: function
    :return: コードの候補のリスト
    :rtype: list[Chord]
    """
    note_indexes = [note.note_index for note in notes]
    return note_indexes_to_chords(note_indexes, sort_func=sort_func)


def note_indexes_to_chords(note_indexes, sort_func=__chord_sort_func):
    """
    ノーツリストから該当するコードの候補のリストを取得します。
    :param note_indexes: ノーツリスト
    :type note_indexes: list[int]
    :param sort_func: コードをソートするときに使用する関数
    :type sort_func: function
    :return: コードの候補のリスト
    :rtype: list[Chord]
    """

    shifted_notes = note_indexes[1:]

    chord_list = []
    bass_note = note_indexes[0]
    # ベースを含まない転回系
    for i in range(len(shifted_notes)):
        is_match, quality = match_quality(shifted_notes)
        if is_match:
            root_note = shifted_notes[0]

            on_chord = ""
            if bass_note != root_note:
                on_chord = "/" + Note.create_from_index_note(bass_note).normed_note_text

            chord = chd.Chord(Note.create_from_index_note(root_note).normed_note_text + quality + on_chord)
            chord_list.append(chord)

        note = shifted_notes.pop(0)
        shifted_notes.append(note)

    # ベースを含む転回系
    shifted_notes.insert(0, bass_note)
    for i in range(len(shifted_notes)):
        is_match, quality = match_quality(shifted_notes)
        if is_match:
            root_note = shifted_notes[0]

            on_chord = ""
            if bass_note != root_note:
                on_chord = "/" + Note.create_from_index_note(bass_note).normed_note_text

            chord = chd.Chord(Note.create_from_index_note(root_note).normed_note_text + quality + on_chord)
            chord_list.append(chord)

        note = shifted_notes.pop(0)
        shifted_notes.append(note)

    chord_list = sorted(chord_list, key=sort_func, reverse=True)
    return chord_list
