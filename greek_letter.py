#!/usr/local/bin/python3

import itertools as it
import re

# sound type:  lpd   d p     l  d lp        (l)abial, (d)ental, (p)alatal
# aspiration:  und z a vlnn. vl.v aa.       (u)nvoiced, (a)spirated, (n)asal, (l)iquid, (z)eta
# consonants: -βγδ-ζ-θ-κλμνξ-πρστ-φχψ-
# vowels:     α---ε-η-ι-----ο----υ---ω
# short/long: .   s l .     s    .   l      (s)hort, (l)ong (.)=both

####################
# letters, vowels
####################
# vowels: α[εη]ι[οω]υ
#     short sound: ᾰεῐοῠ
#     long sound : ᾱηῑωῡ

_upper_vowels = "ΑΕΙΟΥΗΩ"
_lower_vowels = "αειουηω"

_diphthongs = set((
    "αι",   # h[i]
    "ᾱι",   # ?, written ᾳ
    "ει",   # f[a]te, [η]
    "ηι",   # ?, written ῃ
    "οι",   # t[oy]
    "ωι",   # ?, written ῳ
    "υι",   # ?

    "αυ",   # ?
    "ευ",   # n[ew]
    "ου",   # n[ew]
    ))

####################
# letters, consonants
####################

_upper_consonants = "ΒΓΔΖΘΚΛΜΝΞΠΡΣΤΦΧΨ"
_lower_consonants = "βγδζθκλμνξπρστφχψ"

# consonants by sound type
_labials =  "πβφ"   # and ".σ" -> "ψ" # which are formed with the lips
_dentals =  "τδθ"   # and ".σ" -> "σ" # which are formed with the tongue and teeth
_palatals = "κγχ"   # and ".σ" -> "ξ" # which are formed with the tongue and palate

# consonants by sound type
_voiced = "πτκ"     # STOP consonants: the airflow or breathing passage must be momentarily closed, when aspirated with the "h" sound, becomes _aspirated
_unvoiced = "βδγ"   # VOICED STOPS: pronouncing "πτκ" while vibrating your vocal cords
_aspirated = "φθχ"  # a breathing or “h” sound to the consonants
_nasal = ["μ", "ν", "γγ"]
_liquid = "λρ"
_zeta = "ζ"
___missing_but_above = "ψσξ"

_aspirated_to_unaspirated = dict(((a, b) for a, b in zip(_aspirated, _voiced)))


####################
# morphs: accents, breathing marks, sort/long vowels, ...
####################

# breathing marks:
#   breathing marks are only placed on the first vowel or diphthong (on the second letter) in a word, or ρ if it is the first letter of a word.
#       a smooth breathing mark means inticates there is no aspiration "h" sound to start the word.
#       a rough breathing mark means inticates there is an aspiration "h" sound to start the word.
#   if ρ is the first letter of a word it is always aspirated.
#   when letters in _voiced are aspirated, they become _aspirated
#
# accents are applied only to any of the last three syllables of a word.
#   names of the last three syllables:
#       ultima: last
#       penult: 2nd last
#       antepenult: 3rd last
#
# accents:
#   long vowels mean to sing them for two beats
#       ᾱ -> αα     ῑ -> ιι     ῡ -> υυ     η -> εε     ω -> οο
#   accute (/) means pitch up when singing
#       αά -> ά     ιί -> ί     υύ -> ύῦ    εέ -> ή     οό -> ώ
#   grave (\) means no pitch up, and is only applied to ultima when another word follows the word being accented.
#       because a pitch up was unpronounced if another word followed in the sentence.
#   circumflex (~) means up then down, so that (/\) on "two letters", long vowels or diphthongs
#       άὰ -> ᾶ     ίὶ -> ῖ     ύὺ -> ῦ     έὲ -> ῆ     όὸ -> ῶ
#

_upper_morph_and_vowels = (
    # accents (acute, grave, circumflex)
    (r"/  ",  "ΆΈΊΌΎΉΏ"), # ΆΈΊΌΎΉΏ
    (r"\  ",  "ᾺῈῚῸῪῊῺ"),
    (None, ""),

    # breathing mark, smooth
    (r" s ",  "ἈἘἸὈ ἨὨ"),
    (r"/s ",  "ἌἜἼὌ ἬὬ"),
    (r"\s ",  "ἊἚἺὊ ἪὪ"),
    (r"~s ",  "Ἆ Ἶ  ἮὮ"),

    # breathing mark, rough
    (r" r ",  "ἉἙἹὉὙἩὩ"),
    (r"/r ",  "ἍἝἽὍὝἭὭ"),
    (r"\r ",  "ἋἛἻὋὛἫὫ"),
    (r"~r ",  "Ἇ Ἷ ὟἯὯ"),

    # iota subscript
    (r"  i",  "ᾼ    ῌῼ"),
    (None, ""),
    (None, ""),
    (None, ""),

    # iota subscript with breathing marks
    (r" si", "ᾈ    ᾘᾨ"),
    (r" ri", "ᾉ    ᾙᾩ"),
    (r"/si", "ᾌ    ᾜᾬ"),
    (r"/ri", "ᾍ    ᾝᾭ"),
    (r"\si", "ᾊ    ᾚᾪ"),
    (r"\ri", "ᾋ    ᾛᾫ"),
    (r"~si", "ᾎ    ᾞᾮ"),
    (r"~ri", "ᾏ    ᾟᾯ"),

    # short and long vowel
    (r"  S",  "Ᾰ Ῐ Ῠ  "),
    (r"  L",  "Ᾱ Ῑ Ῡ  "),

    # ???
    (r" : ",  "  Ϊ Ϋ  "),
    (None, ""),
    (None, ""),
    (None, ""),
)

_lower_morph_and_vowels = (
    # accents (acute, grave, circumflex)
    (r"/  ",  "άέίόύήώ"), # άέίόύήώ
    (r"\  ",  "ὰὲὶὸὺὴὼ"),
    (r"~  ",  "ᾶ ῖ ῦῆῶ"),

    # breathing mark, smooth
    (r" s ",  "ἀἐἰὀὐἠὠ"),
    (r"/s ",  "ἄἔἴὄὔἤὤ"),
    (r"\s ",  "ἂἒἲὂὒἢὢ"),
    (r"~s ",  "ἆ ἶ ὖἦὦ"),

    # breathing mark, rough
    (r" r ",  "ἁἑἱὁὑἡὡ"),
    (r"/r ",  "ἅἕἵὅὕἥὥ"),
    (r"\r ",  "ἃἓἳὃὓἣὣ"),
    (r"~r ",  "ἇ ἷ ὗἧὧ"),

    # iota subscript
    (r"  i",  "ᾳ    ῃῳ"),
    (r"/ i",  "ᾴ    ῄῴ"),
    (r"\ i",  "ᾲ    ῂῲ"),
    (r"~ i",  "ᾷ    ῇῷ"),

    # iota subscript with breathing marks
    (r" si", "ᾀ    ᾐᾠ"),
    (r" ri", "ᾁ    ᾑᾡ"),
    (r"/si", "ᾄ    ᾔᾤ"),
    (r"/ri", "ᾅ    ᾕᾥ"),
    (r"\si", "ᾂ    ᾒᾢ"),
    (r"\ri", "ᾃ    ᾓᾣ"),
    (r"~si", "ᾆ    ᾖᾦ"),
    (r"~ri", "ᾇ    ᾗᾧ"),

    # short and long vowel
    (r"  S",  "ᾰ ῐ ῠ  "),
    (r"  L",  "ᾱ ῑ ῡ  "),
#   (r"/ L",  "ᾱ́      "),

    # ???
    (r" : ",  "  ϊ ϋ  "),
    (r"/: ",  "  ΐ ΰ  "), # ΐ ΰ
    (r"\: ",  "  ῒ ῢ  "),
    (r"~: ",  "  ῗ ῧ  "),
)

_lower_vowel_set = set(_lower_vowels)
_lower_vowel_and_rho_set = set(_lower_vowels + "ρ")

_upper_to_lower = dict(zip(_upper_vowels, _lower_vowels))
_upper_to_lower.update(zip(_upper_consonants, _lower_consonants))
_upper_to_lower.update(
    ((u2,l2)
        for z in (
            zip(umav[1], lmav[1])
            for umav, lmav in zip(_upper_morph_and_vowels, _lower_morph_and_vowels)
            if umav[0])
        for u2, l2 in z
        if u2 != " " and l2 != " "))


_all_greek_letter_set = set(_lower_vowels +
    _lower_consonants + "ς" +
    "".join((
        vowels.replace(" ", "")
        for morph, vowels in _lower_morph_and_vowels)) +
    "".join(_upper_to_lower.keys()))

_all_vowel_set = set(
    _lower_vowels +
    "".join((
        vowels.replace(" ", "")
        for morph, vowels in _lower_morph_and_vowels)) +
    _upper_vowels +
    "".join((
        vowels.replace(" ", "")
        for morph, vowels in _upper_morph_and_vowels)))

_vowels_to_clean = dict(
    ((morphed_vowel, vowel)
        for morphed_vowels in (pair[1] for pair in _lower_morph_and_vowels)
        for vowel, morphed_vowel in zip(_lower_vowels, morphed_vowels)
        if morphed_vowel != " "))
_vowels_to_clean.update(
    ((morphed_vowel, vowel)
        for morphed_vowels in (pair[1] for pair in _upper_morph_and_vowels if pair[0])
        for vowel, morphed_vowel in zip(_upper_vowels, morphed_vowels)
        if morphed_vowel != " "))

_morph_to_clean_to_vowel = dict((
    (morph, dict([
        (_vowels_to_clean.get(vowel), vowel)
        for vowel in vowels
        if vowel != " "]))
    for morph, vowels in (
        (lmav[0], lmav[1] + umav[1])
        for lmav, umav in zip(_lower_morph_and_vowels, _upper_morph_and_vowels))
    if vowels))

_vowel_to_morph = dict((
    (vowel, morph)
    for morph, vowels in _lower_morph_and_vowels + _upper_morph_and_vowels
    if vowels
    for vowel in vowels
    if vowel != " "))


def get_morph(letter):
    return _vowel_to_morph.get(letter, "  ")

def add_morph(letter, morph):
    clean_letter = _vowels_to_clean.get(letter, letter)
    if not clean_letter in _lower_vowel_set:
        return letter # not a vowel

    orig_morph = _vowel_to_morph.get(letter, "   ")
    if len(morph) == 3:
        morphed_vowel = None
        morph_to_vowel = _morph_to_clean_to_vowel.get(morph, None)
        if morph_to_vowel:
            morphed_vowel = morph_to_vowel.get(clean_letter, None)
        if not morphed_vowel:
            morph_to_vowel = _morph_to_clean_to_vowel.get(morph[:2]+orig_morph[2], None)
            if morph_to_vowel:
                morphed_vowel = morph_to_vowel.get(clean_letter, None)
        if not morphed_vowel:
            morph_to_vowel = _morph_to_clean_to_vowel.get(morph[0]+orig_morph[1:], None)
            if morph_to_vowel:
                morphed_vowel = morph_to_vowel.get(clean_letter, None)
        if morphed_vowel:
            return morphed_vowel
        morph = morph[0]
    if morph in '/\\~':
        new_morph = morph + orig_morph[1:]
        if not new_morph in _morph_to_clean_to_vowel:
            new_morph = morph + "  "
    elif morph in 'sr':
        new_morph = orig_morph[0] + morph + orig_morph[2]
        if not new_morph in _morph_to_clean_to_vowel:
            new_morph = " " + morph + " "
    else:
        new_morph = orig_morph[:2] + morph
        if not new_morph in _morph_to_clean_to_vowel:
            new_morph = "  " + morph

    morph_to_vowel = _morph_to_clean_to_vowel.get(new_morph, None)
    if morph_to_vowel:
        morphed_vowel = morph_to_vowel.get(clean_letter, None)
        if morphed_vowel:
            return morphed_vowel
    return letter

def cp_morph(letter, morphed_letter):
    return add_morph(letter, get_morph(morphed_letter))

def translate_morph(word, i, f, t):
    letter = word[i]
    morph = get_morph(letter)
    j = f.find(morph[0])
    if j != -1:
        return word[:i] + add_morph(letter, t[j]) + word[i+1:]


def clean_let(letter, sigma=False, lower=False, keep_rough=True):
    """remove any morphs"""
    if keep_rough:
        add_rough = _vowel_to_morph.get(letter, "  ")[1] == 'r'
    else:
        add_rough = False
    letter = _vowels_to_clean.get(letter, letter)
    if lower:
        letter = lower_let(letter)
    if sigma and letter == 'ς':
        letter = 'σ'
    if add_rough:
        letter = add_morph(letter, "r")
    return letter

def clean_word(word, sigma=False, lower=False, keep_rough=True):
    return "".join((
        clean_let(letter, sigma, lower, keep_rough)
        for letter in word))

def all_greek_letter(word):
    for letter in word:
        if letter in _all_greek_letter_set:
            continue
        return False
    return True

def any_greek_letter(word):
    for letter in word:
        if not letter in _all_greek_letter_set:
            continue
        return True
    return False

def _strip_let(letter):
    letter = _upper_to_lower.get(letter, letter)
    return letter

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
        _strip_let(letter)
        for letter in word[i1:i2+1]))

def is_vowel(letter):
    return letter in _all_vowel_set

def lower_let(letter):
    return _upper_to_lower.get(letter, letter)

####################
# contractions
####################

# contracting the vowels (α, ε, ο) and accents:
#   resulting vowel or diphthong is long
#   examples:
#       ά + ὲ = ᾶ	έ + ὰ = ῆ	ό + ὰ = ῶ
#       ά + ὸ = ῶ	έ + ὸ = οῦ	ό + ὲ = οῦ
#       α + έ = ά	ε + ά = ή	ο + ά = ώ
#       α + ό = ώ	ε + ό = ού	ο + έ = ού

# url: https://ancientgreek.pressbooks.com/chapter/1/
# TODO: remove from greek_noun.py, when this is correct
_vowel_contract = {

    ## standard contractions

    'αα': 'α',
    'εα': 'η', # MISSING
    'οα': 'α', # CHANGED

    'αε': 'α',
    'εε': 'ει',
    'οε': 'ον',

    'αο': 'ω', # MISSING
    'εο': 'ον',
    'οο': 'ον', # CHANGED, but 2 different choices

    ## discovered contractions

    'ηε': 'η',
    'ηι': 'η',
    'εη': 'η',
    'ηη': 'η',

#    'οη': 'ω',
    'αη': 'α',

    'αω': 'ω',
    'εω': 'ω',
    'οω': 'ω',

    'αοι': 'ω',
    'εοι': 'οι',
    'ηοι': 'ω',
    'οοι': 'οι',

#    'αου': 'ω',
    'εου': 'οι',
    'οου': 'οι', # οου -> ονυ/ωυ
    'ουι': 'ου',

    'σου': 'σαι', # doesn't fit the code to implement the others well
}

# if word <ENDS> <WITH> key, replace key with value in word
_sigma_contract_ends = {
    'ορσ': 'ωρ',
    'ονσ': 'ων',
    'οδσ': 'ουσ',
    'ωνσι': 'ωσ',
    'ονσι': 'οσ',
    'οτσι': 'υσ',
    'οντσ': 'ων',
}

_sigma_contract_2 = dict(
    list(zip(_labials, it.repeat('ψ'))) +                                       # <L>σ -> ψ
    list(zip(_palatals, it.repeat('ξ'))) +                                      # <P>σ -> ξ
    list(zip((p + d for p in _palatals for d in _dentals), it.repeat('ξ'))) +   # <PD>σ -> ξ
    list(zip((l + d for l in _labials for d in _dentals), it.repeat('ψ'))) +    # <LD>σ -> ψ
    list(zip(_dentals, it.repeat(''))))                                         # <D>σ -> ""

# ν is a nasal
_sigma_contract_2["ν"] = "ν"                                               # νσ -> ν

# δτ are both dentals
_sigma_contract_2["δ"] = "σ"                                               # δσ -> σ
_sigma_contract_2["τ"] = "σ"                                               # τσ -> σ


# elision:
#   when a word ends in a vowel and the next word starts with a vowel
#       then the vowel at the end of the word is removed
# movable nu:
#   if a word ends in σι and the next word starts with a vowel, σι -> σιν

def vocal_modifications(word):
    """
    Modify a word as the Greeks did, so that it is spelled like it sounds.

    This includes verb contractions, and dealing with sigma.
    """

    _dbg = []

    # contractions
    for find_len in [3,2]:
        for i in range(len(word) - find_len + 1):
            find = word[i  :  i + find_len]
            replace = _vowel_contract.get(find, None)
            if replace:
                delta = word[i:i + find_len] + " -> " + replace
                word = word[:i] + replace + word[i + find_len  :  ]
                _dbg.append(("cont", word, delta))

    # sigma
    for find_len in [3,4]:
        replace = _sigma_contract_ends.get(word[-find_len:], None)
        if replace:
            delta = word[find_len:] + " -> " + replace
            word = word[:-find_len] + replace
            _dbg.append(("sigma1", word, delta))
    sigma_indexes = [m.start() for m in re.finditer("[σς]", word)]
    sigma_indexes.reverse()
    for i in sigma_indexes:
        for find_len in [1,2]:
            replace = _sigma_contract_2.get(word[i-find_len:i], None)
            if replace:
                delta = word[i-find_len:i+1] + " -> " + replace
                word = word[:i-find_len] + replace + word[i+1:]
                _dbg.append(("sigma2", word, delta))
        
    if word[-1] == 'σ':
        word = word[:-1] + 'ς'
    return word, _dbg

def accent_word(word, next_word):
    c_word = clean_word(word)
    return c_word

####################
# syllables
####################

# TODO: incomplete, consonant clusters not understood
_consonant_cluster = set((
    "χ",
    "φ",
    "θ",

    "χθ",
    "φθ",
    ))

def syllables(word):
    syls = []
    c_word = clean_word(word, True, True, False)
    index1 = 0
    index2 = 0
    word_len = len(word)
    letter = None
    prev_letter = None
    while index2 < word_len:
        prev_letter = letter
        letter = c_word[index2]
        if letter in _lower_vowel_and_rho_set:
            consonant_count = index2 - index1

            # vowels and diphthongs end a syllable,
            #   because each syllable can have either one vowel or a diphthong, diphthong wins
            # choose the vowel or diphthong
            if c_word[index2:index2+2] in _diphthongs:
                index2 += 2
            else:
                index2 += 1

            # if there are more than one consonant, and they are not a cluster, split them
            # unless the split would join to a vowel by itself
            if syls and consonant_count >= 2 and not c_word[index1] in _consonant_cluster:
                syls[-1] += word[index1]
                syls.append(word[index1+1:index2])
            else:
                syls.append(word[index1:index2])
            index1 = index2
        elif letter == prev_letter:
            if syls and index2-index1 == 1:
                syls[-1] += word[index1]
                index1 += 1
            else:
                syls.append(word[index1:index2])
            index1 = index2
            index2 += 1
        else:
            index2 += 1
    if index1 < len(c_word):
        if c_word[index1] in _consonant_cluster:
            syls.append(word[index1:])
        elif syls:
            syls[-1] = syls[-1] + word[index1:]
        else:
            syls.append(word[index1:])
    return syls

