# thesis-lasla-pipeline

Pipeline to convert LASLA data to refined Pie compatible data in the context of my PhD

## Step-by-step explanation

### Step 0

Convert APN/BPN using BPN converter

### Step 1

Use protogenie with protogenie-configs/step-1.xml

#### Changes applied

- V -> u
- POS with Declension indentifier (such as VER1 and NOM2) are mapped to POS without declension identifier
- Split morphs into multiple elements (Gend, Numb, Case, Deg, Mood_Tense_Voice, Person)
- Extract numbers from lemma (such as hic1) to a new column Dis (for disambiguation)
- Extract entities identifiers (such as Romanus_a) to a new column Entity
- Converts Roman numbers to Arabic numbers
	- Replaces some Roman Numbers (XXC/IIX) to more normative form before
- Remove dots from tokens (mostly for abbreviation such as L.)


#### Logs

The log of this step is available at ./protogenie-memory/step-1-memory.csv

### Step 2

Deals with Composed Tenses

### Step 3

Deals with Clitics