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
    'Pers.pr.':     "Np",
    'Poss.pr.':     "Np",
    'Recip.pr.':    "Np",
    'Refl.pr.':     "Np",
    'Rel.pr.':      "Np",

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

    'Cj.':          "?",
    'Cond.':        "?",
    'Disj.prt.':    "?",
    'Ij.':          "?",
    'Indec.num.':   "?",
    'Irg.prt.':     "?",
    'Neg.cj.':      "?",
    'Neg.prt.':     "?",
    'Prep.':        "?",
}

_words = {}
def read_dict():
    global _words

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

        n_types = [a_type[1] for a_type in word_types if a_type.startswith("N")]

        for gen in n_types:
            if gen in "MFN":
                sn_word = greek[0]
                b_sn_word = gl.base_word(sn_word)
                root, dgnc = gn.derive_root_given_GNC(set([gen + "SN"]), sn_word)
                if root:
                    x = gn.noun_inflect_all(root, gen)[0][2]
                    print("CPd1 %s %s %s"%(gen, b_sn_word, repr(x)))
                    for num, words2 in x.items():
                        for case, word_dbg in words2.items():
                            word = word_dbg[0]
                            b_word = gl.base_word(word)
                            l = _words.get(b_word, None)
                            if not l:
                                l = []
                                _words[b_word] = l
                            l.append(("N", gen + num + case, word, desc))
                else:
                    print("CPd0 %s %s"%(gen, b_sn_word))

    fh.close()

def lookup(word):
    return _words.get(gl.base_word(word), None)

read_dict()

