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
            article_index = 0
            while article_index < len(greek) and greek[article_index] not in gn.article_to_indexes:
                article_index += 1
            if gen in "MFN":
                print("CPdStart %s %s"%(ident, gen))
                sn_word = greek[0]
                b_sn_word = gl.base_word(greek[0])
                sn_stem, sn_dgnc = gn.derive_stem_given_GNC(set([gen + "SN"]), sn_word)

                sg_stem = None
                if article_index >= 2:
                    sg_word = greek[1]
                    b_sg_word = gl.base_word(sg_word)
                    if b_sg_word[0] == "ο" and b_sn_word[-2] == "ω" and b_sg_word[1] == b_sn_word[-1]:
                        sg_word = sn_word[:-2] + sg_word
                    elif b_sg_word == "εως" and b_sn_word.endswith("ις"):
                        sg_word = sn_word[:-2] + sg_word
                    elif b_sg_word == "ιδος" and b_sn_word.endswith("ις"):
                        sg_word = sn_word[:-2] + sg_word
                    elif not b_sg_word.startswith(b_sn_word[:-2]):
                        last_letter_match_index = b_sn_word.rfind(b_sg_word[0])
                        if last_letter_match_index != -1:
                            sg_word = sn_word[:last_letter_match_index] + sg_word
                        else:
                            sg_word = None
                    if sg_word:
                        print("CPdY %s"%(sg_word))
                        sg_stem, sg_dgnc = gn.derive_stem_given_GNC(set([gen + "SG"]), sg_word)
                        if sg_stem and sn_stem and gl.base_word(sg_stem) != gl.base_word(sn_stem):
                            print("CPdX SN:%s SG:%s"%(sn_stem, sg_stem))

                the_stem = sg_stem or sn_stem
                if sn_stem and sg_stem and len(sn_stem) > len(sg_stem):
                    the_stem = sn_stem

                if the_stem:
                    x = gn.noun_inflect_all(the_stem, gen)[0][2]
                    print("CPd1 stem:%s g:%s %s"%(the_stem, gen, repr(x)))
                    for num, words2 in x.items():
                        for case, word_dbg in words2.items():
                            word = word_dbg[0]
                            b_word = gl.base_word(word, lower=True)
                            l = _words.get(b_word, None)
                            if not l:
                                l = []
                                _words[b_word] = l
                            l.append(("N", ident, gen + num + case, word, desc))
                else:
                    print("CPd0 %s %s"%(gen, gl.base_word(sn_word)))

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

