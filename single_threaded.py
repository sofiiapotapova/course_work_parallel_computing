from glob import glob
from pprint import pprint as pp
import time


def single_pass_indexing(fileglob='**\*.txt'):
    terms = {}
    index = {}
    for txtfile in glob(fileglob, recursive=True):
        with open(txtfile, 'r', encoding='utf-8') as f:
            doc_id = txtfile
            text = f.read().split()
            for term in text:
                done_term = term.strip("(){}[],.!?<>:;|/")
                if done_term in terms:
                    index[done_term].append(doc_id)
                    terms[done_term] += 1
                else:
                    terms[done_term] = 1
                    index[done_term] = []
                    index[done_term].append(doc_id)
    return terms, index


def search(query, index):
    if query in index:
        pp(index[query])


if __name__ == "__main__":
    start_time = time.time()
    terms, index = single_pass_indexing()
    print(time.time() - start_time)
    print("Enter search query: (or '0' to exit): ")
    close = True
    while close:
        query = input()
        if query == "0":
            close = False
        else:
            search(query, index)