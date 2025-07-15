import os 


def index_files(directory):
    for root, dirs, files in os.walk(directory, topdown=True):
        for file in files:
            print(file)

index_files("context_search_test")