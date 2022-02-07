import go_greek as g

_morph_do_long_alpha = False
_guess_alpha_eta_omicron = True

# Koine Greek evloved from Attic Greek

# Nominative: subject
# Genitive: posession
# Dative: indirect object
# Accusative: object of a transitive verb, direct object of verbs
# Vocative: JOE, what are you doing?


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

def_art_base = (
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

def_art_to_indexes = {}
for def_art, index in zip(def_art_base, range(2*3*4)):
    if not def_art in def_art_to_indexes:
        def_art_to_indexes[def_art] = []
    def_art_to_indexes[def_art].append(index)


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
                'N': "σ",
                'G': "οσ",
                'D': "ι",
                'A': "α",   # or ν
                'V': "",    # or σ
            },
            'D': {
                'N': "ε",
                'G': "σιν",
                'D': "σιν",
                'A': "ε",
                'V': "ε",
            },
            'P': {
                'N': "εσ",
                'G': "ων",
                'D': "σι",
                'A': "ασ",
                'V': "εσ",
            },
        },
        'N': {
            'S': {
                'N': "",
                'G': "οσ",
                'D': "ι",
                'A': "",   # or ν
            },
            'P': {
                'N': "α",
                'G': "ων",
                'D': "σι",
                'A': "α",
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

_labials = "πβφ"    # and ".σ" -> "ψ"
_palatals = "κγχ"   # and ".σ" -> "ξ"
_dentals = "τδθ"    # and ".σ" -> "σ"

_stop_xform_consonants = dict(
    list(zip(_labials, "ψψψ")) +
    list(zip(_palatals, "ξξξ")) +
    list(zip(_dentals, "...")))

# preferred endings: ν, ρ, ς (sometimes ι or υ as semi-consonants)
# note: πατηρ + ς = πατηρ (father; ρ + ς = ρ)

def _noun_inflect(word, decl, gen, num, cas, do_dbg=True):
    end = _noun_stems[decl][gen][num][cas]

    _dbg = None
    if do_dbg: _dbg = [(word + "-" + end, "start")]

    b_word = g.base_word(word, True)
    # replace α with η if not preceeded by ειρ
    # only for first declension, (genative|dative)-singluar
#    if decl == '1' and num == 'S' and cas in ['G', 'D'] and b_word[-1] == 'α' and b_word[-2] not in ['ε', 'ι', 'ρ']:
#        word = word[:-1] + g.cp_morph('η', word[-1])
#        b_word = b_word[:-1] + 'η'
#        if do_dbg: _dbg.append((word + "-" + end, "α->η"))

    if decl == '3':
        word = word + end
        b_word = g.base_word(word)

        if b_word[-1] == 'σ':
            replace = _stop_xform_consonants.get(b_word[-2], None)
            if replace:
                if replace == ".":
                    replace = ""
                word = word[:-2] + replace
                if do_dbg: _dbg.append((word, "stop xform " + + replace))
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
                    word = word[:-1] + g.cp_morph(new_last_let, word[-1])
                    b_word = b_word[:-1] + new_last_let
                    if do_dbg: _dbg.append((word + "-" + end, "%s->%s"%(last_let, new_last_let)))

                # this should only be done sometimes
                if num == "S":
                    if do_dbg: _dbg.append((word + "-" + end, "skip %s->%s"%(last_let, new_last_let)))

        # remove trailing sigma before applying the ending
        if last_let == 'σ':
            word = word[:-1]

        # apply the ending
        if end[0] == ".":
            word = word + end[1:]
            if do_dbg: _dbg.append((word, "combine_keep_last"))
        elif end[0] == "i":
            end_let = word[-1]
            if g.base_let(end_let) in "ηαο":
                word = word[:-1] + g.add_morph(word[-1], "i") + end[1:]
                if do_dbg: _dbg.append((word, "combine_iota"))
            else:
                word = word + end[1:]
                if do_dbg: _dbg.append((word, "combine_iota_oops"))
        else:
            word = word[:-1] + end
            if do_dbg: _dbg.append((word, "combine_rm_last"))

    b_word = g.base_word(word)

    if b_word[-2:] == "νσ":
        word = word[:-1]
        b_word = b_word[:-1]
        if do_dbg: _dbg.append((word, "νσ->ν"))

    i_last_v = len(word)-1
    # find last vowel
    while i_last_v >= 0 and not b_word[i_last_v] in g._lower_vowel_set:
        i_last_v -= 1
    if i_last_v >= 0:
        # vowel contraction
        # affects 2 or 3 vowels together
        # done before moving morphs
        if i_last_v > 0 and b_word[i_last_v-1] in g._lower_vowel_set:

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

                    replace = replace[:-1] + g.cp_morph(g.cp_morph(g.cp_morph(replace[-1], word[i_last_v-2]), word[i_last_v-1]), word[i_last_v])
                    word = word[:i_last_v-2] + replace + word[i_last_v+1+ii:]
                    b_word = b_word[:i_last_v-2] + replace + b_word[i_last_v+1+ii:]

                    i_last_v -= 3 - len(replace) + ii
                    if do_dbg: _dbg.append((word, "contract-3", find, replace))

            # try 2 letters ending at last vowel
            # (if i_last_v > 2) for θεὸσ and λαῷ
            if i_last_v > 2 and b_word[i_last_v-1] in g._lower_vowel_set:
                find = b_word[i_last_v-1:i_last_v+1]
                replace = _vowel_contract.get(find, None)
                if not replace and b_word[i_last_v-1] == b_word[i_last_v]:
                    replace = g.cp_morph(word[i_last_v-1], word[i_last_v])
                if replace:
                    # if this would create a double-vowel, don't
                    ii = 0
                    if replace[-1] == word[i_last_v+1:i_last_v+2]:
                        ii = 1

                    word = word[:i_last_v-1] + replace + word[i_last_v+1+ii:]
                    b_word = b_word[:i_last_v-1] + g.base_word(replace) + b_word[i_last_v+1+ii:]
                    i_last_v -= 2 - len(replace) + ii
                    if do_dbg: _dbg.append((word, "contract-2", find, replace))

        # moving morphs to the last vowel in diphthongs
        if i_last_v > 0 and b_word[i_last_v-1:i_last_v+1] in g._diphthongs:
            # move accent from beginning to end of diphthong
            # affects [αεου][ιυ]
            let1 = word[i_last_v-1]
            let1_morph = g.get_morph(let1)
            let1 = g.base_let(let1)

            let2 = g.add_morph(word[i_last_v], let1_morph)
            if let2 != word[i_last_v]:
                word = word[:i_last_v-1] + let1 + let2 + word[i_last_v+1:]
                if do_dbg: _dbg.append((word, "mv"))

        # accent translation
        if cas == 'G' and num == 'S':
            word2 = g.translate_morph(word, i_last_v, "\\", "~")
            if word2:
                word = word2
                if do_dbg: _dbg.append((word, "\\ -> ~"))
        if cas == 'D' and num == 'P':
            word2 = g.translate_morph(word, i_last_v, "/", "~")
            if word2:
                word = word2
                if do_dbg: _dbg.append((word, "/ -> ~"))
        if cas in 'N' and num == 'P':
            word2 = g.translate_morph(word, i_last_v, "/", "\\")
            if word2:
                word = word2
                if do_dbg: _dbg.append((word, "/ -> \\"))
        if cas in 'A' and num == 'P':
            word2 = g.translate_morph(word, i_last_v, "\\", "/")
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

    # set last sigma
    if g.base_let(word[-1]) == 'σ':
        word = word[:-1] + g.cp_morph('ς', word[-1])

    return (word, _dbg)

# D1 M ends in ης ας
# D1 F ends in η α
#   1: [MF]:[SPD]:[NAGDV] -> [.iα]α*
# D2 [MF]: ending is ος
# D2 [N]: ending is ον
#   2: [MFN]:[SPD]:[NAGDV] -> [.iα]α*
# D3 consonants
#   3: [-]:[SPD]:[NAGDV] -> [.iα]α*
def decl_gen(word, gen):
    """
    word - root word, no stem
    """
    b_word = g.base_word(word)
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
        for num in ('S', 'P'): # TODO: 'D' removed, not for 3rd declension, not interesting
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

####################
# transform
####################

_root_ends = [
    ("1", "M", "ης"),
    ("1", "M", "ας"),
    ("1", "F", "η"),
    ("1", "F", "α"),

    ("2", ".", "ος"),
    ("2", "N", "ον"),

    ("3", ".", "ν"),
    ("3", ".", "ρ"),
    ("3", ".", "ς")]

_end_to_what = {}
for decl, gen, end in _root_ends:
    gens = gen
    if gens == ".":
        if decl == "3":
            gens = "-"
        else:
            # usualy M, but could be F
            gens = "MF"
    for gen in gens:
        for num in "SP":
            for cas in "NGDA":
                word, _dbg = _noun_inflect("βββ" + end, decl, gen, num, cas)

                word_end = g.base_word(word[3:])

                what_list = _end_to_what.get(word_end, None)
                if not what_list:
                    what_list = []
                    _end_to_what[word_end] = what_list
#                print("CP9 %s %s %s %s %s %s"%(word_end, end, decl, gen, num, cas))
                what_list.append((end, decl, num + gen + cas))

def derive_noun_root(def_art, word, existing_roots=None):
    word = g.base_word(word)
    art_is = set((
        "SP"[(i//12)] + "MFN"[i%3] + "NGDA"[(i//3)%4]
        for i in def_art_to_indexes[def_art]))

    for i in range(4,0,-1):
        word_end = word[-i:]
        what = _end_to_what.get(word_end, None)
        if what:
            word_start = word[:-i]
            fildered_what = [   
                (w_end, w_decl)
                for w_end, w_decl, w_ngc in what
                if
                    (
                        w_ngc in art_is
                        or (w_ngc[1] == "-" and (
                            w_ngc[0] + "M" + w_ngc[2] in art_is
                            or w_ngc[0] + "F" + w_ngc[2] in art_is
                            ))
                    ) and (
                        not existing_roots
                        or g.base_word(word_start) + w_end in existing_roots)]
            all_ends = set([end for end, w_decl in fildered_what])
            if len(all_ends) == 1:
                root = word_start + fildered_what[0][0]
                print("CP1 %s %s %s %s %s %s"%(def_art, word, root, repr(art_is), repr(what), repr(all_ends)))
                return root

            if existing_roots:
                # TODO: this section "guesses" the right answer
                # there may be better heuristics here, but is it worth the time?
                if _guess_alpha_eta_omicron:
                    fildered_what = [   
                        (w_end, w_decl)
                        for w_end, w_decl, w_ngc in what
                        if (
                            w_ngc in art_is
                            or (w_ngc[1] == "-" and w_ngc[0] + "M" + w_ngc[2] in art_is))]
                    first_letters = set((end[0] for end, decl in fildered_what))
                    for first_letter in first_letters:
                        if first_letter not in "αηο":
                            break
                    else:
                        last_letters = set((end[1:] for end, decl in fildered_what))
                        if len(last_letters) == 1:
                            # prefere alpha
                            choices = [end for end, decl in fildered_what]
                            choices.sort()

                            root = word_start + choices[0]
                            print("CP1-b %s %s %s %s %s"%(word, root, repr(art_is), repr(what), repr(all_ends)))
                            return root

                    all_ends = set([end for end, w_decl in fildered_what])
                print("CP2 %s %s %s : %s+%s %s | %s"%(def_art, word, g.base_word(word), word_start, word_end, repr(what), repr(art_is)))

    return None

def split_last_syllable(word):
    """Feeble attempt to get the root of this noun"""
    b_word = g.base_word(word)

    # find last vowel in last syllable
    i = len(word)-1
    while i >= 0 and not b_word[i] in g._lower_vowel_set:
        i -= 1

    if i >= 0:

        # find first vowel in last syllable
        j = i
        while j >= 0 and b_word[j-1] in g._lower_vowel_set:
            j -= 1

#        if j-1+1 >= 3 and word[j:j+2] in g._diphthongs:
#            j += 2
        return (word[:j], word[j:])
    return (None, None)

