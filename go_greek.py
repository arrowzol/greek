#!/usr/local/bin/python3

####################
# letters
####################

_upper_vowels = "ΑΕΙΟΥΗΩ"
_upper_consonants = "ΒΓΔΖΘΚΛΜΝΞΠΡΣΤΦΧΨ"

_upper_morph_and_vowels = (
    ("/ ",  "ΆΈΊΌΎΉΏ"),
    ("\\ ", "ᾺῈῚῸῪῊῺ"),
    (None, ""),
    (" s",  "ἈἘἸὈ ἨὨ"),
    ("/s",  "ἌἜἼὌ ἬὬ"),
    ("\\s", "ἊἚἺὊ ἪὪ"),
    ("~s",  "Ἆ Ἶ  ἮὮ"),
    (" r",  "ἉἙἹὉὙἩὩ"),
    ("/r",  "ἍἝἽὍὝἭὭ"),
    ("\\r", "ἋἛἻὋὛἫὫ"),
    ("~r",  "Ἇ Ἷ ὟἯὯ"),
    (" i",  "ᾼ    ῌῼ"),
    (None, ""),
    (None, ""),
    (None, ""),
    (" is", "ᾈ    ᾘᾨ"),
    (" ir", "ᾉ      "),
    (" :",  "  Ϊ Ϋ  "),
    (None, ""),
    (" S",  "Ᾰ Ῐ Ῠ  "),
    (" L",  "Ᾱ Ῑ Ῡ  "),
)

_lower_vowels = "αειουηω"
_lower_vowel_set = set(_lower_vowels)
_lower_consonants = "βγδζθκλμνξπρστφχψ"

_lower_morph_and_vowels = (
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

_all_greek_letter_set = set(
    _lower_vowels +
    _lower_consonants + "ς" +
    "".join((
        vowels.replace(" ", "")
        for morph, vowels in _lower_morph_and_vowels)) +
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
        for morphed_vowels in (pair[1] for pair in _lower_morph_and_vowels)
        for vowel, morphed_vowel in zip(_lower_vowels, morphed_vowels)
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
    base_letter = _vowels_to_base.get(letter, letter)
    if not base_letter in _lower_vowel_set:
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

def cp_morph(letter, morphed_letter):
    return add_morph(letter, get_morph(morphed_letter))

def translate_morph(word, i, f, t):
    let = word[i]
    morph = get_morph(let)
    j = f.find(morph[0])
    if j != -1:
        return word[:i] + add_morph(let, t[j]) + word[i+1:]


def base_let(let, sigma=False):
    """remove any morphs"""
    let = _vowels_to_base.get(let, let)
    if sigma and let == 'ς':
        let = 'σ'
    return let

def base_word(word, sigma=False):
    return "".join((
        base_let(let, sigma)
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
        if letter in _lower_vowel_set:
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

