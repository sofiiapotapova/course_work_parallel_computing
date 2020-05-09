from glob import glob


def single_pass_indexing(fileglob='**\*.txt'):
    terms = []
    index = {}
    for txtfile in glob(fileglob, recursive=True):
        with open(txtfile, 'r', encoding='utf-8') as f:
            doc_id = txtfile
            text = f.read().split()
            for term in text:
                if term in terms:
                    index[term].append(doc_id)
                else:
                    terms.append(term)
                    index[term] = []
                    index[term].append(doc_id)
    return index


final = single_pass_indexing()