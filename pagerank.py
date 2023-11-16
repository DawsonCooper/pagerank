import os
import random
import re
import sys

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
    Return a dictionary probability distribution over which page to visit next,
    given a current page. 
    ex. {pageKey/link: probability, pagekey/link: probability, ...}
    

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # total distribution of any page being chosen key = page value = probability
    distribution = dict()
    # set of pages that are linked by the current page 
    currentPageLinks = corpus[page]
    
    # calculate the base probability for each page in the corpus being chosen completly at random after the damping factor is applied and divided evenly among all pages in the corpus
    for page in corpus:
        distribution[page] = (1 - damping_factor) / len(corpus)
        
    # for each page that is linked by current add the probability of being chosen at random to the distribution of all pages being chosen
    for page in currentPageLinks:
        evenDistribution = damping_factor / len(currentPageLinks)
        distribution[page] += evenDistribution
    
    print(distribution)
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    
    result = {pageInCorpus: probability, pageInCorpus: probability, ...}
    
    """
    result = dict()
    # this page will start as a random page then will be updated throughout our sample loop 
    currPage = random.choice(list(corpus.keys()))
    """
    sample loop starts on a random page then chooses a page based on the probability distribution of returned from transition_model
    each time we visit a page we can increment the value of that page in our result dictionary by 1
    after the loop is finished we can loop over our result dictionary and divide each value by the total number of samples to get the probability of each page being chosen
    """
    for i in range(n):
        
        pass
    
    
    
    return result


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
