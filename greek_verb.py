#!/usr/local/bin/python3

import greek_letter as gl

# person
#   1 1st person (me)
#   2 2nd person (you)
#   3 3rd person (someone else)
# number
#   S singluar
#   P plural
# tense
#   - present
#   < past
#   > future
#   = present perfect
#   [ past perfect (pluperfect)
#   ] future perfect
# mood
#   D indicative - a fact
#   P imperative - a command
#   J subjective - hypothetical, wishes, conditions, possibilities
#   F infinitive - action w/o a person
# voice
#   A active
#   P passive

_verb_stems_2 = {
    "-FA": "ναι",
    "-DA": "νυ",
}

_verb_stems_1 = {
    "-IA": {
        "1": {
            "S": "μι",
            "P": "μεν",
        },
        "2": {
            "S": "σ",
            "P": "τε",
        },
        "3": {
            "S": "σι",
            "P": "ασι",
        },
    },
}

_exceptions = {
    # most common verb
    # meaning: to be
    # -old-> older than koine, εσ -> εε
    # -vc-> vowel contraction
    # -pro-> changes in pronunciation over time
    "ἐσ": {
        "-IA": {
            "1": {
                "S": "εἰμί", # εσ -> ἐσμί -old-> εεμι -vc-> εἰμί, in the dictionary
                "P": "ἐσμέν", # εσ -> εσμεν
            },
            "2": {
                "S": "εἶ", # εσ -old-> εσσι -old(drop σ)-> εε -vc-> ει
                "P": "ἐστέ", # εσ -> εστε
            },
            "3": {
                "S": "ἐστί", # εσ -old-> εστι
                "P": "εἰσί", # εσ -old-> εσντι -pro-> εισι
            },
        },
    },
    "φα,φη": { # stem for singluar and plural
        "-FA": {
            "1": {
                "S": "φημί", # φη -> φημι, in the dictionary
                "P": "φαμέν", # φα -> φαμεν
            },
            "2": {
                "S": "φῄς", # φη -> φησ
                "P": "φατέ", # φα -> φατε
            },
            "3": {
                "S": "φησί", # φη -> φησι
                "P": "φασί", # φα -> φαασι -> φασι
            },
        },
    },
}

