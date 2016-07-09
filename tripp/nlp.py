import matplotlib.pyplot as pyplot
from bs4 import BeautifulSoup
import requests
import re
from collections import defaultdict, Counter
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
        ("big data", 100, 15), ("hadoop", 95, 25), ("python", 75, 50),
        ("R", 50, 40), ("machine learning", 80, 20), ("statistics", 20, 60),
        ("data science", 60, 70), ("analytics", 90, 3),
        ("team player", 85, 85), ("dynamic", 2, 90), ("synergies", 70, 0),
        ("actionable insights", 40, 30), ("self-starter", 30, 50),
        ("think out of the box", 45, 10), ("customer focus", 65, 15),
        ("thought leadership", 35, 35)
    ]

    for word, job_popularity, resume_popularity in data:
        pyplot.text(job_popularity,
                    resume_popularity,
                    word,
                    ha='center',
                    va='center',
                    size=text_size(job_popularity + resume_popularity))
    pyplot.xlabel("Popularity of jobs postings")
    pyplot.ylabel("Popularity on resumes")
    pyplot.axis([0, 100, 0, 100])
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


def sample_from(weights):
    """returns i with probability weights[i] / sum(weights)"""
    total = sum(weights)
    rnd = total * random.random()  # uniform between 0 and total
    for i, w in enumerate(weights):
        rnd -= w
        if rnd <= 0:  # return the smallest i such that
            return i  # weights[0] + ... + weights[i] >= rnd


def p_topic_given_document(document_topic_counts,
                           document_lengths,
                           topic,
                           d,
                           k,
                           alpha=0.1):
    """the fraction of words in document d
    that are assigned to topic (plus some smoothing)"""
    return ((document_topic_counts[d][topic] + alpha) /
            (document_lengths[d] + k * alpha))


def p_word_given_topic(topic_word_counts,
                       topic_counts,
                       word,
                       topic,
                       W,
                       beta=0.1):
    """the fraction of words assigned to topic
    that equal word (plus some smoothing)"""
    return ((topic_word_counts[topic][word] + beta) /
            (topic_counts[topic] + W * beta))


def topic_weight(topic_word_counts, topic_counts, document_topic_counts,
                 document_lengths, W, d, word, k):
    """given a document and a word in that document,
    return the weight for the k-th topic"""
    return p_word_given_topic(
        topic_word_counts, topic_counts, word, k, W) * p_topic_given_document(
            document_topic_counts, document_lengths, d, k)


def choose_new_topic(topic_word_counts, topic_counts, document_topic_counts,
                     document_lengths, W, d, word, k):
    return sample_from([topic_weight(topic_word_counts, topic_counts,
                                     document_topic_counts, document_lengths,
                                     W, d, word, i) for i in range(k)])


def model_topics(documents, k=4):
    document_topic_counts = [Counter() for _ in documents]
    topic_word_counts = [Counter() for _ in range(k)]
    topic_counts = [0 for _ in range(k)]

    document_lengths = map(len, documents)
    distinct_words = set(word for document in documents for word in document)

    W = len(distinct_words)
    D = len(documents)

    random.seed(0)
    document_topics = [[random.randrange(k) for word in document]
                       for document in documents]

    for d in range(D):
        for word, topic in zip(documents[d], document_topics[d]):
            document_topic_counts[d][topic] += 1
            topic_word_counts[topic][word] += 1
            topic_counts[topic] += 1

    for iter in range(1000):
        for d in range(D):
            for i, (word,
                    topic) in enumerate(zip(documents[d], document_topics[d])):

                # remove the word & topic from the counts
                # so that it doesn't influence weights
                document_topic_counts[d][topic] -= 1
                topic_word_counts[topic][word] -= 1
                topic_counts[topic] -= 1
                document_lengths[d] -= 1

                # choose a new topic based on the weights
                new_topic = choose_new_topic(topic_word_counts, topic_counts,
                                             document_topic_counts,
                                             document_lengths, W, d, word, k)
                document_topics[d][i] = new_topic

                # and now add it back in
                document_topic_counts[d][new_topic] += 1
                topic_word_counts[new_topic][word] += 1
                topic_counts[new_topic] += 1
                document_lengths[d] += 1

    return {
        'topic_word_counts': topic_word_counts,
        'document_topic_counts': document_topic_counts,
        'topic_counts': topic_counts,
        'document_lengths': document_lengths
    }


if __name__ == '__main__':
    TEST_METHODOLOGY = 'topic modelling'

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
        '_N':
        ['data science', 'python', 'regression', 'engineering', 'management'],
        '_A':
        ['big', 'linear', 'logistic', 'unwise', 'radical', 'conservative'],
        '_P': ['about', 'near', 'behind', 'below', 'around', 'besides'],
        '_V': ['learns', 'trains', 'leaves', 'develops', 'tests', 'is']
    }

    if 'grammars' == TEST_METHODOLOGY:
        sentence = generate_sentence(GRAMMAR)
        logging.info('(grammar): {}'.format(' '.join(sentence)))

    documents = [
        ["Hadoop", "Big Data", "HBase", "Java", "Spark", "Storm", "Cassandra"],
        ["NoSQL", "MongoDB", "Cassandra", "HBase", "Postgres"],
        ["Python", "scikit-learn", "scipy", "numpy", "statsmodels", "pandas"],
        ["R", "Python", "statistics", "regression", "probability"],
        ["machine learning", "regression", "decision trees", "libsvm"],
        ["Python", "R", "Java", "C++", "Haskell", "programming languages"],
        ["statistics", "probability", "mathematics", "theory"],
        ["machine learning", "scikit-learn", "Mahout", "neural networks"],
        ["neural networks", "deep learning", "Big Data",
         "artificial intelligence"],
        ["Hadoop", "Java", "MapReduce", "Big Data"],
        ["statistics", "R", "statsmodels"],
        ["C++", "deep learning", "artificial intelligence", "probability"],
        ["pandas", "R", "Python"],
        ["databases", "HBase", "Postgres", "MySQL", "MongoDB"],
        ["libsvm", "regression", "support vector machines"]
    ]

    if 'topic modelling' == TEST_METHODOLOGY:
        models = model_topics(documents)
        topic_word_counts = models['topic_word_counts']
        document_topic_counts = models['document_topic_counts']
        topic_counts = models['topic_counts']
        for k, word_counts in enumerate(topic_word_counts):
            for word, count in word_counts.most_common():
                if count > 0: print k, word, count
