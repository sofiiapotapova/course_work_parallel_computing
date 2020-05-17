from glob import glob
from pprint import pprint as pp
import time
from threading import Lock, Thread

terms = {}
index = {}
file_names = []
lock = Lock()


# def choose_file(num, max, fileglob='**\*.txt'):
#     global total_time
#     num_of_files = 2000
#     amount = int(num_of_files/max)
#     thread_files = []
#     for i in range((num * amount), ((num + 1) * amount)):
#         thread_files.append(file_names[i])
#     for txtfile in glob(fileglob, recursive=True):
#         if txtfile in thread_files:
#             start_time = time.time()
#             single_pass_indexing(txtfile, num)
#             total_time += time.time() - start_time


def single_pass_indexing(txtlist, num):
    for txtfile in txtlist:
        with open(txtfile, 'r', encoding='utf-8') as f:
            # print(num)
            doc_id = txtfile
            text = f.read().split()
            for term in text:
                done_term = term.strip("(){}[],.!?<>:;|/")
                if done_term in terms:
                    with lock:
                        index[done_term].append(doc_id)
                        terms[done_term] += 1
                else:
                    with lock:
                        terms[done_term] = 1
                        index[done_term] = []
                        index[done_term].append(doc_id)
    return terms, index


def search(query, index):
    if query in index:
        pp(index[query])


if __name__ == "__main__":
    num_of_threads = int(input("Enter number of threads you want: "))
    num_of_files = 2000
    amount = int(num_of_files / num_of_threads)

    procs = []
    for txtfile in glob('**\*.txt', recursive=True):
        with open(txtfile, 'r', encoding='utf-8') as f:
            file_names.append(txtfile)

    start = time.time()
    for i in range(num_of_threads):
        p = Thread(target=single_pass_indexing, args=(file_names[(i * amount):((i + 1) * amount)], i))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()
    total = time.time() - start

    print(total)

    print("Enter search query: (or '0' to exit): ")
    close = True
    while close:
        query = input()
        if query == "0":
            close = False
        else:
            search(query, index)

