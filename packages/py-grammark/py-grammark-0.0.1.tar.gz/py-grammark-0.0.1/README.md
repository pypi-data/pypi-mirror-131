This is a python port of Grammark. The grammar checker developed by Mark Fullmer.
Visit https://github.com/markfullmer/grammark to learn more about Grammark.
All credit goes to markfullmer.

The contributions of this work can be summarized as follows:

* Key words, that are used by the grammar rules are collected in JSON files. This makes it hopefully easier to manage expressions and the JSON files can be used in other projects.
* The grammar rules are defined in (informal) logic. It is presented in the next section of this README. This makes the workings of grammark more transparent. However, I reverse engineered those rules from the angular app and it is absolutely possible that I made mistakes.
* The different checks implemented by grammark, e.g., passive voice, wordiness, academic style..., are provided as functions in the Python package. The functions return the ratings, as proposed by grammark and offsets indicating the problematic positions.

# Usage

Install package with pip:

```
pip install py-grammark
```
Then import the different functions:

```
from grammark import check_wordiness, \
				check_nominalizations, \
				check_passive_voice, \
				check_sentences, \
				check_academic, \
				check_transitions, \
				check_grammar, \
				check_eggcorns

text = "This is some string."

check_wordiness(text)
check_normalizations(text)
...
```
Every function can be called with the text as parameter. Text must be of type string.

The return values look as follows:

```
{
	"findings": [
		{"start_pos": 10, "end_pos": 12, "remark": "Some remark or None, if there is no"},
		...
	],
	"score": 40
}
```

It returns a dictionary. The score is calculated as defined by Grammark (https://github.com/markfullmer/grammark).
The findings contain the offsets, where the found problem, resides in the provided text.

The remarks are provided by Grammark. Again all credits goes to https://github.com/markfullmer/grammark.
The remark can be `None` if there are no remarks for a certain check.

# An (Informal) Definition of the Grammar Rules

In the following we define the workings of the different tools provided by grammark.

Thereby, $W$ represents the set of words, that is built by parsing the text provided by the user (see section *Parsing the Text* for a detailed discussion).
Furthermore, $|w|$ represents the size of word $w \in W$ and we use $w[a:b]$ for $a,b \in \mathbb{N}$ to represent substrings, where $a,b$ represent positions in the string, where the substring starts and ends, respectively.
$pre(w) \in W$ indicates the predecessing word, that occurs before $w$ in the original text provided by the user.
We write $upper(w)$ for $w \in W$ to denote the word $w$ where the first letter is capitalized.

Note that $w \in W$ represents not necessarily a single word, but can be also a sequence of words if we try to match several consecutive words.

We use $s(w)$ to denote the sentence, that contains the word $w \in W$ and $s(w)[i]$ to select words in the sentence by index $i \in \mathbb{N}$.

## Passive voice

Let $I$ be the set of irregulars and $H$ be the set of helpers with sets as defined in `src/resources/passive_voice.json`:

The passive voice check hits, if for a word $w \in W$

$(w[|w| - 1:|w|] = "ed" \lor w \in I) \land pre(w) \in H$

In text: Every word that ends with "ed" or is an irregular verb and the predecessing word is a helper word.

## Wordiness

Let $K$ be the set of keywords. It is constructed by the first elements of the set keywords in file `src/resources/wordiness.json`

The wordiness check hits, if for a word $w \in W$

$\forall k \in K: w = k \lor w = upper(k)$

In text: We look if one of the elements in $K$ occurs in the text. We do this also for the situation, that it has a capitalized first letter.

## Nominalizations

Let $E$ be the set of postfixes taken from the file `src/resources/normalizations.json`

The nominalization check hits if for a word $w \in W$

$\exists a,b \in \mathbb{N}: w[a:b] \in E \land |w| > 7$

In text: The rule checks if the word $w$ ends with a postfix contained in $E$ and if its length is greater than seven.

## Sentences

Let $K$ be the set of keywords as defined in file `src/resources/sentences.json`

The sentences check hits if for a word $w \in W$

$|s(w)| > 50 \lor s(w)[0] \in K$

Here $|s(w)|$ denotes the number of words in the sentence.

## Transitions

Let $K$ be the set of keywords from the file `src/resources/transitions.json`

The transition check hits, if for a word $w \in W$

$\forall k \in K: w = k \lor w = upper(k)$

In text: We look if one of the elements in $K$ occurs in the text. We do this also for the situation, that it has a capitalized first letter.

## Academic

Let $K$ be the set of keywords from the file `src/resources/academic.json`

The academic check hits, if for a word $w \in W$

$\forall k \in K: w = k \lor w = upper(k)$

In text: We look if one of the elements in $K$ occurs in the text. We do this also for the situation, that it has a capitalized first letter.

## Grammar

Let $K$ be the set of keywords from the file `src/resources/grammar.json`

The grammar check hits, if for a word $w \in W$

$\forall k \in K: w = k \lor w = upper(k)$

In text: We look if one of the elements in $K$ occurs in the text. We do this also for the situation, that it has a capitalized first letter.

## Egcorns

Let $K$ be the set of keywords from the file `src/resources/eggcorns.json`

The grammar check hits, if for a word $w \in W$

$\forall k \in K: w = k \lor w = upper(k)$

In text: We look if one of the elements in $K$ occurs in the text. We do this also for the situation, that it has a capitalized first letter.

## Parsing the Text

Basically, we use two variants to work with the text. Either we check word-wise, thereby,
the text is split based on the following chars " ,.!?:-\n'\")({}". That means word are
limited by these chars and will be identified as single words.

The other variant is based on regex in the hope that this is for certain operations more efficient.

# Development

# Build

```
python3 -m build
```

# Run tests

```
python3 -m unittest tests.test_grammark.TestGrammark
```
