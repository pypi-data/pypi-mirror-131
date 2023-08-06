from dlchord2.note import Note
from dlchord2.parser.accidentals_parser import AccidentalsType
from dlchord2.parser.chord_parser import ChordParser
from dlchord2.quality import Quality
from dlchord2 import utils


class Chord(object):
    def __init__(self, chord_text, scale_text="C"):
        self.__raw_chord_text = chord_text
        self.__scale_text = scale_text

        parser = ChordParser()
        self.__chord_data = parser.parse(chord_text)
        self.__root = Note(self.__chord_data.root_text, scale_text=scale_text)
        self.__bass = Note(self.__chord_data.bass_text, scale_text=scale_text)
        self.__quality = Quality(self.__chord_data.quality_text)

    def __str__(self):
        return "<Chord: {}>".format(self.raw_chord_text)

    def __unicode__(self):
        return "<Chord: {}>".format(self.raw_chord_text)

    def __eq__(self, other):
        if not isinstance(other, Chord):
            raise TypeError("{} オブジェクトとChordオブジェクトを比較できません".format(type(other)))

        note_indexes = {note.note_index for note in self.get_notes()}
        other_note_indexes = {note.note_index for note in self.get_notes()}
        if note_indexes == other_note_indexes:
            return True

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def raw_chord_text(self):
        return self.__raw_chord_text

    @property
    def root(self):
        """
        ルート音を取得します。
        :return: ルート音
        :rtype: Note
        """
        return self.__root

    @property
    def bass(self):
        """
        ベース音を取得します。
        :return: ベース音
        :rtype: Note
        """
        return self.__bass

    @property
    def quality(self):
        """
        コードクオリティを取得します。
        :return: コードクオリティ
        :rtype: Quality
        """
        return self.__quality

    @property
    def is_on_chord(self):
        """
        オンコードかを取得します。
        :return: オンコードの場合はTrue,それ以外の場合はFalse
        :rtype: bool
        """
        return self.root != self.bass

    def transposed(self, steps, scale_text=None):
        """
        転調したコードを返します。
        scale_textがNoneの場合は、現在のコードに設定されているスケールを使用します。
        :param steps: 転調する数
        :type steps: int
        :param scale_text: 転調後のコードに適用するスケール
        :type scale_text: str
        :return: 転調後のコード
        :rtype: Chord
        """
        if self.is_on_chord:
            return Chord(self.root.transposed(steps, scale_text).normed_note_text +
                         self.quality.raw_quality_text +
                         "/" + self.bass.transposed(steps, scale_text).normed_note_text)
        else:
            return Chord(self.root.transposed(steps, scale_text).normed_note_text +
                         self.quality.raw_quality_text)

    def get_notes(self, sparse=False):
        """
        コードのノートリストを取得します。
        :param sparse: ノートリストをスパースにするか
        :return: コードのノートリスト
        :rtype: list[Note]
        """
        relative_notes = self.quality.get_notes()
        notes = [note.transposed(self.root.note_index) for note in relative_notes]

        if self.is_on_chord:
            notes.insert(0, self.bass)

        if sparse:
            # 非構成音は0
            sparse_notes = [0 for i in range(12)]

            # 構成音は1
            for note in notes:
                sparse_notes[note] = 1

            # ベース音は2
            sparse_notes[notes[0]] = 2

            notes = sparse_notes

        return notes

    def reconfigured(self):
        """
        コードを再構成します。
        :return: 再構成されたコード
        :rtype: Chord
        """

        rec_chord = utils.notes_to_chords(self.get_notes())[0]

        if rec_chord.is_on_chord:
            bass_chord = rec_chord.bass.transposed(0, rec_chord.root.raw_note_text)
            rec_chord = Chord(rec_chord.root.raw_note_text +
                              rec_chord.quality.raw_quality_text +
                              "/" + bass_chord.normed_note_text, scale_text=self.__scale_text)
        else:
            rec_chord = Chord(rec_chord.root.raw_note_text +
                              rec_chord.quality.raw_quality_text, scale_text=self.__scale_text)

        return rec_chord
