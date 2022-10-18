#!/usr/local/bin/python3

import greek_letter as gl
import greek_noun as gn

_types = {
    'letter':       "l",

    # nouns, adjectives
    'n.m.':         "NM",
    'n.f.':         "NF",
    'n.n.':         "NN",
    'n.indcl.':     "N?",

    'Article':      "a",    # definite article

    'Irg.pr.':      "Np", # irregular pronoun
    'Corr./Irg.pr.':"Np",
    'Corr.pr.':     "Np",
    'Dem.pr.':      "Np",
    'Indef.pr.':    "Np",
    'Pers.pr.':     "Np", # personal pronoun: (M, F, N) or (?)
    'Poss.pr.':     "Np",
    'Recip.pr.':    "Np",
    'Refl.pr.':     "Np",
    'Rel.pr.':      "Npr", # personal pronoun, relative

    'Prop.n.':      "NP", # proper noun (name of person or place)

    'Adj':          "j",
    'Adj.':         "j",

    # verbs, adverbs
    'v.':           "V",
    'Adv':          "v",
    'Adv.':         "v",
    '(Comp.)adv.':  "vc",
    'Comp.adv.':    "vc",
    'Irg.adv.':     "vi", # irregular adverb
    'Neg.adv.':     "vn", # negative adverb
    'Corr.adv.':    "vr",
    'Sup.adv.':     "vs",


    'Aram.':        "-a",
    'Hebr.':        "-h",
    'Heb.':         "-h",

    'Cj.':          "C", # conjunction, like και
    'Neg.cj.':      "C",
    'Disj.prt.':    "C",

    'Cond.':        "Cd", # condition, a conjunction with a condition
    'Ij.':          "?",
    'Indec.num.':   "?",
    'Irg.prt.':     "?",
    'Neg.prt.':     "?",
    'Prep.':        "?",
}

_words = {}
def _add_word(contents):
    global _words

    b_word = gl.base_word(contents[3], lower=True)
    l = _words.get(b_word, None)
    if not l:
        l = []
        _words[b_word] = l
    l.append(contents)

def _add_word_inflection(the_stem, w_type, ident, gen, desc):
    x = gn.noun_inflect_all(the_stem, gen)[0][2]
    for num, words2 in x.items():
        for case, word_dbg in words2.items():
            word = word_dbg[0]
            _add_word((w_type, ident, gen + num + case, word, desc))

def add_inflect_MFN(ident, greek, article_index, desc, word_type):
    "Add a noun, in dictionary as (MSN, FSN, NSN) or ([MF]SN, NSN)"

    # Masculine
    msn_word = greek[0]
    b_msn_word = gl.base_word(msn_word)
    msn_stem, msn_dgnc = gn.derive_stem_given_GNC(set(["MSN"]), msn_word)
    if msn_stem:
        _add_word_inflection(msn_stem, word_type, ident, "M", desc)
        print("CPd1J msn stem:%s (%s)"%(gl.base_word(msn_stem), b_msn_word))
    else:
        print("CPd0J msn (%s) %s"%(gl.base_word(b_msn_word), repr(gn._dbg_stem)))

    # Femenine
    if article_index <= 2:
        fsn_word = msn_word
        b_fsn_word = b_msn_word
    else:
        fsn_word = greek[1]
        b_fsn_word = gl.base_word(fsn_word)
        if (
               (b_msn_word[-2:] in ["ος", "υς"] and b_fsn_word in ["α", "η", "ια"])
            or (b_msn_word[-2:] in ["ης"] and b_fsn_word in ["ες"])
        ):
            fsn_word = msn_word[:-2] + fsn_word
        elif fsn_word.endswith("δε") or (len(b_msn_word)+1 >= len(b_fsn_word) and not b_msn_word.startswith(b_fsn_word[:2])):
            last_letter_match_index = b_msn_word.rfind(b_fsn_word[0])
            if last_letter_match_index != -1:
                fsn_word = msn_word[:last_letter_match_index] + fsn_word
            else:
                fsn_word = ""

    fsn_stem = ""
    if fsn_word:
        fsn_stem, fsn_dgnc = gn.derive_stem_given_GNC(set(["FSN"]), fsn_word)
        if fsn_stem and len(fsn_stem) >= 2:
            _add_word_inflection(fsn_stem, word_type, ident, "F", desc)
            print("CPd1J fsn stem:%s (%s)"%(gl.base_word(fsn_stem), gl.base_word(fsn_word)))
        else:
            print("CPd0J fsn (%s) %s"%(gl.base_word(gl.base_word(fsn_word)), repr(gn._dbg_stem)))

    # Neuter
    if article_index == 1:
        nsn_word = msn_word
        b_nsn_word = b_msn_word
    else:
        if article_index == 2:
            nsn_word = greek[1]
        else:
            nsn_word = greek[2]
        b_nsn_word = gl.base_word(nsn_word)
        if (
               (b_msn_word[-2:] in ["ος", "υς"] and b_nsn_word in ["ο", "ον", "ιον", "ουν"])
            or (b_msn_word[-2:] in ["ης"] and b_nsn_word in ["ες"])
        ):
            nsn_word = msn_word[:-2] + nsn_word
        elif nsn_word.endswith("δε") or (len(b_msn_word)+1 >= len(b_nsn_word) and not b_nsn_word.startswith(b_nsn_word[:2])):
            last_letter_match_index = b_msn_word.rfind(b_nsn_word[0])
            if last_letter_match_index != -1:
                nsn_word = msn_word[:last_letter_match_index] + nsn_word
            else:
                nsn_word = ""
    if nsn_word:
        nsn_stem, nsn_dgnc = gn.derive_stem_given_GNC(set(["NSN"]), nsn_word)
        if nsn_stem and len(nsn_stem) >= 2:
            _add_word_inflection(nsn_stem, word_type, ident, "N", desc)
            print("CPd1J nsn stem:%s (%s)"%(gl.base_word(nsn_stem), gl.base_word(nsn_word)))
        else:
            print("CPd0J nsn (%s) %s"%(gl.base_word(gl.base_word(nsn_word)), repr(gn._dbg_stem)))

    if (
            (msn_stem and fsn_stem and msn_stem != fsn_stem)
            or (msn_stem and nsn_stem and msn_stem != nsn_stem)
            or (fsn_stem and nsn_stem and fsn_stem != nsn_stem)
            ):
        print("CPdXV MSN:%s FSN:%s NSN:%s"%(msn_stem, fsn_stem, nsn_word))

def add_inflect_NG(ident, greek, article_index, desc, gen):
    "Add a noun, in dictionary as .SN, .SG"
    sn_word = greek[0]
    b_sn_word = gl.base_word(sn_word)
    sn_stem, sn_dgnc = gn.derive_stem_given_GNC(set([gen + "SN"]), sn_word)
    sn_dbg_stem = gn._dbg_stem

    sg_stem = ""
    b_sg_word = ""
    sg_dbg_stem = ""
    if article_index >= 2:
        sg_word = greek[1]
        b_sg_word = gl.base_word(sg_word)
        if (
            (b_sn_word[-2] == "ω" and b_sg_word[0] == "ο" and b_sn_word[-1] == b_sg_word[1])
            or (b_sn_word.endswith("ης") and b_sg_word == "ου")
            or (b_sn_word.endswith("ις") and b_sg_word in ["εως", "ιδος"])
        ):
            sg_word = sn_word[:-2] + sg_word
        elif not b_sg_word.startswith(b_sn_word[:-2]):
            last_letter_match_index = b_sn_word.rfind(b_sg_word[0])
            if last_letter_match_index != -1:
                sg_word = sn_word[:last_letter_match_index] + sg_word
            else:
                sg_word = ""
        if sg_word:
            sg_stem, sg_dgnc = gn.derive_stem_given_GNC(set([gen + "SG"]), sg_word)
            sg_dbg_stem = gn._dbg_stem
            if sg_stem and sn_stem and gl.base_word(sg_stem) != gl.base_word(sn_stem):
                print("CPdXN SN:%s SG:%s"%(sn_stem, sg_stem))
        b_sg_word = gl.base_word(sg_word)

    the_stem = sg_stem or sn_stem
    if sn_stem and sg_stem and len(sn_stem) > len(sg_stem):
        the_stem = sn_stem

    if the_stem:
        _add_word_inflection(the_stem, "N", ident, gen, desc)
        print("CPd1N stem:%s g:%s (%s %s)"%(gl.base_word(the_stem), gen, b_sn_word, b_sg_word))
    else:
        print("CPd0N g:%s (%s %s)\n  %s\n  %s"%(gen, b_sn_word, b_sg_word, repr(sn_dbg_stem), repr(sg_dbg_stem)))

def read_dict():
    fh = open("dict/dict.copy")
    for line in fh:
        parts = line.rstrip().split(" ")
        ident = parts[0]

        i = 1
        greek = [parts[1]]
        while parts[i].endswith(","):
            i += 1
            greek.append(parts[i])
        greek = [w[:-1] for w in greek[:-1]] + [greek[-1]]
        i += 1

        word_types = []
        go = True
        while go:
            a_type = _types[parts[i]]
            word_types.append(a_type)

            if parts[i+1] == "&":
                i += 2
            else:
                go = False
        desc = " ".join(parts[i+1:])

        if word_types[0] == "C":
            # https://ancientgreek.pressbooks.com/chapter/10/
            # conjunctions and conditions
            _add_word(("C", ident, None, greek[0], desc))
        else:
            n_types = [a_type[1] for a_type in word_types if a_type.startswith("N")]
            j_types = [a_type for a_type in word_types if a_type == "j"]

            article_index = 0
            while article_index < len(greek) and greek[article_index] not in gn.article_to_indexes:
                article_index += 1

            if j_types:
                # adjectives
                add_inflect_MFN(ident, greek, article_index, desc, "J")

            for gen in n_types:
                if gen in "MFN":
                    # regular nouns
                    add_inflect_NG(ident, greek, article_index, desc, gen)
                if gen == "p":
                    # pronouns
                    add_inflect_MFN(ident, greek, article_index, desc, "n")
    fh.close()

def lookup_nc(word, nc):
    x = _words.get(gl.base_word(word, lower=True), [])
    return [y for y in x if y[2][1:] == nc]

def lookup(word):
    """
    return list of (type, ident, GNC, word with accents, description)
    type:
        N - noun
    if not found, return an empty list
    """
    return _words.get(gl.base_word(word, lower=True), [])

read_dict()

