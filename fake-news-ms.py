'''
File: fake-news-ms.py
Author: Justin Nichols
Purpose: Finds the most frequent words in the headlines of articles.
         Organizes them primarily by count (descending order), secondarily by
             increasing lexicographical order.
         Prints out the n-most-frequent, where n is determined by user input.
CSC120, Section 1, Fall 18
'''


import sys
import csv
import string


HEADLINE_INDEX = 4
TRIVIAL_WORD_LENGTH = 2

def clean_headlines_update_counts(infile_it_obj, counts):
    '''
    Purpose: finds all the words in all the headlines (sans punctuation) and
                 makes word-objs that will keep track of the frequency with
                 which they all occur
    Parameters: infile_it_obj, an iterable-obj. The first item contains
                    formatting info. The rest contain info about articles
                    in the dataset
                counts, a list. Starts out empty, but will contain one word-obj
                    for each word found in any headline in the dataset
    Returns: n/a
    Pre-Conditions: n/a
    Post-Conditions: 'counts' is as described above
    '''
    headlines_list = []

    # getting rid of first line in file, which contains no information about
    #     any article
    infile_list_form = list(infile_it_obj)
    del infile_list_form[0]

    
    # iterating over the headlines of each article
    for article_info_list in infile_list_form:
        headline = article_info_list[HEADLINE_INDEX]
        # replacing punctuation in current headline with whitespace
        headline_no_punc = ''
        for character in headline:
            if character not in string.punctuation:
                headline_no_punc += character
            else:
                headline_no_punc += ' '
        headline_words = headline_no_punc.lower().split()
        for word in headline_words:
            if len(word) > TRIVIAL_WORD_LENGTH:
                update_count(counts, word)


def update_count(counts, word):
    '''
    Purpose: Creates word-objs as necessary.
             Keeps the count-attribute of each word-obj current.
    Parameters: count, a list. Contains word-objs corresponding to words found
                    in at least one headline in the dataset
                word, a str. The word whose count is being updated
    Returns: n/a
    Pre-Conditions: n/a
    Post-Conditions: either a word-obj has been creatd or an existing one has
                         had its 'count' attribute updated
    '''
    word_in_list = False
    for word_obj in counts:
        if word_obj.word() == word:
            word_in_list = True
            word_obj.incr()
            return

    counts.append(Word(word))
    

class Word:
    '''
    Purpose: stores and provides access to info about a word that appeared in
                 at least one headline in the dataset
    Parameters: word, a str. The word described above
    Returns: n/a
    Pre-Conditions: n/a
    Post-Conditions: n/a
    '''
    def __init__(self, word):
        self._word = word
        self._count = 1

    # getters
    def word(self):
        return self._word

    def count(self):
        return self._count

    # setters
    def incr(self):
        self._count += 1

    # special methods
    def __str__(self):
        return self._word

    def __lt__(self, other):
        '''
        Purpose: makes 'self < other' true iff 'self' precedes 'other' in the
                     final list
        Parameter: other, a word-obj. The word-obj being compared against this
                       one
        '''
        return (self.count() > other.count()) or \
               (self.count() == other.count() and self.word() < other.word())


# DISCLAIMER: THIS FUNCTION WAS TAKEN FROM THE SLIDES
# I DID NOT WRITE THIS FUNCTION
def merge(L1, L2, merged):
    '''
    Purpose: recursively merges two pre-sorted lists onto a third
    Parameters: L1, the first list.
                L2, the second list.
                merged, the third list.
    Returns: a recursive call to merge (with changed parameters)
    Pre-Conditions: lists must be pre-sorted
    Post-Conditions: the list ultimately returned will be sorted and will
                         contain all elements of all component-lists
                         (counting multiplicities)
    '''
    # base-case
    if L1 == [] or L2 == []:
        return merged + L1 + L2

    # recursive case
    if L1[0] < L2[0]:
        merged += [L1[0]]
        new_L1 = L1[1:]
        new_L2 = L2
    else:
        merged += [L2[0]]
        new_L1 = L1
        new_L2 = L2[1:]
    return merge(new_L1, new_L2, merged)


# DISCLAIMER: THIS FUNCTION WAS ADAPTED FROM THE SLIDES
# I DID NOT WRITE THIS FUNCTION
def msort(L):
    '''
    Purpose: this is a merge-sort algorithm. Recusrively splits the list L down
                 into single elements and then recursively merges then back
                 together (but now in sorted order)
    Parameters: L, a list. The list to be sorted.
    Returns: A sorted version of L
    Pre-Conditions: n/a
    Post-Conditions: return-value is as described above
    '''
    # base-case
    if len(L) <= 1:
        return L

    # recursive case
    split_pt = len(L) // 2
    L1 = L[:split_pt]
    L2 = L[split_pt:]
    return merge(msort(L1), msort(L2), [])

        
def get_k(ordered_counts, n):
    '''
    Purpose: gets the count of the word at index n in the sorted list
    Parameters: ordered_counts, a list. Contains word-objs, sorted first by
                    count (descending) and then by name (ascending)
                n, an int. The index mentioned above
    Returns: the count of the word at index n in ordered_counts
    Pre-Conditions: ordered_counts is as described above.
                        n is nonnegtive (failure to meet this condition will result
                        in an assertion-error)
    Post-Conditions: n/a
    '''
    assert n >= 0

    if len(ordered_counts) <= n:
        return 0

    nth_word_obj = ordered_counts[n]
    return nth_word_obj.count()


def print_upto_k(ordered_counts, k):
    '''
    Purpose: prints all words with frequency larger than (or equal to) k
    Parameters: ordered_counts, a list. Contains word-objs, sorted first by
                    count (descending) and then by name (ascending)
                k, an int. The count of the word at the cutoff-index in the
                    list
    Returns: n/a
    Pre-Conditions: ordered_counts is ordered
    Post-Conditions; n/a
    '''
    if k!= 0:
        i = 0
        while ordered_counts[i].count() >= k:
            word_obj = ordered_counts[i]
            print("{} : {:d}".format(word_obj.word(),
            word_obj.count()))
            i += 1
    

def main():
    sys.setrecursionlimit(2500)
    
    # getting and parsing the csv-file
    infile_name = input('File: ')
    try:
        infile_it_obj = open(infile_name)
    except FileNotFoundError:
        print("ERROR: Could not open file " + infile_name)
        sys.exit(1)
    infile_it_obj = csv.reader(infile_it_obj)
    
    # obtaining counts for each word and sorting accordingly
    counts = []
    clean_headlines_update_counts(infile_it_obj, counts)
    ordered_counts = msort(counts)  

    # getting the value for n
    n_name = input('N:')
    try:
        n = int(n_name)
    except ValueError:
        print('ERROR: Could not read N')
        sys.exit(1)

    # getting ready to print, and then printing
    k = get_k(ordered_counts, n)
    print_upto_k(ordered_counts, k)


main()
