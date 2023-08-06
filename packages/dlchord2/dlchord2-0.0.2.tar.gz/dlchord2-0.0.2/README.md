# DL-Chord2
[![PyPI](https://img.shields.io/pypi/v/dlchord.svg)](https://pypi.org/project/dlchord2)
[![Build Status](https://travis-ci.com/anime-song/DL-Chord.svg?branch=master)](https://travis-ci.com/anime-song/DLChord2)
## 概要
和音を解析するライブラリ。

以下のようなことができます。

- 構成音の解析
- 移調
- 構成音からコード検索

## インストール
```sh
$ pip install dlchord2
```

## コード作成
```python
>>> from dlchord2 import Chord
>>> chord = Chord("C")
>>> chord
<Chord: C>
```

## コード検索
```python
>>> from dlchord2 import notes_to_chord
>>> chords = notes_to_chord(["C", "E", "G"])
>>> chords
[<Chord : C>]

>>> chords = notes_to_chord(["B", "Db", "F", "A"])
>>> chords
[<Chord: Faug/B>, <Chord: Dbaug/B>, <Chord: Aaug/B>]

>>> chords = notes_to_chord(["B", "Db", "F", "A"], scale="F#")
>>> chords
[<Chord: Faug/B>, <Chord: C#aug/B>, <Chord: Aaug/B>]
```

## ルート音取得
```python
>>> from dlchord2 import Chord
>>> chord = Chord("C")
>>> print(chord.root)
<Note: C>

>>> from dlchord2 import Chord
>>> chord = Chord("C/G")
>>> print(chord.root)
<Note: C>

```

## ベース音取得
```python
>>> from dlchord2 import Chord
>>> chord = Chord("C")
>>> print(chord.bass)
<Note: C>

>>> from dlchord2 import Chord
>>> chord = Chord("C/G")
>>> print(chord.bass)
<Note: G>

```


## 移調
```python
>>> from dlchord2 import Chord
>>> chord = Chord("C")
>>> t_chord = chord.transposed(steps=1)
>>> t_chord
<Chord: Db>
```

## コード最適化
```python
>>> from dlchord2 import Chord
>>> chord = Chord("E/Ab")
>>> chord.reconfigured()
E/G#

>>> chord = Chord("AM7/F#")
>>> chord.reconfigured()
F#m7(9)
```


## 構成音取得
```python
>>> from dlchord2 import Chord
>>> chord = Chord("C")
>>> cons = chord.getNotes(sparse=False)
>>> print(cons)
[0 4 7]

>>> cons = chord.getNotes(sparse=True)
>>> print(cons)
[2. 0. 0. 0. 1. 0. 0. 1. 0. 0. 0. 0.]
# ベース音 2
# 構成音 1
# 非構成音 0
```

## コードを比較
```python
>>> from dlchord2 import Chord
>>> Chord("C") == Chord("C")
True
>>> Chord("C") == Chord("C7")
False
>>> Chord("C#") == Chord("Db")
True
>>> Chord("F/D") == Chord("Dm7")
True
>>> Chord("C#dim7/A") == Chord("A7(b9)")
True
```
