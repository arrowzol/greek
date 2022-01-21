#!/usr/local/bin/python3

_debug = False

####################
# letters
####################

_vowels = "αειουηω"
_vowel_set = set("αειουηω")

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

_vowel_and_morphed_vowels = (
    ("α", "άὰᾶἀἄἂἆἁἅἃἇᾳᾴᾲᾷᾀᾁᾰᾱ"),
    ("ε", "έὲἐἔἒἑἕἓ"),
    ("ι", "ίὶῖἰἴἲἶἱἵἳἷϊΐῐῑ"),
    ("ο", "όὸὀὄὂὁὅὃ"),
    ("υ", "ύὺῦὐὔὒὖὑὕὓὗϋΰῠῡ"),
    ("η", "ήὴῆἠἤἢἦἡἥἣἧῃῄῂῇᾐῇ"),
    ("ω", "ώὼῶὠὤὢὦὡὥὣὧῳῴῲῷᾠῷ"),
)

_vowels_to_base = dict(((variant, base) for base, variants in _vowel_and_morphed_vowels for variant in variants))

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

def base_let(let):
    return _vowels_to_base.get(let, let)

def base_word(word):
    return "".join((
        base_let(let)
        for let in word))

####################
# syllables
####################

_diphthongs = set((
    "αι",
    "ει",
    "οι",
    "αυ",
    "ευ",
    "ου",
    "υι"))

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
        if letter in _vowel_set:
            # vowels and diphthongs end a syllable,
            #   because each syllable can have either one vowel or a diphthong, diphthong wins
            # choose the vowel or diphthong
            if b_word[index2:index2+2] in _diphthongs:
                index2 += 2
            else:
                index2 += 1

            # if there are more than one consonant, and they are not a cluster, split them
            # unless the split would join to a vowel by itself
            if syls and index2-index1 > 2 and not b_word[index1] in _consonant_cluster:
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
        else:
            syls[-1] = syls[-1] + word[index1:]
    return syls

####################
# nouns
####################

_noun_stems = {
    '12': { # αη, feminine
        'M': {
            'S': {
                'N': "ς",
                'G': "υ",
                'D': "ι",
                'A': "ν",
            },
            'P': {
                'N': "ι",
                'G': "ων",
                'D': "ις",
                'A': "υς",
            }
        },
        'F': {
            'S': {
                'N': "",
                'G': "ς",
                'D': "ι",
                'A': "ν",
            },
            'P': {
                'N': "ι",
                'G': "ων",
                'D': "ις",
                'A': "ς",
            }
        },
        'N': {
            'S': {
                'N': "ν",
                'G': "υ",
                'D': "ι",
                'A': "ν",
            },
            'P': {
                'N': "α",
                'G': "ων",
                'D': "ις",
                'A': "α",
            }
        }
    },
#    '3': { # consonants
#    }
}

_vowel_contract = {
    'αω': 'ῶ',

    'αα': 'ᾱ',
#    'εα': 'η',
    'οα': 'ω',

    'αε': 'ᾱ',
    'εε': 'ει',
    'οε': 'ον',

    'αο': 'ω',
    'εο': 'ον',
    'οο': 'ον',
}
_fix_dative = {
    'ηι': 'ῃ',
    'αι': 'ᾳ',
    'οι': 'ῳ',
}
def _noun_inflect(word, end, decl, num, cas):
    global _dbg
    b_word = base_word(word)
    _dbg = [word]

    # replace α with η if not preceeded by ειρ
    # only for first declension, singluar, genative and dative
    if decl == '12' and num == 'S' and cas in ['G', 'D'] and b_word[-1] == 'α' and b_word[-2] not in ['ε', 'ι', 'ρ']:
        word = word[:-1] + 'η'
        b_word = b_word[:-1] + 'η'
        _dbg.append(word)

    # TODO: my guess, see φωνή
    # replace η with α for plurals
    elif num == 'P' and b_word[-1] == 'η':
        word = word[:-1] + 'α'
        b_word = b_word[:-1] + 'α'
        _dbg.append(word)
        
    word = word + end
    b_word = b_word + base_word(end)

    # The first-declension genitive plural always takes a circumflex on the last syllable
    if decl == '12' and num == 'P' and cas == 'G':
        i = len(word)-1
        while i >= 0 and not b_word[i] in _vowel_set:
            i -= 1
        if i >= 0:
            while i > 0 and b_word[i-1] in _vowel_set:
                i -= 1
            word = word[:i] + add_morph(word[i], "~") + word[i+1:]

    # for dative: place iota subscript on vowels followed by iota
    # only for singular, dative
    if cas == 'D' and num == 'S':
        end2 = word[-2:]
        if b_word[-2:] in _fix_dative:
            replace = add_morph(word[-2], "i")
            word = word[:-2] + replace
            b_word = b_word[:-1]
            _dbg.append(word)

    # vowel contraction
    replace = _vowel_contract.get(b_word[-2:], None)
    if replace:
        word = word[:-2] + replace
        b_word = b_word[:-2] + replace
        _dbg.append(word)
    else:
        replace = _vowel_contract.get(b_word[-3:-1], None)
        if replace:
            word = word[:-3] + replace + word[-1]
            b_word = b_word[:-3] + replace + b_word[-1]
            _dbg.append(word)

    # alphas at the end of the word have "long" mark
    # unless it is morphed already
    if num == 'S' or cas == 'A':
        if word[-1] == 'α':
            word = word[:-1] + 'ᾱ'
            _dbg.append(word)
        elif word[-2] == 'α':
            word = word[:-2] + 'ᾱ' + word[-1]
            _dbg.append(word)

    if _debug and len(_dbg) > 1:
        print("NOUN INFLECT (%s,%s): "%(num, cas) + " -> ".join(_dbg))

    return word

def noun_inflect(word, decl, gen, num, cas):
    end = _noun_stems[decl][gen][num][cas]
    return _noun_inflect(word, end, decl, num, decl)

def noun_inflect_all(word, gen):
    words = []
#    for decl in ('12', '3'):
    for decl in ('12', ):
        for num in ('S', 'P'):
            for cas in ('N', 'G', 'D', 'A'):
                end = _noun_stems[decl][gen][num][cas]
                words.append((decl + cas + num, _noun_inflect(word, end, decl, num, cas), _dbg))
    return words

def print_noun_inflects(word, gen):
    data = noun_inflect_all(word, gen)
    max_len = max((len(word) for stuff, word, dbg in data))
    print("root: %s"%(word))
    for num_cnt in range(2):
        print("{5}:    {1:{0}s} {2:{0}s} {3:{0}s} {4:{0}s}".format(
            max_len+2,
            data[num_cnt*4+0][1],
            data[num_cnt*4+1][1],
            data[num_cnt*4+2][1],
            data[num_cnt*4+3][1],
            num_cnt+1,
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
            print("ERROR %s %s (%s exp %s) (%s exp %s)"%(name, act[0], act[1], exp[1], base_act, base_exp))
        elif act[1] != exp[1]:
            print("WARN %s %s (%s exp %s)"%(name, act[0], act[1], exp[1]))

if __name__ == '__main__':
    # F, ending ρα
    test_noun_inflect(
        "χώρα",
        noun_inflect_all("χώρα", 'F'), (
        ('12NS', 'χώρᾱ'),  ('12GS', 'χώρᾱς'), ('12DS', 'χώρᾳ'),   ('12AS', 'χώρᾱν'),
        ('12NP', 'χῶραι'), ('12GP', 'χωρῶν'), ('12DP', 'χώραις'), ('12AP', 'χώρᾱς')))

    # F, ending εα
    test_noun_inflect(
        "θεά",
        noun_inflect_all("θεά", 'F'), (
        ('12NS', 'θεά'),  ('12GS', 'θεᾶς'), ('12DS', 'θεᾷ'),   ('12AS', 'θεάν'),
        ('12NP', 'θεαί'), ('12GP', 'θεῶν'), ('12DP', 'θεαῖς'), ('12AP', 'θεάς')))

    # F, ending ια
    test_noun_inflect(
        "οἰκία",
        noun_inflect_all("οἰκία", 'F'), (
        ('12NS', 'οἰκίᾱ'),  ('12GS', 'οἰκίᾱς'), ('12DS', 'οἰκίᾳ'),   ('12AS', 'οἰκίᾱν'),
        ('12NP', 'οἰκίαι'), ('12GP', 'οἰκιῶν'), ('12DP', 'οἰκίαις'), ('12AP', 'οἰκίᾱς')))

    # F, ending η
    test_noun_inflect(
        "φωνή",
        noun_inflect_all("φωνή", 'F'), (
        ('12NS', 'φωνή'),  ('12GS', 'φωνῆς'), ('12DS', 'φωνῇ'),   ('12AS', 'φωνήν'),
        ('12NP', 'φωναί'), ('12GP', 'φωνῶν'), ('12DP', 'φωναῖς'), ('12AP', 'φωνάς')))


    if False:
        for av in _vowels:
            for al in "/\\~sriSL":
                print("%s: %s -> %s"%(al, av, add_morph(av, al)))
        for av in _vowels_to_base.keys():
            for al in "sriSL":
                print("%s: %s -> %s"%(al, av, add_morph(av, al)))

    if True:
        print_noun_inflects("χώρα", 'F')
        print_noun_inflects("θεά", 'F')
        print_noun_inflects("οἰκία", 'F')
        print_noun_inflects("φωνή", 'F')

    while False:
        word = input("What's up? ")
        word
        print("-".join(syllables(word.rstrip())))

