""" This scripts run on Python 3.

This scripts takes a source folder (hardcoded for now as mood-tense-voice/*.tsv) and an output folder 
(hardcoded mood-tense-voice-pft). It requires a tense.tsv (additional-data/tense.tsv) which classifies
LASLA tenses as composed or not. Composed tense in LASLA means it uses an auxiliary (esse) and a 
perfect. We removed this distinction in the output of our model: particips are classified as particips
and auxiliaries as their own tense.



Author: Thibault Clérice (leponteineptique  -[chez]- gmail.com)
"""


import glob
import os
import argparse

here = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Input folder", default=os.path.join(here, "..", "OUTPUT", "step-1"))
parser.add_argument("--output", help="Output folder", default=os.path.join(here, "..", "OUTPUT", "step-2"))
parser.add_argument("--tense", help="Tense file", default=os.path.join(here, "tense.tsv"))
args = parser.parse_args()
inp, out, tense = args.input, args.output, args.tense

os.makedirs(args.input, exist_ok=True)

comps = []
with open("tenses.tsv") as f:
	for line in f:
		try:
			tense, composed = line.strip().split("\t")
			if composed == "o" and not tense.startswith("Par"):
				comps.append(tense)
		except:
			continue

print(comps)

for file in glob.glob("mood-tense-voice/*.tsv"):
	with open(file.replace("mood-tense-voice", "mood-tense-voice-pft"), "w") as o:
		with open(file) as i:
			for line_no, line in enumerate(i):
				if line.strip():
					if line_no == 0:
						header = line.strip().split("\t")
						o.write(line)
					else:
						line_dict = dict(zip(header, line.strip().split("\t")))
						mtv = line_dict["Mood_Tense_Voice"]
						if mtv in comps:
							print(line_dict)
							m, t, v = mtv.split("|")

							# Indicative do not needs new cases or person change
							if m == "Inf":
								m = "Par"
								if "Fut" in t:
									t = "Fut"
								else:
									t = "Perf"
							else:
								if "Fut" in t:
									t = "Fut"
								else:
									t = "Perf"
								m = "Par"
								if line_dict["Case"] != "_":
									line_dict["Case"] = "Nom"
								line_dict["Person"] = "_"
							line_dict["Mood_Tense_Voice"] = "|".join([m, t, v])
							o.write("\t".join([line_dict[head] for head in header])+"\n")
						else:
							o.write(line)
				else:
					o.write(line)