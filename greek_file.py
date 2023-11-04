import re

import greek_letter as gl

########################################
# convert unicode chars to standard set.
# The standard set is what's typeable
########################################

ignore = set(['᾿', '῎', '῞', '῏', '῾'])
is_ok = set(['·'])

_net_chars = {
    # choose different char, same meaning, different "font"
        ";": ";",
        "’": "'",
        "·": "·",

        # proper to types by keyboard
        "ά": "ά",
        "έ": "έ",
        "ί": "ί",
        "ό": "ό",
        "ύ": "ύ",
        "ή": "ή",
        "ώ": "ώ",

        "Ά": "Ά",
        "Έ": "Έ",
        "Ί": "Ί",
        "Ό": "Ό",
        "Ύ": "Ύ",
        "Ή": "Ή",
        "Ώ": "Ώ",

        "ΐ": "ΐ",
        "ΰ": "ΰ",

    # remove markings
        "ᾱ́": "ά",

        # rough rho
        "Ῥ": "Ρ",
        "ῥ": "ρ",
        "ῤ": "ρ",
}

weird = set()

def standardize_let(letter):
    if letter in ignore:
        return ""
    c = _net_chars.get(letter, letter)
    if c and c not in is_ok and c not in gl._all_greek_letter_set:
        if ord(c) > 128:
            weird.add(c)
    return c

def standardize_word(word):
    return "".join((standardize_let(letter) for letter in word))

def get_weird():
    "A set of unrecognized characters, may require investigation"
    return weird

########################################
# read files
########################################

def read_document(files, yield_punctuation=False, yield_chapters_and_verses=False, yield_eol=False):
    """
    Read greek words from a list of document files

    Punctuation will be returned with "P" as it's first character.
    Chapter and verse will be returned as "C:%d V:%d"
    End of line will be returned as "EOL"
    """
    for fn in files:
        fh = open(fn)

        ch = '0'
        for line in fh:
            if line.startswith("CH "):
                ch = line[3:].rstrip()
                continue

            line = standardize_word(line)
            tail = 0;
            in_num = False
            for head in range(len(line)):
                letter = line[head]
                if letter >= "0" and letter <= "9":
                    if not in_num:
                        if head > tail:
                            yield line[tail:head]
                        tail = head
                        in_num = True
                    continue

                if in_num:
                    in_num = False
                    if yield_chapters_and_verses:
                        yield "C:" + ch + " V:" + line[tail:head]
                    tail = head

                if not letter in gl._all_greek_letter_set:
                    if head > tail:
                        yield line[tail:head]
                    if letter not in " \t\n\r" and yield_punctuation:
                        yield "P" + letter
                    tail = head+1
            if tail+1 < len(line):
                yield line[tail:]
            if yield_eol:
                yield "EOL"
        fh.close()

def read_word_file(file, order):
    """
        read a "word" file.
        return a list of dict mapping inflection type to a word

        file - name of the file
        order - comma separated list of inflection keys
    """
    request_order = re.split(", *", order)
    reorder = list(range(len(request_order)))
    begin = False
    word = {}
    words = []
    states = {}
    with open(file, "r") as fh:
        for line in fh:
            line = line.rstrip();
            if not line:
                begin = False
            elif line.startswith("ORDER: "):
                file_order = re.split(", *", line[7:])
                reorder = [file_order.index(x) for x in request_order]
            elif line.startswith("BEGIN"):
                begin = True
                if word:
                    words.append(word)
                word = {}
                state = ""
                prev_idx = -2
            elif begin:
                (key, value) = line.split(":")
                idx = key.rfind(" ")
                key = key[idx+1:]
                if value:
                    key = state + key
                    key = "".join((key[i] for i in reorder))
                    word[key] = value.strip()
                else:
                    if idx > prev_idx:
                        states[str(idx)] = state
                        state += key
                    else:
                        state = states[str(idx)] + key
                    prev_idx = idx
    if word:
        words.append(word)
    return words

