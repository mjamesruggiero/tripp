import matplotlib.pyplot as pyplot
from bs4 import BeautifulSoup
import requests
import re
from collections import defaultdict
import random
import logging

logging.basicConfig(level=logging.INFO, format="%(lineno)d\t%(message)s")


def text_size(total):
    """Equals 8 if total is 0, 28 if total is 200"""
    return 8 + total / 200 * 20

def fix_unicode(text):
    return text.replace(u'\u2019', "'")

def build_buzzword_ranking():
    data = [
        ("big data", 100, 15),
        ("hadoop", 95, 25),
        ("python", 75, 50),
        ("R", 50, 40),
        ("machine learning", 80, 20),
        ("statistics", 20, 60),
        ("data science", 60, 70),
        ("analytics", 90, 3),
        ("team player", 85, 85),
        ("dynamic", 2, 90),
        ("synergies", 70, 0),
        ("actionable insights", 40, 30),
        ("self-starter", 30, 50),
        ("think out of the box", 45, 10),
        ("customer focus", 65, 15),
        ("thought leadership", 35, 35)
    ]

    for word, job_popularity, resume_popularity in data:
        pyplot.text(job_popularity, resume_popularity, word,
                 ha='center', va='center',
                 size=text_size(job_popularity + resume_popularity))
    pyplot.xlabel("Popularity of jobs postings")
    pyplot.ylabel("Popularity on resumes")
    pyplot.axis([0, 100, 0 , 100])
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.show()

def generate_using_bigrams(transitions):
    current = "."
    result = []
    while True:
        next_word_candidates = transitions[current]
        current = random.choice(next_word_candidates)
        result.append(current)
        if current == ".":
            return " ".join(result)

def generate_using_trigrams(starts, transitions):
    current = random.choice(starts)
    prev = "."
    result = [current]
    while True:
        next_word_candidates = transitions[(prev, current)]
        next_word = random.choice(next_word_candidates)

        prev, current = current, next_word
        logging.debug("result is {}".format(result))
        result.append(current)
        if current == ".":
            return " ".join(result)

def get_document(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html5lib')

    content = soup.find("div", "article-body")

    # match word or period
    regex = r"[\w']+|[\.]"

    document = []
    for paragraph in content("p"):
        words = re.findall(regex, fix_unicode(paragraph.text))
        document.extend(words)
    return document

def get_bigram(document, count=10):
    bigrams = zip(document, document[1:])
    transitions = defaultdict(list)
    for prev, current in bigrams:
        transitions[prev].append(current)

    random.seed(0)
    result = []
    for i in range(count):
        result.append(generate_using_bigrams(transitions))
    return result

def get_trigram(document):
    trigrams = zip(document, document[1:], document[2:])
    trigram_transitions = defaultdict(list)
    starts = []
    for prev, current, next in trigrams:
        if prev == ".":
            starts.append(current)
        trigram_transitions[(prev, current)].append(next)

    logging.debug("starts is {}".format(starts))
    generated = generate_using_trigrams(starts, trigram_transitions)
    return generated

def is_terminal(token):
    return token[0] != '_'

def expand(grammar, tokens):
    for i, token in enumerate(tokens):

        # skip terminals
        if is_terminal(token):
            continue

        # if you got here, we found a non-terminal token
        # and we need to choose a random replacement
        replacement = random.choice(grammar[token])

        if is_terminal(replacement):
            tokens[i] = replacement
        else:
            tokens = tokens[:i] + replacement.split() + tokens[(i + 1):]

        # call yourself on the new list of tokens
        return expand(grammar, tokens)

    # if we get this far, it was all terminals
    return tokens

def generate_sentence(grammar):
    return expand(grammar, ['_S'])



if __name__ == '__main__':
    TEST_METHODOLOGY = 'grammars'

    url = "http://radar.oreilly.com/2010/06/what-is-data-science.html"

    if 'bigrams' == TEST_METHODOLOGY:
        document = get_document(url)
        bigrams = get_bigram(document, count=20)
        for l in bigrams:
            logging.info("bigram -> {}".format(l))

    if 'trigrams' == TEST_METHODOLOGY:
        document = get_document(url)
        for i in range(0, 5):
            trigram_sentence = get_trigram(document)
            logging.info("trigram-> {}".format(trigram_sentence))

    GRAMMAR = {
        '_S': ['_NP _VP'],
        '_NP': ['_N', '_A _NP _P _A _N'],
        '_VP': ['_V', '_V _NP'],
        '_N': ['data science', 'python', 'regression', 'engineering', 'management'],
        '_A': ['big', 'linear', 'logistic', 'unwise', 'radical', 'conservative'],
        '_P': ['about', 'near', 'behind', 'below', 'around', 'besides'],
        '_V': ['learns', 'trains', 'leaves', 'develops', 'tests', 'is']
    }

    if 'grammars' == TEST_METHODOLOGY:
        sentence = generate_sentence(GRAMMAR)
        logging.info('(grammar): {}'.format(' '.join(sentence)))

