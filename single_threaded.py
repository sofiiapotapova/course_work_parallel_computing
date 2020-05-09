from glob import glob
from pprint import pprint as pp


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


terms, index = single_pass_indexing()