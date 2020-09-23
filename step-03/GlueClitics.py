#!/usr/bin/env python
# coding: utf-8

""" This scripts 
- transform arabic numerals into 1, 2 or 3 
- glue clitics together
"""

import glob
import os
from typing import Dict, List
import regex as re
import argparse
from collections import Counter


here = os.path.dirname(os.path.abspath(__file__))



parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Input folder", default=os.path.join(here, "..", "OUTPUT", "step-02"))
parser.add_argument("--output", help="Output folder", default=os.path.join(here, "..", "OUTPUT", "step-03"))
parser.add_argument("--clitic_char", help="Character used to join clitics with their attached lemma", default="界")
args = parser.parse_args()
dir_inp, dir_out, CLITIC_CHAR = args.input, args.output, args.clitic_char



os.makedirs(dir_out, exist_ok=True)

def write_sentence(fio, sentence: List[Dict[str, str]]):
    fio.write("\n".join(
        "\t".join(list(tok.values()))
        for tok in sentence
    )+"\n"*2)


counts = {3: 0, 2: 0, 1: 0}
div = Counter()

def transform_numeric(token: Dict[str, str], c=counts, d=div) -> Dict[str, str]:
    if token["token"].isnumeric():
        v = int(token["token"])
        div[v] += 1
        if v > 3:
            v = 3
        elif v == 2:
            v = 2
        else:
            v = 1
        c[v] += 1
        token["token"] = token["lemma"] = str(v)
    for key, value in token.items():
        if key not in ("token", "lemma", "pos"):
            token[key] = "_"
    return token
    
def treat_sentence(sentence, file, lineno, CLITIC=CLITIC_CHAR):
    changed = 0
    for index, token in enumerate(sentence):
        # Dealing with previously undetected clitics
        if (
                index > 0 and 
                token["token"] == sentence[index-1]["token"] and 
                token["lemma"] != sentence[index-1]["lemma"] and 
                token["lemma"].split("_")[0] != sentence[index-1]["lemma"].split("_")[0]
            ):
            
            sentence[index-1]["lemma"] += CLITIC + token["lemma"]
            #if token["lemma"] not in (
            #    "ne_2",
            #    "uolo_3",
            #    "sum_2",
            #    "sum_1",
            #    "ipse") and token["pos"] not in ("ADJord", "ADJcar"):
            #    print(sentence[index-1]["lemma"], file, lineno)
            sentence.pop(index)
            return treat_sentence(sentence, file, lineno, CLITIC=CLITIC)
        # Dealing with previously modified clitics
        if token["token"].startswith("-"):
            sentence[index-1]["token"] += token["token"][1:]
            sentence[index-1]["lemma"] += CLITIC + token["lemma"]
            sentence.pop(index)
            return treat_sentence(sentence, file, lineno, CLITIC=CLITIC)
        # Dealing with a true positive but badly formated
        if token["token"] == "-adduxtin":
            sentence[index-1]["lemma"] += CLITIC + "ne"
            sentence.pop(index)
            return treat_sentence(sentence, file, lineno, CLITIC=CLITIC)
        # Dealing with numbers
        if token["token"].isnumeric():
            sentence[index] = transform_numeric(token)
        if token["lemma"] == "seruus界sum界seruus":
            token["lemma"] = "seruus界sum"
    return sentence

for file in glob.glob(os.path.join(dir_inp, "*")):
    with open(file) as f:
        with open(file.replace(dir_inp, dir_out), "w") as outio:
            sentence = []
            for lineno, line in enumerate(f):
                line = line.strip()
                if not line:
                    sentence = treat_sentence(sentence, file, lineno)
                    write_sentence(outio, sentence)
                    sentence = []
                    continue 
                if lineno == 0:
                    outio.write(line+"\n")
                    header = line.split("\t")
                    continue
                line = dict(zip(header, line.split("\t")))
                sentence.append(line)
print(counts)