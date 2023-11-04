#!/usr/local/bin/python3

import greek_letter as gl

# Morphology in NET:
#   (N-noun)(case)(gender)(person)(number)
#   (V-verb)(mood)(tense)(voice)(case)(gender)(person)(number)

# mood
#   I (I) indicative - a fact
#   M (M) imperative - a command
#   S (S) subjective - hypothetical, wishes, conditions, possibilities
#   N (N) infinitive - action w/o a person
#   P (P) participle
#
# tense
#   P (P) present (present, ongoing)
#   I (I) imperfect (past, ongoing)
#   F (F) future (future, simple or ongoing)
#   A (A) aorist (past, simple)
#   R (RX) perfect (present, completed)
#   Y (Y) pluperfect (past, completed)
#   U ( ) future perfect (future, completed)
#
# voice
#   A (A) active
#   P (P) passive
#   M (M) middle
#
# case
#   A (A) Accusative
#   D (D) dative
#   G (G) genitive
#   N (N) nominative
#

# gender
#   M (M) male
#   F (F) female
#   N (N) neuter
#
# person
#   1 (1) 1st person (me)
#   2 (2) 2nd person (you)
#   3 (3) 3rd person (someone else)
#
# number
#   S (S) singluar
#   P (P) plural
#   D ( ) dual
#

_endings = {
    "IPA": {
        "1S": "μι",
        "1P": "μεν",
        "2S": "σ",
        "2P": "τε",
        "3S": "σι", # ν
        "3P": "ασι", # ν
    },
    "NPA" : "ναι",
}

_special_words = {
    # CH 5
    # meaning: to be
    # -old-> older than koine, εσ -> εε
    # -vc-> vowel contraction
    # -pro-> changes in pronunciation over time
    "ἐσ": {
        "IPA": {
            "1S": "εἰμί", # εσ -> ἐσμί -old-> εεμι -vc-> εἰμί, in the dictionary
            "1P": "ἐσμέν", # εσ -> εσμεν
            "2S": "εἶ", # εσ -old-> εσσι -old(drop σ)-> εε -vc-> ει
            "2P": "ἐστέ", # εσ -> εστε
            "3S": "ἐστί", # εσ -old-> εστι
            "3P": "εἰσί", # εσ -old-> εσντι -pro-> εισι
        },
        "NPA": "εἶναι",
    },
    "φα,φη": { # stem for singluar and plural
        "IPA": {
            "1S": "φημί", # φη -> φημι, in the dictionary
            "1P": "φαμέν", # φα -> φαμεν
            "2S": "φῄς", # φη -> φησ
            "2P": "φατέ", # φα -> φατε
            "3S": "φησί", # φη -> φησι
            "3P": "φασί", # φα -> φαασι -> φασι
        },
        "NPA": "φάναι",
    },
}

# dictionary seems to be Present, Indicative, Active
def inflect(stem, tmv, pn):
    """
    tmv - str with (tense, mood, voice)
        tense
          - present
          < past
          > future
          = present perfect
          [ past perfect (pluperfect)
          ] future perfect
          A aorist
        mood
          D indicative - a fact
          P imperative - a command
          J subjective - hypothetical, wishes, conditions, possibilities
          F infinitive - action w/o a person
        voice
          A active
          P passive
    pn - str with (person, number)
    """

    pn_to_ending = _endings.get(tmv, None)
    if not pn_to_ending:
        return None, None
    if type(pn_to_ending) == str:
        ending = pn_to_ending
    else:
        ending = pn_to_ending.get(pn, None)
        if not ending:
            return None, None

    word, _dbg = gl.vocal_modifications(stem + ending)

    return word, _dbg


####################
# stems
####################

_stem_ends = [
    "",
    "η",
    "α",
    "ια",

    "ο",
    "γο",
    "πο",
    "ιο",

    "ος",
    "ης",
    "οντ",
    "ορ",
    "ιδ",
    "ων",
    "ατ",
    "σι",
]
_stem_ends.extend((let + "α" for let in gl._lower_consonants))
_stem_ends.extend((let + "η" for let in gl._lower_consonants))
_stem_ends.extend((let + "ε" for let in gl._lower_consonants))
_stem_ends.extend((let for let in gl._lower_consonants if let != 'σ'))
_stem_ends.extend((let + "ιδ" for let in gl._lower_consonants))
_stem_ends.extend((let + "οδ" for let in gl._lower_consonants))
_stem_ends.extend((let + "ον" for let in gl._lower_consonants))
_stem_ends.extend((let + "ι" for let in gl._lower_consonants))
_stem_ends.extend((p + d for p in gl._palatals for d in gl._dentals))
_stem_ends.extend((l + d for l in gl._labials for d in gl._dentals))

_stem_ends = list(set(_stem_ends))

_end_to_end_and_mtvpn_list = {}


for stem_end in _stem_ends:
    for mtv in ["IPA", "NPA"]:
        for pn in ["1S", "2S", "3S", "1P", "2P", "3P"]:
            if mtv == "NPA":
                pn = ""
            word, _dbg = inflect("βββ" + stem_end, mtv, pn)

            word_end = gl.clean_word(word[3:])

            listof_end_mtvpn = _end_to_end_and_mtvpn_list.get(word_end, None)
            if not listof_end_mtvpn:
                listof_end_mtvpn = []
                _end_to_end_and_mtvpn_list[word_end] = listof_end_mtvpn
            listof_end_mtvpn.append((stem_end, mtv + pn))
            if not pn:
                break

def derive_stem(word):
    for i in range(4,0,-1):
        word_end = word[-i:]
        listof_end_mtvpn = _end_to_end_and_mtvpn_list.get(word_end, None)
        if listof_end_mtvpn:
            if len(listof_end_mtvpn) == 1:
                end_mtvpn = listof_end_mtvpn[0]
                stem_end = end_mtvpn[0]
                word = word[:-i] + stem_end
                return word, end_mtvpn[1]
            else:
                return None, repr(listof_end_mtvpn)
    return None, "nothing"

