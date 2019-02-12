def mode_f(L):
    counter = 0
    number = L[0]
    for i in L:
        amount_times = L.count(i)
        if amount_times > counter:
            counter = amount_times
            number = i

    return number


def load(path, seperator):
    # print("Loading data...")
    file_data = open(path, "r", encoding="ISO-8859-1").read().split("\n")
    normalized_data = []

    # Seperate data according to seperator
    for row in file_data:
        if row != "":
            normalized_data.append(row.split(seperator))

    return normalized_data


def print_clusters(title, clusters):
    print('\n' + "<------ " + title + " ------>")
    print("\n==> total clusters: " + str(len(clusters)))
    for index, cluster in enumerate(clusters):
        print("\n==> cluster no. " + str(index))
        print("==> cluster size: " + str(len(cluster)) + " vectors")
        print("==> cluster vectors: " + str(cluster))
