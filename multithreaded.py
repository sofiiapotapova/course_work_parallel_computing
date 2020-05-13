from glob import glob
from pprint import pprint as pp
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

terms = {}
index = {}
file_names = []
total_time = 0


def choose_file(num, max, fileglob='**\*.txt'):
    global total_time
    num_of_files = 2000
    amount = int(num_of_files/max)
    thread_files = []
    for i in range((num * amount), ((num + 1) * amount)):
        thread_files.append(file_names[i])
    for txtfile in glob(fileglob, recursive=True):
        if txtfile in thread_files:
            start_time = time.time()
            single_pass_indexing(txtfile)
            total_time += time.time() - start_time
    # print("{} ended".format(num))
    # pp(len(thread_files))



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

    for txtfile in glob('**\*.txt', recursive=True):
        with open(txtfile, 'r', encoding='utf-8') as f:
            file_names.append(txtfile)
    # start_time = time.time()
    with ThreadPoolExecutor(num_of_threads) as executor:
        future_list = []
        for i in range(num_of_threads):
            future = executor.submit(choose_file(i, num_of_threads), i, 'sh clock')
            future_list.append(future)
    for f in as_completed(future_list):
        pass
    # print(time.time() - start_time)
    print(total_time)
    pp("Enter search query: (or '0' to exit): ")
    close = True
    while close:
        query = input()
        if query == "0":
            close = False
        else:
            search(query, index)
