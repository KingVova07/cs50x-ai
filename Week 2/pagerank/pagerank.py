import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    model = {}
    pages = corpus[page]

    if pages:
        value = damping_factor / len(pages)
        remains = (1 - damping_factor) / len(corpus)
        for i in corpus:
            model[i] = remains

        for i in corpus[page]:
            model[i] += value
    else:
        for i in corpus:
            model[i] = 1.0 / len(corpus)

    return model



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    distribution = {}.fromkeys(corpus.keys(),0)
    page = random.choices(list(corpus.keys()))[0]


    for i in range(1,n):
        curr_distribution = transition_model(corpus,page,damping_factor)
        for j in distribution:
            distribution[j] = (((i-1) * distribution[j]) + curr_distribution[j]) / i
        #print (distribution)
        page = random.choices(list(distribution.keys()), weights = list(distribution.values()), k = 1)[0]

    return distribution


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    total = len(corpus)
    curr_distribution = {}.fromkeys(corpus.keys(),1/total)

    flag = True
    while flag:
        distribution = copy.deepcopy(curr_distribution)
        for page in corpus:
            curr_distribution[page] = ((1 - damping_factor)/total) + (damping_factor * get_sum(corpus,curr_distribution,page))
            if abs(curr_distribution[page] - distribution[page]) < 0.001:
                flag = False
            else:
                flag = True

    return distribution



def get_sum(corpus,distribution,page):
    result = 0

    for p in corpus:
        if page in corpus[p]:
            result += distribution[p] / len(corpus[p])

    return  result


if __name__ == "__main__":
    main()
