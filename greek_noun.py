#!/usr/local/bin/python3

import itertools as it
import greek_letter as gl

_dbg_on = False
_morph_do_long_alpha = False
_guess_alpha_eta_omicron = True

# Koine Greek evloved from Attic Greek

# Nominative: subject (does the verb) or predicate nominative
# Genitive: posession, noun of GEN
# Dative: indirect object, (subject verb object) to DAT
# Accusative: object of a transitive verb, direct object of verbs
# Vocative: JOE, what are you doing?

# DGNC - (declension, gender, number, case)

# 1st
#   M ends in ης ας
#   F ends in η  α
# 2nd
#   M: ends in ος
#   F: ends in ος
#   N: ends in ον

# 1st, fem:
# _noun_stems['1']['F'] ... ['SP']['NGDAV']
#       N   G   D   A   V
#       --- --- --- --- ---
#   S:  .   .υ  i   .ν  .
#   P:  αι  ων  αις ᾱς  αι

# 1st, mas:
# _noun_stems['1']['M'] ... ['SP']['NGDAV']
#       N   G   D   A   V
#       --- --- --- --- ---
#   S:  .ς  ου  i   .ν  .
#   P:  αι  ων  αις ᾱς  αι

# 2nd, mas/fem:
# _noun_stems['2']['M','F'] ... ['SP']['NGDAV']
#       N   G   D   A   V
#       --- --- --- --- ---
#   S:  .ς  .υ  ῳ   .ν  ε
#   P:  .ι  ων  .ις .υς .ι

# 3rd, mas/fem:
# _noun_stems['-']['M','F'] ... ['SP']['NGDAV']
#       N   G   D   A   V
#       --- --- --- --- ---
#   S:  ς   ος  ι   α/ν
#   P:  ες  ων  σι  ας  ες


# see _noun_stems
# see _vowel_contract


####################
# articles
####################

article_base = (
# singular --------------
#   mas     fem     neu
    "ο",    "η",    "το",       # nominative
    "του",  "της",  "του",      # genative
    "τω",   "τη",   "τω",       # dative
    "τον",  "την",  "το",       # accusative
# plural ----------------
#   mas     fem     neu
    "οι",   "αι",   "τα",       # nominative
    "των",  "των",  "των",      # genative
    "τοις", "ταις", "τοις",     # dative
    "τους", "τας",  "τα")       # accusative

article_to_indexes = {}
for article, index in zip(article_base, range(2*3*4)):
    if not article in article_to_indexes:
        article_to_indexes[article] = []
    article_to_indexes[article].append(index)


####################
# noun inflection
####################

# url: https://en.wiktionary.org/wiki/Appendix:Ancient_Greek_first_declension
# url: https://en.wiktionary.org/wiki/Appendix:Ancient_Greek_second_declension
# url: https://en.wiktionary.org/wiki/Appendix:Ancient_Greek_third_declension

# "." -> keep last letter
# missing "." -> remove last letter
# "i" -> perform iota subscript on the last letter
_noun_stems = {
    # 1st declension
    # D1 M ends in ης ας
    # D1 F ends in η α
    '1': {
        'F': {
            'S': {
                'N': ".",
                'V': ".",
                'A': ".ν",
                'G': ".σ",
                'D': "i",
            },
            'P': {
                'N': "αι",
                'V': "αι",
                'A': "ᾱσ",
                'G': "ων",
                'D': "αισ",
            },
            'D': {
                'N': "ᾱ",
                'V': "ᾱ",
                'A': "ᾱ",
                'G': "aιν",
                'D': "aιν",
            }
        },
        'M': {
            'S': {
                'N': ".σ",
                'V': ".",
                'A': ".ν",
                'G': "ου",
                'D': "i",
            },
            'P': {
                'N': "αι",
                'V': "αι",
                'A': "ᾱσ",
                'G': "ων",
                'D': "αισ",
            },
            'D': {
                'N': "ᾱ",
                'V': "ᾱ",
                'A': "ᾱ",
                'G': "aιν",
                'D': "aιν",
            }
        },
        # TODO: copy of M, needs to be corrected
        'N': {
            'S': {
                'N': ".σ",
                'V': ".",
                'A': ".ν",
                'G': "ου",
                'D': "i",
            },
            'P': {
                'N': "αι",
                'V': "αι",
                'A': "ᾱσ",
                'G': "ων",
                'D': "αισ",
            },
            'D': {
                'N': "ᾱ",
                'V': "ᾱ",
                'A': "ᾱ",
                'G': "aιν",
                'D': "aιν",
            }
        },
    },
    # 2nd declension
    # M: ending is ος
    # F: ending is ος
    # N: ending is ον
    '2': {
        'M': {
            'S': {
                'N': ".σ",
                'G': ".υ",
                'D': "ῳ",
                'A': ".ν",
                'V': "ε",
            },
            'P': {
                'N': ".ι",
                'G': "ων",
                'D': ".ισ",
                'A': ".υσ",
                'V': ".ι",
            },
            'D': {
                'N': "ω",
                'G': ".ιν",
                'D': ".ιν",
                'A': "ω",
                'V': "ω",
            }
        },
        'F': {
            'S': {
                'N': ".σ", # no change
                'G': ".υ",
                'D': "ῳ",
                'A': ".ν",
                'V': "ε",
            },
            'P': {
                'N': ".ι",
                'G': "ων",
                'D': ".ισ",
                'A': ".υσ",
                'V': ".ι",
            },
            'D': {
                'N': "ω",
                'G': ".ιν",
                'D': ".ιν",
                'A': "ω",
                'V': "ω",
            }
        },
        'N': {
            'S': {
                'N': ".ν", # no change
                'G': ".υ",
                'D': "ῳ",
                'A': ".ν",
                'V': ".ν",
            },
            'P': {
                'N': "α",
                'G': "ων",
                'D': ".ισ",
                'A': "α",
                'V': "α",
            },
            'D': {
                'N': "ω",
                'G': ".ιν",
                'D': ".ιν",
                'A': "ω",
                'V': "ω",
            }
        },
    },
    # 3rd declension
    # consonants
    '3': {
        '-': {
            'S': {
                'N': ".σ",
                'G': ".οσ",
                'D': ".ι",
                'A': ".α",   # or ν
                'V': ".",    # or σ
            },
            'P': {
                'N': ".εσ",
                'G': ".ων",
                'D': ".σι",
                'A': ".ασ",
                'V': ".εσ",
            },
            'D': {
                'N': ".ε",
                'G': ".σιν",
                'D': ".σιν",
                'A': ".ε",
                'V': ".ε",
            },
        },
        'N': {
            'S': {
                'N': ".",
                'G': ".οσ",
                'D': ".ι",
                'A': ".",   # or ν
            },
            'P': {
                'N': ".α",
                'G': ".ων",
                'D': ".σι",
                'A': ".α",
            },
        },
    },
}

# see https://en.wiktionary.org/wiki/Appendix:Ancient_Greek_contraction
_vowel_contract = {
    # Attic Greek Below
    'αα': 'ᾱ',
#    'εα': 'η',
    'οα': 'ὰ', # different that Attic

    'αε': 'ᾱ',
    'εε': 'ει',
    'ηε': 'η',
    'οε': 'ον',

    'ηι': 'η',

#    'αο': 'ω',
    'εο': 'ον',
    'οο': 'ον',

    'αοι': 'ω',
    'εοι': 'οι',
    'ηοι': 'ω',
    'οοι': 'οι',

#    'αου': 'ω',
    'εου': 'οι',
    'οου': 'οι',

    'αη': 'α',
    'εη': 'η',
    'ηη': 'η',
#    'οη': 'ω',

    'αω': 'ω',
    'εω': 'ω',
    'οω': 'ω',

    # Koine Greek ???
    'ουι': 'ου',
#    'ονν': 'αν',

    # non-vowel contractions
    'σου': 'σαι',
#    'ρου': 'ρος',
    'ονς': 'ων',
}

_stop_xform_consonants = dict(
    list(zip(gl._labials, it.repeat('ψ'))) +
    list(zip(gl._palatals, it.repeat('ξ'))) +
    list(zip((p + d for p in gl._palatals for d in gl._dentals), it.repeat('ξ'))) +
    list(zip((l + d for l in gl._labials for d in gl._dentals), it.repeat('ψ'))) +
    list(zip(gl._dentals, it.repeat(''))))
_stop_xform_consonants["ν"] = "ν"
_stop_xform_consonants["δ"] = "σ"

def _noun_inflect(stem, decl, gen, num, case, do_dbg=True):
    if decl == "3" and gen in "MF":
        gen = "-"
    end = _noun_stems[decl][gen][num][case]

    _dbg = None
    if do_dbg: _dbg = [(stem + "-" + end, "start")]

    stem_ending = gl.base_let(stem[-1])
    if decl != '3':

        # swap η with α for plural (genative|dative), sometimes singular
        if gen == "F" and case in "GD":
            if stem_ending in 'αη':
                if stem_ending == 'α':
                    new_last_let = 'η'
                else:
                    new_last_let = 'α'

                if num == "P" or (num == "S" and stem in ["θάλασσα", "δόξα", "γέεννα"]):
                    stem = stem[:-1] + gl.cp_morph(new_last_let, stem[-1])
                    if do_dbg: _dbg.append((stem + "-" + end, "%s->%s"%(stem_ending, new_last_let)))

                # this should only be done sometimes
                if num == "S":
                    if do_dbg: _dbg.append((stem + "-" + end, "skip %s->%s"%(stem_ending, new_last_let)))

    # apply the ending
    if end[0] == ".":
        end = end[1:]
        stem = stem + end
    elif end[0] == "i":
        if gl.base_let(stem[-1]) in "ηαο":
            end = gl.add_morph(stem[-1], "i") + end[1:]
            stem = stem[:-1] + end
            if do_dbg: _dbg.append((stem, "iota_subscript"))
        else:
            end = end[1:]
            stem = stem + end
            if do_dbg: _dbg.append((stem, "iota_sub_oops"))
    else:
        stem = stem[:-1] + end
        if do_dbg: _dbg.append((stem, "combine_rm_last"))

    b_stem = gl.base_word(stem)

    if end and end[0] == 'σ':
        stem_ending = gl.base_word(stem[-len(end)-3:-len(end)])
        if stem_ending == 'οντ' and end == 'σ':
            replace = 'ων'
        else:
            stem_ending = stem_ending[-2:]
            replace = _stop_xform_consonants.get(stem_ending, None)
            if not replace:
                if stem_ending == 'ον' and end == 'σ':
                    replace = 'ων'
                elif stem_ending == 'οδ' and end == 'σ':
                    replace = 'ουσ'
                elif stem_ending == 'ον' and end == 'σι':
                    replace = 'οσ'
                elif stem_ending == 'ντ' and end == 'σι':
                    replace = 'υσ'
                else:
                    # κτσ -> ξ
                    # already: κσ -> ξ
                    # already: τσ -> ""
                    stem_ending = stem_ending[-1]
                    replace = _stop_xform_consonants.get(stem_ending, None)
        if replace:
            stem = stem[:-len(end)-len(stem_ending)] + replace + end[1:]
            if do_dbg: _dbg.append((stem, stem_ending + "σ->" + replace))

    i_last_v = len(stem)-1
    # find last vowel
    while i_last_v >= 0 and not b_stem[i_last_v] in gl._lower_vowel_set:
        i_last_v -= 1
    if i_last_v >= 0:
        # vowel contraction
        # affects 2 or 3 vowels together
        # done before moving morphs
        if i_last_v > 0 and b_stem[i_last_v-1] in gl._lower_vowel_set:

            # try 3 letters ending at last vowel
            # (if i_last_v > 3) for θεοῦ
            if i_last_v > 3:
                find = b_stem[i_last_v-2:i_last_v+1]
                replace = _vowel_contract.get(find, None)
                if replace:

                    # if this would create a double-vowel, don't
                    ii = 0
#                    if replace[-1] == stem[i_last_v+1:i_last_v+2]:
#                        ii = 1

                    replace = replace[:-1] + gl.cp_morph(gl.cp_morph(gl.cp_morph(replace[-1], stem[i_last_v-2]), stem[i_last_v-1]), stem[i_last_v])
                    stem = stem[:i_last_v-2] + replace + stem[i_last_v+1+ii:]
                    b_stem = b_stem[:i_last_v-2] + replace + b_stem[i_last_v+1+ii:]

                    i_last_v -= 3 - len(replace) + ii
                    if do_dbg: _dbg.append((stem, "contract-3", find, replace))

            # try 2 letters ending at last vowel
            # (if i_last_v > 2) for θεὸσ and λαῷ
            if i_last_v > 2 and b_stem[i_last_v-1] in gl._lower_vowel_set:
                find = b_stem[i_last_v-1:i_last_v+1]
                replace = _vowel_contract.get(find, None)
                if not replace and b_stem[i_last_v-1] == b_stem[i_last_v]:
                    replace = gl.cp_morph(stem[i_last_v-1], stem[i_last_v])
                if replace:
                    # if this would create a double-vowel, don't
                    ii = 0
                    if replace[-1] == stem[i_last_v+1:i_last_v+2]:
                        ii = 1

                    stem = stem[:i_last_v-1] + replace + stem[i_last_v+1+ii:]
                    b_stem = b_stem[:i_last_v-1] + gl.base_word(replace) + b_stem[i_last_v+1+ii:]
                    i_last_v -= 2 - len(replace) + ii
                    if do_dbg: _dbg.append((stem, "contract-2", find, replace))

        # moving morphs to the last vowel in diphthongs
        if i_last_v > 0 and b_stem[i_last_v-1:i_last_v+1] in gl._diphthongs:
            # move accent from beginning to end of diphthong
            # affects [αεου][ιυ]
            let1 = stem[i_last_v-1]
            let1_morph = gl.get_morph(let1)
            let1 = gl.base_let(let1)

            let2 = gl.add_morph(stem[i_last_v], let1_morph)
            if let2 != stem[i_last_v]:
                stem = stem[:i_last_v-1] + let1 + let2 + stem[i_last_v+1:]
                if do_dbg: _dbg.append((stem, "mv"))

        # accent translation
        if case == 'G' and num == 'S':
            word2 = gl.translate_morph(stem, i_last_v, "\\", "~")
            if word2:
                stem = word2
                if do_dbg: _dbg.append((stem, "\\ -> ~"))
        if case == 'D' and num == 'P':
            word2 = gl.translate_morph(stem, i_last_v, "/", "~")
            if word2:
                stem = word2
                if do_dbg: _dbg.append((stem, "/ -> ~"))
        if case in 'N' and num == 'P':
            word2 = gl.translate_morph(stem, i_last_v, "/", "\\")
            if word2:
                stem = word2
                if do_dbg: _dbg.append((stem, "/ -> \\"))
        if case in 'A' and num == 'P':
            word2 = gl.translate_morph(stem, i_last_v, "\\", "/")
            if word2:
                stem = word2
                if do_dbg: _dbg.append((stem, "\\ -> /"))

    # for dative: place iota subscript on vowel followed by iota
    # only for dative-singular
    # affects [ηαο]ι
    if case == 'D' and num == 'S':
        if b_stem[-1] == 'η':
            # ἐργάτῃ
            # τρίτῇ->τρίτῃ (.F.)
            # -----
            # κριτῃ->κριτῇ (M.N)
            if b_stem[-2] in ['φ', 'θ'] or (b_stem[-2] == 'τ' and gen != 'F'):
                if stem[-1] != 'ῇ':
                    stem = stem[:-1] + 'ῇ'
                    if do_dbg: _dbg.append((stem, "DS(η)->iota.1"))
            else:
                if stem[-1] != 'ῃ':
                    stem = stem[:-1] + 'ῃ'
                    if do_dbg: _dbg.append((stem, "DS(η)->iota.2"))

    # alphas at the end of the stem have "long" mark
    # unless it is morphed already
    if _morph_do_long_alpha:
        if num == 'S' or case == 'A':
            if stem[-1] == 'α':
                stem = stem[:-1] + 'ᾱ'
                if do_dbg: _dbg.append((stem, "long-1"))
            elif stem[-2] == 'α':
                stem = stem[:-2] + 'ᾱ' + stem[-1]
                if do_dbg: _dbg.append((stem, "long-2"))

    # set last sigma
    if gl.base_let(stem[-1]) == 'σ':
        stem = stem[:-1] + gl.cp_morph('ς', stem[-1])

    return (stem, _dbg)

# D1 M ends in ης ας
# D1 F ends in η α
#   1: [MF]:[SPD]:[NAGDV] -> [.iα]α*
# D2 [MF]: ending is ος
# D2 [N]: ending is ον
#   2: [MFN]:[SPD]:[NAGDV] -> [.iα]α*
# D3 consonants
#   3: [-]:[SPD]:[NAGDV] -> [.iα]α*
def decl_gen(stem, gen):
    b_stem = gl.base_word(stem)
    last_let = b_stem[-1]
    last_2_let = b_stem[-2:]

    if last_2_let in ["ης", "ας"]:
        decl = "1"
        gen = "M"
    elif last_let in "αη":
        decl = "1"
        gen = "F"
    # not sure, but probably true
    elif last_let == "ο":
        decl = "2"
        gen = "M"
    elif last_2_let == "ος":
        decl = "3"
        gen = "-"
    elif last_2_let == "ον":
        decl = "3"
        gen = "N"
    else:
        decl = "3"
        gen = "-" # gender doesn't matter

    return (decl, gen)


def noun_inflect(stem, gen, num, case):
    decl, gen = decl_gen(stem, gen)
    return _noun_inflect(stem, decl, gen, num, decl)

def noun_inflect_all(stem, gen, decl=None):
    """
    returns a list of 1 or 2 answers, each answer containing (decl, gen, words)
        decl in ["1", "2", "3"]
        gen in ["M", "F", "N"]
        words[num][case] contains (word, _dbg list)
    """
    if not decl:
        decl, gen2 = decl_gen(stem, gen)
        if gen == "-":
            gen = gen2

    if decl == "2" and gen == "-":
        gens = ["M", "F"]
    else:
        gens = [gen]

    gen3 = gen
    if decl == "3":
        gen3 = "-"

    answers = []
    for gen in gens:
        words = {}
        answers.append((decl, gen, words))
        for num in ('S', 'P'):
            num_words = words[num] = {}
            for case in ('N', 'G', 'D', 'A'):
                if stem:
                    num_words[case] = _noun_inflect(stem, decl, gen3, num, case)
                else:
                    num_words[case] = ("", [])
    return answers

def print_noun_1(stem, decl, gen):
    for decl, gen, data in noun_inflect_all(stem, gen, decl):
        max_len = max((
            len(word_dbg[0])
            for case_to_word_dbg in data.values()
            for word_dbg in case_to_word_dbg.values()))

        print("-------------------- decl=%s gen=%s "%(decl, gen))
        print("{5:6s} {1:{0}s} {2:{0}s} {3:{0}s} {4:{0}s}".format(
            max_len+2,
            "nom", "gen", "dat", "acc",
            stem,
            ))
        for num in ('S', 'P'):
            print("{5:s}:    {1:{0}s} {2:{0}s} {3:{0}s} {4:{0}s}".format(
                max_len+2,
                data[num]["N"][0],
                data[num]["G"][0],
                data[num]["D"][0],
                data[num]["A"][0],
                num,
                ))
        for num in "SP":
            for case in "NGDA":
                print(data[num][case][1])
                

####################
# transform
####################

_stem_ends = [
#    ("1", "M", "ης"),
#    ("1", "M", "ας"),
    ("1", "F", "η"),
    ("1", "F", "α"),

    ("2", "MF", "ο"),

    ("3", "MF", "ος"),
    ("3", "M", "οντ"),
    ("3", "M", "ον"),
    ("3", "M", "οδ"),
]
_stem_ends.extend((("3", "-", let) for let in gl._lower_consonants))
_stem_ends.extend((("3", "M", p + d) for p in gl._palatals for d in gl._dentals))
_stem_ends.extend((("3", "M", l + d) for l in gl._labials for d in gl._dentals))

_end_to_end_and_dgnc_list = {}
for decl, gens, end in _stem_ends:
    for gen in gens:
        for num in "SP":
            for case in "NGDA":
                word, _dbg = _noun_inflect("βββ" + end, decl, gen, num, case)

                word_end = gl.base_word(word[3:])

                listof_end_dgnc = _end_to_end_and_dgnc_list.get(word_end, None)
                if not listof_end_dgnc:
                    listof_end_dgnc = []
                    _end_to_end_and_dgnc_list[word_end] = listof_end_dgnc
                if gen == "-":
                    listof_end_dgnc.append((end, decl + "M" + num + case))
                    listof_end_dgnc.append((end, decl + "F" + num + case))
                    listof_end_dgnc.append((end, decl + "N" + num + case))
                else:
                    listof_end_dgnc.append((end, decl + gen + num + case))

def gnc_set_from_article(article):
    return set((
        "MFN"[i%3] + "SP"[(i//12)] + "NGDA"[(i//3)%4]
        for i in article_to_indexes[article]))

# DGNC - (declension, gender, number, case)
def derive_stem_given_article(article, word, existing_stems=None):
    GNC_set = gnc_set_from_article(article)
    return derive_stem_given_GNC(GNC_set, word, existing_stems)

def derive_stem_given_GNC(GNC_set, word, existing_stems=None):
    """
    params:
        GNC_set - a set of strings with the first char of (Gender, Number, Case) which this word may be
        word - the word
    return (stem word, DGNC)
    """
    # for display only
    GNC_list = list(GNC_set)
    GNC_list.sort()

    b_word = gl.base_word(word)
    for i in range(4,0,-1):
        word_end = b_word[-i:]
        listof_end_dgnc = _end_to_end_and_dgnc_list.get(word_end, None)
        if listof_end_dgnc:
            if _dbg_on:
                print("CP0 %s %d -> ends:%s art:%s"%(word, i, repr(listof_end_dgnc), repr(GNC_list)))
            word_start = word[:-i]
            filtered_end_dgnc = list(filter(
                lambda end_dgnc: end_dgnc[1][1:] in GNC_set and (
                    not existing_stems
                    or gl.base_word(word_start) + end_dgnc[0] in existing_stems),
                listof_end_dgnc))
            common_ends = set(map(lambda end_dgnc: end_dgnc[0], filtered_end_dgnc))
            if len(common_ends) == 1:
                stem = word_start + filtered_end_dgnc[0][0]
                dgnc = filtered_end_dgnc[0][1]
                if _dbg_on:
                    print("CProot (%s, %s) (%s %s) common:%s"%(dgnc, stem, b_word, word, repr(common_ends)))
                return (stem, dgnc)
            if common_ends:
                if _dbg_on:
                    common_ends = list(common_ends)
                    common_ends.sort()
                    print("CP1 common:%s"%(repr(common_ends)))

            if existing_stems:
                # TODO: this section "guesses" the right answer
                # there may be better heuristics here, but is it worth the time?
                if _guess_alpha_eta_omicron:
                    filtered_end_dgnc = list(filter(
                        lambda end_dgnc: end_dgnc[1][1:] in GNC_set,
                        listof_end_dgnc))
                    first_letters = set((end[0] for end, dgnc in filtered_end_dgnc))
                    for first_letter in first_letters:
                        if first_letter not in "αηο":
                            break
                    else:
                        last_letters = set((end[1:] for end, dgnc in filtered_end_dgnc))
                        if len(last_letters) == 1:
                            # prefere alpha
                            filtered_end_dgnc.sort()

                            stem = word_start + filtered_end_dgnc[0][0]
                            dgnc = filtered_end_dgnc[0][1]
                            if _dbg_on:
                                print("CP2 (%s %s) (%s %s) %s %s %s"%(dgnc, stem, b_word, word, repr(GNC_list), repr(listof_end_dgnc), repr(common_ends)))
                            return (stem, dgnc)
                if _dbg_on:
                    print("CP3 (%s %s) %s+%s %s | %s"%(gl.base_word(word), word, word_start, word_end, repr(listof_end_dgnc), repr(GNC_list)))

    return (None, None)


if __name__ == '__main__':
    _dbg_on = True
    while True:
        word = input("noun: ")
        if word:
            stem, dgnc = derive_stem_given_GNC(set(["MSN", "FSN"]), word)
            if stem:
                print("stem: " + stem)
                print("DGNC: " + dgnc)
                decl = dgnc[0]
                gen = dgnc[1]
            else:
                print("stem not derived")
        else:
            stem = input("stem: ")
            decl = input("decl: ")
            gen = input("gen: ")
        if stem:
            print_noun_1(stem, decl, gen)


