#!/usr/local/bin/python3

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
# consonants: -βγδ-ζ-θ-κλμνξ-πρστ-φχψ-

_upper_consonants = "ΒΓΔΖΘΚΛΜΝΞΠΡΣΤΦΧΨ"
_lower_consonants = "βγδζθκλμνξπρστφχψ"

# vowels by sound type
_labials =  "πβφ"   # and ".σ" -> "ψ" # which are formed with the lips
_dentals =  "τδθ"   # and ".σ" -> "σ" # which are formed with the tongue and teeth
_palatals = "κγχ"   # and ".σ" -> "ξ" # which are formed with the tongue and palate

# consonants by sound type
_voiced = "πτκ"     # STOP consonants: the airflow or breathing passage must be momentarily closed
_unvoiced = "βδγ"   # VOICED STOPS: pronouncing "πτκ" while vibrating your vocal cords
_aspirated = "φθχ"  # a breathing or “h” sound to the consonants
_nasal = ["μ", "ν", "γγ"]
_liquid = "λρ"
_zeta = "ζ"

_aspirated_to_unaspirated = dict(((a, b) for a, b in zip(_aspirated, _voiced)))


####################
# morphs: accents, breathing marks, sort/long vowels, ...
####################

# breathing marks:
#   breathing marks are only placed on the first vowel or diphthong (on the second letter) in a word, or ρ if it is the first letter of a word.
#       a smooth breathing mark means inticates there is no aspiration "h" sound to start the word.
#       a rough breathing mark means inticates there is an aspiration "h" sound to start the word.
#   if ρ is the first letter of a word it is always aspirated.
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

    orig_morph = _vowel_to_morph.get(letter, "   ")
    if len(morph) == 3:
        morphed_vowel = None
        morph_to_vowel = _morph_to_base_to_vowel.get(morph, None)
        if morph_to_vowel:
            morphed_vowel = morph_to_vowel.get(base_letter, None)
        if not morphed_vowel:
            morph_to_vowel = _morph_to_base_to_vowel.get(morph[:2]+orig_morph[2], None)
            if morph_to_vowel:
                morphed_vowel = morph_to_vowel.get(base_letter, None)
        if not morphed_vowel:
            morph_to_vowel = _morph_to_base_to_vowel.get(morph[0]+orig_morph[1:], None)
            if morph_to_vowel:
                morphed_vowel = morph_to_vowel.get(base_letter, None)
        if morphed_vowel:
            return morphed_vowel
        morph = morph[0]
    if morph in '/\\~':
        new_morph = morph + orig_morph[1:]
        if not new_morph in _morph_to_base_to_vowel:
            new_morph = morph + "  "
    elif morph in 'sr':
        new_morph = orig_morph[0] + morph + orig_morph[2]
        if not new_morph in _morph_to_base_to_vowel:
            new_morph = " " + morph + " "
    else:
        new_morph = orig_morph[:2] + morph
        if not new_morph in _morph_to_base_to_vowel:
            new_morph = "  " + morph

    morph_to_vowel = _morph_to_base_to_vowel.get(new_morph, None)
    if morph_to_vowel:
        morphed_vowel = morph_to_vowel.get(base_letter, None)
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


def base_let(letter, sigma=False, lower=False, keep_rough=True):
    """remove any morphs"""
    if keep_rough:
        add_rough = _vowel_to_morph.get(letter, "  ")[1] == 'r'
    else:
        add_rough = False
    letter = _vowels_to_base.get(letter, letter)
    if lower:
        letter = lower_let(letter)
    if sigma and letter == 'ς':
        letter = 'σ'
    if add_rough:
        letter = add_morph(letter, "r")
    return letter

def base_word(word, sigma=False, lower=False, keep_rough=True):
    return "".join((
        base_let(letter, sigma, lower, keep_rough)
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
    'αα': 'ᾱ',
    'εα': 'η', # changed
    'οα': 'ω', # changed

    'αε': 'ᾱ',
    'εε': 'ει',
    'οε': 'ον',

    'αο': 'ω',
    'εο': 'ον',
    'οο': 'ον',
}

# elision:
#   when a word ends in a vowel and the next word starts with a vowel
#       then the vowel at the end of the word is removed
# movable nu:
#   if a word ends in σι and the next word starts with a vowel, σι -> σιν

def contract(word, elision=False):
    pass

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
        if letter in _lower_vowel_and_rho_set:
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

def dump_unicode_ranges():
        fh=open("lets2", "bw")
        # cc 80 : add \
        # cc 81 : add /
        # cc 82 : add ^
        # cc 83 : add ~
        # cc 84 : add long vowel
        # cc 85 : add "big" long vowel
        # cc 86 : add short vowel
        # cc 87 : add one dot over
        # cc 88 : add two dots over
        # cc 89 : add smooth
        # cc 8a : add circle
        # cc 8b : add //
        # cc 8c : add v over
        # cc 8d : add | over
        # cc 8e : add || over
        # cc 8f : add \\ over
        # ... lots of weird stuff
        for j in range(0x80, 0xc0):
            for i in range(0xb0, 0xbd):
                fh.write(("e1 be %2x + cc %2x = "%(i, j)).encode())
                fh.write(bytes([0xe1, 0xbe, i, 0x20, 0xe1, 0xbe, i, 0xcc, j, ord('\n')]))
        fh.write("---\n".encode())
        for i in range(0x86, 0xc0):
            fh.write(("ce %2x = "%(i)).encode())
            fh.write(bytes([0xce, i, ord('\n')]))
        for i in range(0x80, 0x90):
            fh.write(("cf %2x = "%(i)).encode())
            fh.write(bytes([0xcf, i, ord('\n')]))
        for i in range(0x80, 0xc0):
            fh.write(("e1 bc %2x = "%(i)).encode())
            fh.write(bytes([0xe1, 0xbc, i, ord('\n')]))
        for i in range(0x80, 0xC0):
            fh.write(("e1 bd %2x = "%(i)).encode())
            fh.write(bytes([0xe1, 0xbd, i, ord('\n')]))
        for i in range(0x80, 0xc0):
            fh.write(("e1 be %2x = "%(i)).encode())
            fh.write(bytes([0xe1, 0xbe, i, ord('\n')]))
        for i in range(0x80, 0xc0):
            fh.write(("e1 bf %2x = "%(i)).encode())
            fh.write(bytes([0xe1, 0xbf, i, ord('\n')]))
        fh.close()

if __name__ == '__main__':
    if False:
        l = list(_all_greek_letter_set)
        l.sort()
        for i in l:
            print(i)
    else:
        dump_unicode_ranges()

