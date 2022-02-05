#!/usr/local/bin/python3

# Koine Greek evloved from Attic Greek

# Nominative: subject
# Genitive: posession
# Dative: indirect object
# Accusative: object of a transitive verb, direct object of verbs
# Vocative: JOE, what are you doing?

# see _noun_stems
# see _vowel_contract


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

_morph_do_long_alpha = False


####################
# letters
####################

_upper_vowels = "ΑΕΙΟΥΗΩ"
_upper_vowel_set = set("ΑΕΙΟΥΗΩ")
_upper_consonants = "ΒΓΔΖΘΚΛΜΝΞΠΡΣΤΦΧΨ"

_upper_morph_and_vowels = (
    ("/ ",  "ΆΈΊΌΎΉΏ"),
    ("\\ ", "ᾺῈῚῸῪῊῺ"),
    (None, None),
    (" s",  "ἈἘἸὈ ἨὨ"),
    ("/s",  "ἌἜἼὌ ἬὬ"),
    ("\\s", "ἊἚἺὊ ἪὪ"),
    ("~s",  "Ἆ Ἶ  ἮὮ"),
    (" r",  "ἉἙἹὉὙἩὩ"),
    ("/r",  "ἍἝἽὍὝἭὭ"),
    ("\\r", "ἋἛἻὋὛἫὫ"),
    ("~r",  "Ἇ Ἷ ὟἯὯ"),
    (" i",  "ᾼ    ῌῼ"),
    (None, None),
    (None, None),
    (None, None),
    (" is", "ᾈ    ᾘᾨ"),
    (" ir", "ᾉ      "),
    (" :",  "  Ϊ Ϋ  "),
    (None, None),
    (" S",  "Ᾰ Ῐ Ῠ  "),
    (" L",  "Ᾱ Ῑ Ῡ  "),
)

_vowels = "αειουηω"
_vowel_set = set("αειουηω")
_consonants = "βγδζθκλμνξπρστφχψ"

_morph_and_vowels = (
    ("/ ",  "άέίόύήώ"),
    ("\\ ", "ὰὲὶὸὺὴὼ"),
    ("~ ",  "ᾶ ῖ ῦῆῶ"),
    (" s",  "ἀἐἰὀὐἠὠ"),
    ("/s",  "ἄἔἴὄὔἤὤ"),
    ("\\s", "ἂἒἲὂὒἢὢ"),
    ("~s",  "ἆ ἶ ὖἦὦ"),
    (" r",  "ἁἑἱὁὑἡὡ"),
    ("/r",  "ἅἕἵὅὕἥὥ"),
    ("\\r", "ἃἓἳὃὓἣὣ"),
    ("~r",  "ἇ ἷ ὗἧὧ"),
    (" i",  "ᾳ    ῃῳ"),
    ("/i",  "ᾴ    ῄῴ"),
    ("\\i", "ᾲ    ῂῲ"),
    ("~i",  "ᾷ    ῇῷ"),
    (" is", "ᾀ    ᾐᾠ"),
    (" ir", "ᾁ    ῇῷ"),
    (" :",  "  ϊ ϋ  "),
    ("/:",  "  ΐ ΰ  "),
    (" S",  "ᾰ ῐ ῠ  "),
    (" L",  "ᾱ ῑ ῡ  "),
#    ("L/", "ᾱ́"),
)

_upper_to_lower = dict(zip(_upper_vowels, _vowels))
_upper_to_lower.update(zip(_upper_consonants, _consonants))
_upper_to_lower.update(
    ((u2,l2)
        for z in (
            zip(u1[1], l1[1])
            for u1, l1 in zip(_upper_morph_and_vowels, _morph_and_vowels)
            if u1[0])
        for u2, l2 in z
        if u2 != " " and l2 != " "))

_all_greek_letter_set = set(
    _vowels +
    _consonants + "ς" +
    "".join((
        vowels.replace(" ", "")
        for morph ,vowels in _morph_and_vowels)) +
    "".join(_upper_to_lower.keys()))


_vowel_and_morphed_vowels = (
    ("α", "άὰᾶἀἄἂἆἁἅἃἇᾳᾴᾲᾷᾀᾁᾰᾱ"),
    ("ε", "έὲἐἔἒἑἕἓ"),
    ("ι", "ίὶῖἰἴἲἶἱἵἳἷϊΐῐῑ"),
    ("ο", "όὸὀὄὂὁὅὃ"),
    ("υ", "ύὺῦὐὔὒὖὑὕὓὗϋΰῠῡ"),
    ("η", "ήὴῆἠἤἢἦἡἥἣἧῃῄῂῇᾐῇ"),
    ("ω", "ώὼῶὠὤὢὦὡὥὣὧῳῴῲῷᾠῷ"),
)

_vowels_to_base = dict(
    ((morphed_vowel, vowel)
        for morphed_vowels in (pair[1] for pair in _morph_and_vowels)
        for vowel, morphed_vowel in zip(_vowels, morphed_vowels)
        if morphed_vowel != " "))
_vowels_to_base.update(
    ((morphed_vowel, vowel)
        for morphed_vowels in (pair[1] for pair in _upper_morph_and_vowels if pair[0])
        for vowel, morphed_vowel in zip(_upper_vowels, morphed_vowels)
        if morphed_vowel != " "))

_morph_to_base_to_vowel = dict((
    (morph, dict([
        (_vowels_to_base.get(vowel), vowel)
        for vowel in vowels
        if vowel != " "]))
    for morph, vowels in _morph_and_vowels))

_vowel_to_morph = dict((
    (vowel, morph)
    for morph, vowels in _morph_and_vowels
    for vowel in vowels
    if vowel != " "))

def add_morph(letter, morph):
    base_letter = _vowels_to_base.get(letter, letter)
    if not base_letter in _vowel_set:
        return letter # not a vowel

    morph2 = _vowel_to_morph.get(letter, "  ")
    if len(morph) == 2:
        morphed_vowel = None
        morph_to_vowel = _morph_to_base_to_vowel.get(morph, None)
        if morph_to_vowel:
            morphed_vowel = morph_to_vowel.get(base_letter, None)
        if not morphed_vowel:
            morph_to_vowel = _morph_to_base_to_vowel.get(morph[0]+morph2[1], None)
            if morph_to_vowel:
                morphed_vowel = morph_to_vowel.get(base_letter, None)
        if not morphed_vowel:
            morph_to_vowel = _morph_to_base_to_vowel.get(morph2[0]+morph[1], None)
            if morph_to_vowel:
                morphed_vowel = morph_to_vowel.get(base_letter, None)
        if morphed_vowel:
            return morphed_vowel
        morph = morph[0]
    if len(morph2) == 3:
        return letter # what to do in this case is unclear
    if morph in '/\\~':
        morph3 = morph + morph2[1]
        if not morph3 in _morph_to_base_to_vowel:
            morph3 = morph + " "
    else:
        morph3 = morph2[0] + morph
        if not morph3 in _morph_to_base_to_vowel:
            morph3 = " " + morph

    morph_to_vowel = _morph_to_base_to_vowel.get(morph3, None)
    if morph_to_vowel:
        morphed_vowel = morph_to_vowel.get(base_letter, None)
        if morphed_vowel:
            return morphed_vowel
    return letter

def get_morph(letter):
    return _vowel_to_morph.get(letter, "  ")

def cp_morph(letter, morphed_letter):
    return add_morph(letter, get_morph(morphed_letter))

def translate_morph(word, i, f, t):
    let = word[i]
    morph = get_morph(let)
    j = f.find(morph[0])
    if j != -1:
        return word[:i] + add_morph(let, t[j]) + word[i+1:]

def base_let(let):
    """remove any morphs"""
    return _vowels_to_base.get(let, let)

def base_word(word):
    return "".join((
        base_let(let)
        for let in word))

def all_greek_letters(word):
    for let in word:
        if let in _all_greek_letter_set:
            continue
        return False
    return True

def any_greek_letters(word):
    for let in word:
        if not let in _all_greek_letter_set:
            continue
        return True
    return False

def _strip_let(let):
    let = _upper_to_lower.get(let, let)
    return let

def greek_strip(word):
    i2 = len(word)-1
    while i2 >= 0 and not word[i2] in _all_greek_letter_set:
        i2 -= 1
    if i2 == -1:
        return ""
    i1 = 0
    while i1 < i2 and not word[i1] in _all_greek_letter_set:
        i1 += 1
    return "".join((
        _strip_let(let)
        for let in word[i1:i2+1]))


####################
# syllables
####################

# note: accents go on the last character of the diphthong
# [αεου][ιυ]
_diphthongs = set((
    "αι",
    "ει",
    "οι",
    "υι",

    "αυ",
    "ευ",
    "ου",
    ))

# TODO: incomplete, consonant clusters not understood
_consonant_cluster = set((
    "χ",
    "φ",
    "θ",

    "χθ",
    "φθ",
    ))

def split_last_syllable(word):
    """Feeble attempt to get the root of this noun"""
    b_word = base_word(word)

    # find last vowel in last syllable
    i = len(word)-1
    while i >= 0 and not b_word[i] in _vowel_set:
        i -= 1

    if i >= 0:

        # find first vowel in last syllable
        j = i
        while j >= 0 and b_word[j-1] in _vowel_set:
            j -= 1

#        if j-1+1 >= 3 and word[j:j+2] in _diphthongs:
#            j += 2
        return (word[:j], word[j:])
    return (None, None)

def syllables(word):
    syls = []
    b_word = base_word(word)
    index1 = 0
    index2 = 0
    word_len = len(word)
    letter = None
    pl = None
    vbi2 = False
    while index2 < word_len:
        pl = letter
        letter = b_word[index2]
        if letter in _vowel_set:
            consonant_count = index2 - index1
            # vowels and diphthongs end a syllable,
            #   because each syllable can have either one vowel or a diphthong, diphthong wins
            # choose the vowel or diphthong
            if b_word[index2:index2+2] in _diphthongs:
                index2 += 2
            else:
                index2 += 1

            # if there are more than one consonant, and they are not a cluster, split them
            # unless the split would join to a vowel by itself
            if syls and consonant_count >= 2 and not b_word[index1] in _consonant_cluster:
                syls[-1] += word[index1]
                syls.append(word[index1+1:index2])
            else:
                syls.append(word[index1:index2])
            index1 = index2
        elif letter == pl:
            if syls and index2-index1 == 1:
                syls[-1] += word[index1]
                index1 += 1
            else:
                syls.append(word[index1:index2])
            index1 = index2
            index2 += 1
        else:
            index2 += 1
    if index1 < len(b_word):
        if b_word[index1] in _consonant_cluster:
            syls.append(word[index1:])
        elif syls:
            syls[-1] = syls[-1] + word[index1:]
        else:
            syls.append(word[index1:])
    return syls


####################
# nouns
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
                'G': ".ς",
                'D': "i",
            },
            'P': {
                'N': "αι",
                'V': "αι",
                'A': "ᾱς",
                'G': "ων",
                'D': "αις",
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
                'N': ".ς",
                'V': ".",
                'A': ".ν",
                'G': "ου",
                'D': "i",
            },
            'P': {
                'N': "αι",
                'V': "αι",
                'A': "ᾱς",
                'G': "ων",
                'D': "αις",
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
                'N': ".ς",
                'G': ".υ",
                'D': "ῳ",
                'A': ".ν",
                'V': "ε",
            },
            'P': {
                'N': ".ι",
                'G': "ων",
                'D': ".ις",
                'A': ".υς",
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
                'N': ".ς", # no change
                'G': ".υ",
                'D': "ῳ",
                'A': ".ν",
                'V': "ε",
            },
            'P': {
                'N': ".ι",
                'G': "ων",
                'D': ".ις",
                'A': ".υς",
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
                'D': ".ις",
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
    # ending γ and σ merge into a ξ in the nominative singular and dative plural.
    '3': {
        '-': {
            'S': {
                'N': "ς",               # ξς$ -> ξ
                'G': "ος",              # ξv -> γv
                'D': "ι",               # ξv -> γv
                'A': "α",   # or ν      # ξv -> γv
                'V': "",    # or ς
            },
            'D': {
                'N': "ε",               # ξv -> γv
                'G': "σιν",             # ξv -> γv
                'D': "σιν",
                'A': "ε",               # ξv -> γv
                'V': "ε",               # ξv -> γv
            },
            'P': {
                'N': "ες",              # ξv -> γv
                'G': "ων",              # ξv -> γv
                'D': "σι",              # ξv -> γv
                'A': "ας",              # ξv -> γv
                'V': "ες",              # ξv -> γv
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
}

_labial = "πβφψ"
_velar =  "κγχξ"
_dental = "τδθ"
_labial_velar = _labial + _velar 

def _noun_inflect(word, decl, gen, num, cas, do_dbg=True):
    """
    word - root word, no stem
    """
    end = _noun_stems[decl][gen][num][cas]

    _dbg = None
    if do_dbg: _dbg = [(word + "-" + end, "start")]

    b_word = base_word(word)
    # replace α with η if not preceeded by ειρ
    # only for first declension, (genative|dative)-singluar
#    if decl == '1' and num == 'S' and cas in ['G', 'D'] and b_word[-1] == 'α' and b_word[-2] not in ['ε', 'ι', 'ρ']:
#        word = word[:-1] + cp_morph('η', word[-1])
#        b_word = b_word[:-1] + 'η'
#        if do_dbg: _dbg.append((word + "-" + end, "α->η"))

    if decl == '3':
        last_let = b_word[-1]
        if last_let in _labial:
            category = "L"
        elif last_let in _velar:
            category = "V"
        elif last_let in _dental:
            category = "D"
        else:
            category = "?"

        if category == "L":
            if (
                    b_word[-1] == "ξ" and
                    end[0] in "γς" and
                    ((cas == "N" and gen == "S") or (cas == "D" and gen == "P"))):
                word = word[:-1] + end
            else:
                word = word + end
        else:
            word = word + end
        # TODO: show category
        if do_dbg: _dbg.append((word, "combine-3"))
    else:
        last_let = b_word[-1]

        # swap η with α for plural (genative|dative), sometimes singular
        if gen == "F" and cas in "GD":
            if last_let in 'αη':
                if last_let == 'α':
                    new_last_let = 'η'
                else:
                    new_last_let = 'α'
                if num == "P" or (num == "S" and word in ["θάλασσα", "δόξα", "γέεννα"]):
                    word = word[:-1] + cp_morph(new_last_let, word[-1])
                    b_word = b_word[:-1] + new_last_let
                    if do_dbg: _dbg.append((word + "-" + end, "%s->%s"%(last_let, new_last_let)))

                # this should only be done sometimes
                if num == "S":
                    if do_dbg: _dbg.append((word + "-" + end, "skip %s->%s"%(last_let, new_last_let)))

        # remove trailing sigma before applying the ending
        if last_let == 'ς':
            word = word[:-1]

        # apply the ending
        if end[0] == ".":
            word = word + end[1:]
            if do_dbg: _dbg.append((word, "combine_keep_last"))
        elif end[0] == "i":
            end_let = word[-1]
            if base_let(end_let) in "ηαο":
                word = word[:-1] + add_morph(word[-1], "i") + end[1:]
                if do_dbg: _dbg.append((word, "combine_iota"))
            else:
                word = word + end[1:]
                if do_dbg: _dbg.append((word, "combine_iota_oops"))
        else:
            word = word[:-1] + end
            if do_dbg: _dbg.append((word, "combine_rm_last"))

    b_word = base_word(word)

    if b_word[-2:] == "νς":
        word = word[:-1]
        b_word = b_word[:-1]
        if do_dbg: _dbg.append((word, "νς->ν"))

    i_last_v = len(word)-1
    # find last vowel
    while i_last_v >= 0 and not b_word[i_last_v] in _vowel_set:
        i_last_v -= 1
    if i_last_v >= 0:
        # vowel contraction
        # affects 2 or 3 vowels together
        # done before moving morphs
        if i_last_v > 0 and b_word[i_last_v-1] in _vowel_set:

            # try 3 letters ending at last vowel
            # (if i_last_v > 3) for θεοῦ
            if i_last_v > 3:
                find = b_word[i_last_v-2:i_last_v+1]
                replace = _vowel_contract.get(find, None)
                if replace:

                    # if this would create a double-vowel, don't
                    ii = 0
#                    if replace[-1] == word[i_last_v+1:i_last_v+2]:
#                        ii = 1

                    replace = replace[:-1] + cp_morph(cp_morph(cp_morph(replace[-1], word[i_last_v-2]), word[i_last_v-1]), word[i_last_v])
                    word = word[:i_last_v-2] + replace + word[i_last_v+1+ii:]
                    b_word = b_word[:i_last_v-2] + replace + b_word[i_last_v+1+ii:]

                    i_last_v -= 3 - len(replace) + ii
                    if do_dbg: _dbg.append((word, "contract-3", find, replace))

            # try 2 letters ending at last vowel
            # (if i_last_v > 2) for θεὸς and λαῷ
            if i_last_v > 2 and b_word[i_last_v-1] in _vowel_set:
                find = b_word[i_last_v-1:i_last_v+1]
                replace = _vowel_contract.get(find, None)
                if not replace and b_word[i_last_v-1] == b_word[i_last_v]:
                    replace = cp_morph(word[i_last_v-1], word[i_last_v])
                if replace:
                    # if this would create a double-vowel, don't
                    ii = 0
                    if replace[-1] == word[i_last_v+1:i_last_v+2]:
                        ii = 1

                    word = word[:i_last_v-1] + replace + word[i_last_v+1+ii:]
                    b_word = b_word[:i_last_v-1] + base_word(replace) + b_word[i_last_v+1+ii:]
                    i_last_v -= 2 - len(replace) + ii
                    if do_dbg: _dbg.append((word, "contract-2", find, replace))

        # moving morphs to the last vowel in diphthongs
        if i_last_v > 0 and b_word[i_last_v-1:i_last_v+1] in _diphthongs:
            # move accent from beginning to end of diphthong
            # affects [αεου][ιυ]
            let1 = word[i_last_v-1]
            let1_morph = get_morph(let1)
            let1 = base_let(let1)

            let2 = add_morph(word[i_last_v], let1_morph)
            if let2 != word[i_last_v]:
                word = word[:i_last_v-1] + let1 + let2 + word[i_last_v+1:]
                if do_dbg: _dbg.append((word, "mv"))

        # accent translation
        if cas == 'G' and num == 'S':
            word2 = translate_morph(word, i_last_v, "\\", "~")
            if word2:
                word = word2
                if do_dbg: _dbg.append((word, "\\ -> ~"))
        if cas == 'D' and num == 'P':
            word2 = translate_morph(word, i_last_v, "/", "~")
            if word2:
                word = word2
                if do_dbg: _dbg.append((word, "/ -> ~"))
        if cas in 'N' and num == 'P':
            word2 = translate_morph(word, i_last_v, "/", "\\")
            if word2:
                word = word2
                if do_dbg: _dbg.append((word, "/ -> \\"))
        if cas in 'A' and num == 'P':
            word2 = translate_morph(word, i_last_v, "\\", "/")
            if word2:
                word = word2
                if do_dbg: _dbg.append((word, "\\ -> /"))

    # for dative: place iota subscript on vowel followed by iota
    # only for dative-singular
    # affects [ηαο]ι
    if cas == 'D' and num == 'S':
        if b_word[-1] == 'η':
            # ἐργάτῃ
            # τρίτῇ->τρίτῃ (.F.)
            # -----
            # κριτῃ->κριτῇ (M.N)
            if b_word[-2] in ['φ', 'θ'] or (b_word[-2] == 'τ' and gen != 'F'):
                if word[-1] != 'ῇ':
                    word = word[:-1] + 'ῇ'
                    if do_dbg: _dbg.append((word, "DS(η)->iota.1"))
            else:
                if word[-1] != 'ῃ':
                    word = word[:-1] + 'ῃ'
                    if do_dbg: _dbg.append((word, "DS(η)->iota.2"))

    i = len(word)-1
    # find last vowel
    while i >= 0 and not b_word[i] in _vowel_set:
        i -= 1
    if i >= 0:
        pass
        # The first-declension genitive-plural always takes a circumflex on the last syllable
#        if decl == '1' and cas == 'G' and num == 'P':
#            word = word[:i] + add_morph(word[i], "~") + word[i+1:]
#            if do_dbg: _dbg.append((word, "1GP->~"))

# bad:[('ἅγιο-ς', 'start'), ('ἅγῶν', 'end: ιος -> ων')]
# bad:[('ἥλιο-ς', 'start'), ('ἥλῶν', 'end: ιος -> ων')]
# bad:[('δεξιὸ-ς', 'start'), ('δεξῶν', 'end: ιος -> ων')]
# bad:[('κύριο-ς', 'start'), ('κύρῶν', 'end: ιος -> ων')]
# bad:[('νυμφίο-ς', 'start'), ('νυμφῶν', 'end: ιος -> ων')]
# bad:[('Ναζωραῖο-ς', 'start'), ('Ναζωραῶν', 'end: ιος -> ων')]
# 
# good:[('αἰτίο-ς', 'start'), ('αἰτῶν', 'end: ιος -> ων')]
# good:[('λαλιό-ς', 'start'), ('λαλῶν', 'end: ιος -> ων')]
# good:[('μαρτυρίο-ς', 'start'), ('μαρτυρῶν', 'end: ιος -> ων')]
# 
#    if cas == 'N' and num == 'S':
#        if b_word[-3:] == 'ιος':
#            word = word[:-3] + 'ῶν'
#            b_word = b_word[:-3] + 'ων'
#            if do_dbg: _dbg.append((word, "end: ιος -> ων"))

    # alphas at the end of the word have "long" mark
    # unless it is morphed already
    if _morph_do_long_alpha:
        if num == 'S' or cas == 'A':
            if word[-1] == 'α':
                word = word[:-1] + 'ᾱ'
                if do_dbg: _dbg.append((word, "long-1"))
            elif word[-2] == 'α':
                word = word[:-2] + 'ᾱ' + word[-1]
                if do_dbg: _dbg.append((word, "long-2"))

    return (word, _dbg)

# D1 M ends in ης ας
# D1 F ends in η α
#   1: [MF]:[SPD]:[NAGDV] -> [.iα]α*
# D2 [MF]: ending is ος
# D2 [N]: ending is ον
#   2: [MFN]:[SPD]:[NAGDV] -> [.iα]α*
# D3 consonants, note: ending γ and σ merge into a ξ in the nominative singular and dative plural.
#   3: [-]:[SPD]:[NAGDV] -> [.iα]α*
def decl_gen(word, gen):
    """
    word - root word, no stem
    """
    b_word = base_word(word)
    last_let = b_word[-1]
    last_2_let = b_word[-2:]

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
        decl = "2"
    elif last_2_let == "ον":
        decl = "2"
        gen = "N"
    else:
        decl = "3"
        gen = "-" # gender doesn't matter

    return (decl, gen)


def noun_inflect(word, gen, num, cas):
    """
    word - root word, no stem
    """
    decl, gen = decl_gen(word, gen)
    return _noun_inflect(word, decl, gen, num, decl)

def noun_inflect_all(word, gen):
    """
    word - root word, no stem
    returns a list of 1 or 2 answers, each answer containing (decl, gen, words)
        decl in ["1", "2", "3"]
        gen in ["M", "F", "N"]
        words[num][case] contains (word, _dbg list)
    """
    decl, gen2 = decl_gen(word, gen)

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
        for num in ('S', 'P', 'D'):
            num_words = words[num] = {}
            for cas in ('N', 'G', 'D', 'A'):
                if word:
                    num_words[cas] = _noun_inflect(word, decl, gen3, num, cas)
                else:
                    num_words[cas] = ("", [])
    return answers

def print_noun_1(word, gen):
    for decl, gen, data in noun_inflect_all(word, gen):
        max_len = max((
            len(word_dbg[0])
            for case_to_word_dbg in data.values()
            for word_dbg in case_to_word_dbg.values()))
        print("-------------------- decl=%s gen=%s "%(decl, gen))
        print("{5:6s} {1:{0}s} {2:{0}s} {3:{0}s} {4:{0}s}".format(
            max_len+2,
            "nom", "gen", "dat", "acc",
            word,
            ))
        for num in ('S', 'P', 'D'):
            print("{5}:    {1:{0}s} {2:{0}s} {3:{0}s} {4:{0}s}".format(
                max_len+2,
                data[num]["N"][1],
                data[num]["G"][1],
                data[num]["D"][1],
                data[num]["A"][1],
                num,
                ))

# analyze text

word_map = {}

def eat_line(line):
    words = line.split(' ')
    for word in words:
        word_map[word] = word_map.get(word, 0)+1

def report():
    w = [(cnt, wd) for wd, cnt in word_map.items()]
    w.sort()
    w.reverse()
    for x in w:
        print("%s"%str(x))

def scan_P75():
    fh = open("P75.v2.copy")

    for line in fh:
        line = line.rstrip()
        i = line.find(": ")
        line = line[i+2:]
        eat_line(line)

    report()


def test_noun_inflect(name, actual, expected):
    for act, exp in zip(actual, expected):
        base_act = base_word(act[1])
        base_exp = base_word(exp[1])
        if base_act != base_exp:
            print("ERROR %s %s (%s exp %s) (%s exp %s)\n  %s"%(
                name, act[0], act[1], exp[1], base_act, base_exp, act[2]))
        elif act[1] != exp[1]:
            print("WARN %s %s (%s exp %s)\n  %s"%(
                name, act[0], act[1], exp[1], repr(act[2])))

if __name__ == '__main__':
    while True:
        word = input("What's up? ")
        print_noun_1(word, '-')
#        print("-".join(syllables(word.rstrip())))

