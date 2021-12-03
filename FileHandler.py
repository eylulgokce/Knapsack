import shutil
import sys
from os import path
import requests


def download_all_datasets():
    url = "https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/"

    file_names = get_file_names()

    if check_all_files_exist(file_names):
        print("We already have all Files! There is nothing to download!")
        return

    # Download all file names from given URL
    for file_name in file_names:
        with open(file_name, "wb") as f:
            print("\nDownloading " + file_name)
            response = requests.get(url + file_name, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    # printing progress of download
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
        try:
            # Moving all downloaded files into Files folder
            shutil.move(file_name, "Files")
        finally:
            print("\nFiles moved!")

    # Check if we got all files from web
    check_all_files_exist(file_names)

    print("\nWe have all Files!")


def check_all_files_exist(file_names):
    to_download = True
    for file in file_names:
        if not (path.exists(path.join("C:/Users/eylul/PycharmProjects/knapsack/Files", file))):
            print("Missing File found!: ", file)
            to_download = False
    return to_download


def get_file_names():
    file_names = []

    for problem in range(1, 9):
        for file_type in ["c", "w", "p", "s"]:
            file_names.append(("p0" + str(problem) + "_" + file_type + ".txt"))

    return file_names


def read_files(problem_number):
    # First we download all datasets from Web page
    download_all_datasets()

    # Get files for specific problem with the file names in ascending order
    file_names = sorted(list(filter(lambda file: str(problem_number) in file, get_file_names())))

    knapsack_max_capacity = 0
    capacity_file = open(path.join("Files", file_names[0]), 'r', encoding="utf-8")
    for line in capacity_file.readlines():
        knapsack_max_capacity = int(line)

    # List of all values
    values = []
    weight_file = open(path.join("Files", file_names[1]), 'r', encoding="utf-8")
    for line in weight_file.readlines():
        values.append(int(line))

    # List of all weights
    weights = []
    weight_file = open(path.join("Files", file_names[3]), 'r', encoding="utf-8")
    for line in weight_file.readlines():
        weights.append(int(line))

    num_of_items = len(weights)

    return values, weights, knapsack_max_capacity, num_of_items
