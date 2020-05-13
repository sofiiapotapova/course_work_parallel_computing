from glob import glob
from pprint import pprint as pp
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

terms = {}
index = {}
file_names = []


def choose_file(num, max, fileglob='**\*.txt'):
    num_of_files = 2000
    amount = int(num_of_files/max)
    thread_files = []
    for i in range((num * amount), ((num + 1) * amount)):
        thread_files.append(file_names[i])
    for txtfile in glob(fileglob, recursive=True):
        if txtfile in thread_files:
            single_pass_indexing(txtfile)
    print("{} ended".format(num))
    pp(len(thread_files))


def single_pass_indexing(txtfile):
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

    num_of_threads = int(input("Enter number of threads you want: "))
    start_time = time.time()
    for txtfile in glob('**\*.txt', recursive=True):
        with open(txtfile, 'r', encoding='utf-8') as f:
            file_names.append(txtfile)

    with ThreadPoolExecutor(num_of_threads) as executor:
        for i in range(num_of_threads):
            executor.submit(choose_file(i, num_of_threads), i)
    print(time.time() - start_time)
    pp("Enter search query: (or '0' to exit): ")
    close = True
    while close:
        query = input()
        if query == "0":
            close = False
        else:
            search(query, index)
