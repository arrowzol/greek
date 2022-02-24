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

_verb_stems_1 = {
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
}

_exceptions = {
    # CH 4
    "δεικ": {
        # add "νυ" for present tense
        "-DA": {
            "1": {
                "S": "δείκνυμι", # in the dictionary
                "P": "δείκνυμεν", #
            },
            "2": {
                "S": "δείκνυς", #
                "P": "δείκνυτε", #
            },
            "3": {
                "S": "δείκνυσι", #
                "P": "δεικνύασι", #
            },
        },
        "-FA": "δεικνύναι" ,
    },
    "μιγ": {
        # add "νυ" for present tense set of μιγνυ
        "-DA": {
            "1": {
                "S": "μίγνυμι", # in the dictionary
                "P": "μίγνυμεν", #
            },
            "2": {
                "S": "μίγνυς", #
                "P": "μίγνυτε", #
            },
            "3": {
                "S": "μίγνυσι", #
                "P": "μιγνύασι", #
            },
        },
        "-FA": "μιγνύναι" ,
    },
    "απόλ": {
        # add "λυ" for present tense set of απόλλυ
        "-DA": {
            "1": {
                "S": "απόλλυμι", # in the dictionary
                "P": "απόλλυμεν", #
            },
            "2": {
                "S": "απόλλυς", #
                "P": "απόλλυτε", #
            },
            "3": {
                "S": "απόλλυσι", #
                "P": "απoλλύασι", #
            },
        },
        "-FA": "απoλλύναι" ,
    },

    # CH 5
    # meaning: to be
    # -old-> older than koine, εσ -> εε
    # -vc-> vowel contraction
    # -pro-> changes in pronunciation over time
    "ἐσ": {
        "-DA": {
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
        "-FA": "εἶναι",
    },
    "φα,φη": { # stem for singluar and plural
        "-DA": {
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
        "-FA": "φάναι",
    },

    # CH 6
    # δίδωμι give
    "δω": {
        # present tense: δω -> διδω (REDUPLICATES the initial consonant)
        "-DA": {
            "1": {
                "S": "δίδωμι", # in the dictionary
                "P": "δίδομεν", # 
            },
            "2": {
                "S": "δίδως", # 
                "P": "δίδοτε", # 
            },
            "3": {
                "S": "δίδωσι", # 
                "P": "διδόασι", #
            },
        },
        "-FA": "διδόναι",
    },
    # τίθημι put, make
    "θη": {
        # present tense: θη -> θιθη (REDUPLICATES the initial consonant) -> τιθη (replace aspirated with unaspirated)
        "-DA": {
            "1": {
                "S": "τίθημι", # in the dictionary
                "P": "τίθεμεν", # 
            },
            "2": {
                "S": "τίθης", # 
                "P": "τίθετε", # 
            },
            "3": {
                "S": "τίθησι", # 
                "P": "τιθέασι", #
            },
        },
        "-FA": "διδόναι",
    },

    # ἵστημι stand
    # ἵημι throw
}

# dictionary seems to be Present, Indicative, Active
def build(tense, person, number, mood, voice, stem):
    if tense = '-':
        first_let = gl.lower(gl.base_let(stem[0]))
        if first_let in gl._lower_vowel_set:
            redup = _aspirated_to_unaspirated.get(first_let, first_let) + 'ι'
            stem = redup + stem + 'ν' + _verb_stems_1[person][number]
        else:
            stem = stem + 'νυ' + _verb_stems_1[person][number]
        # TODO: CH 6, long stem shortens in plural
    else
        return
    # TODO: mood, voice
    return stem

