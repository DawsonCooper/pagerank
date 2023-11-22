import os
import random
import re
import sys
import numpy as numpy

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

    if len(currentPageLinks) == 0:
        for page in corpus:
            distribution[page] = 1 / len(corpus)
        return distribution
    
    # calculate the base probability for each page in the corpus being chosen completly at random after the damping factor is applied and divided evenly among all pages in the corpus
    for page in corpus:
        distribution[page] = (1 - damping_factor) / len(corpus)
        
    # for each page that is linked by current add the probability of being chosen at random to the distribution of all pages being chosen
    for page in currentPageLinks:
        evenDistribution = damping_factor / len(currentPageLinks)
        distribution[page] += evenDistribution
    
    print(distribution)
    """
    
    distribution = {
        pageKey: probability(.15),
        pageKey: probability(.10),
        pageKey: probability(.50),
        pageKey: probability(.25),
    }
    
    this will be the probability distribution for the current page passed into the function
    
    """
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
    result = {}
    # get random page 
    currPage = random.choice(list(corpus.keys()))
    
    
    
    probDist = {}
    
    # Get the probability distribution for each of the pages in the courpus and store it in a dictionary so we dont need to calc during sample loop
    for page in corpus:
        # get the probability distribution of each page in the corpus
        probDist[page] = transition_model(corpus, page, damping_factor)
        # fill result with a key for each page
        result[page] = 0
    
    """
    {
        page1: {pageKey: probability, pageKey: probability, pageKey: probability, pageKey: probability, ...},
        page2: {pageKey: probability, pageKey: probability, pageKey: probability, pageKey: probability, ...},
        
        
    }
    """
    
    for pageDist in probDist:
        # this will create a set of list for each page one will represent the possible pages to go to and one will represent the probability of going to that page
        pages = []
        probs = []
        for link in pageDist:
            pages.append(link)
            probs.append(pageDist[link])
        
        # reset the probability distrubution for each page to be a set where set[0] = possible pages and set[1] = probability of going to that page
        pageDist = (pages, probs)
    
    
    # sample loop that uses numpy to choose our next page based on a list of possible pages and a list of weighted probabilities
    for i in range(n):
        
        
        # increase the visit count of the current page by 1/n 
        result[currPage] += 1 / n
        # choose the next page based on the probability distribution of the current page
        currPage = numpy.random.choice(probDist[currPage][0], None, True, probDist[currPage][1])
    

    return result


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    distribution = {}
    # set default PR for each page into the distribution dictionary (base probability based on the change a page will be randomly chosen from corpus) 
    for page in corpus:
        distribution[page] = 1 - damping_factor / len(corpus)

    # dict of pages and the pages that link to that page opposite of the corpus
    linkDist = {}
    

        
    # loop over the corpus and for each page give it a list of pages that link to it length of that list will give us the numPages
    for page in corpus:
        for link in page:
            try:
                linkDist[link].add(page)
            except KeyError:
                # if there is no key for the link we are checking create a new key for it and add the page that links to it
                linkDist[link] = set([page])
    
    """
    
    """
    
    for page in linkDist:
        sumation = 0
        prI = 0
        for link in linkDist[page]:
            # prI = the curr pageRank of link / the number of links on that page
            prI = distribution[link]
            prI /= len(linkDist[link])  
            sumation += prI
        distribution[page] += damping_factor * sumation
    return distribution 

if __name__ == "__main__":
    main()
