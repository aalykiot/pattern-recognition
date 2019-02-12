from random import shuffle
from scipy.spatial import distance
from sklearn.cluster import KMeans, AgglomerativeClustering


class Bsas():

    def calculate_theta(self, theta_min, theta_max, vectors):
        print("theta_min: " + str(theta_min))
        print("theta_max: " + str(theta_max))
        step = 0.1
        S = 5

        theta_results = []
        cluster_groups = []

        theta_current = theta_min

        while theta_current <= theta_max:

            inner_cluster_groups = []

            for i in range(S):
                shuffle(vectors)
                inner_cluster_groups.append(len(self.find_clusters(
                    vectors, theta_current, len(vectors))))

            theta_results.append(theta_current)
            cluster_groups.append(mode_f(inner_cluster_groups))

            theta_current += step

        # Find best theta
        common = mode_f(cluster_groups)
        index = cluster_groups.index(common)

        return theta_results[index], common

    def find_clusters(self, vectors, theta, max_clusters):
        clusters = [[vectors[0]]]

        for vector in vectors[1:]:

            # Calculating the distances from each cluster
            dist = []
            for cluster in clusters:
                sub_dist = [
                    distance.euclidean(vector, c_vec) for c_vec in cluster
                ]

                dist.append(min(sub_dist))

            # Finding the smallest one
            min_dist = min(dist)

            # Getting the index of the selected cluster
            index = dist.index(min(dist))

            if min_dist > theta and len(clusters) < max_clusters:
                # Create new cluster
                clusters.append([vector])
            else:
                # Append vector to cluster
                clusters[index].append(vector)

        return clusters


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


def create_users_vectors(ratings_data, users_data, movies_data):
    # print("Creating vectors...")
    # Creating user vectors initialized with 0
    users_vectors = [[[0, 0] for x in range(0, 19)]
                     for y in range(0, len(users_data))]

    for rating in ratings_data:

        movie = movies_data[int(rating[1]) - 1][5:]

        for index, genre in enumerate(movie):
            if genre is "1":
                users_vectors[int(rating[0]) - 1][index][0] += int(rating[2])
                users_vectors[int(rating[0]) - 1][index][1] += 1

    # Finding the avg value of rating per movie genre per user
    for vector in users_vectors:
        for index, elem in enumerate(vector):
            if elem[1] is 0:
                elem = 0
            else:
                elem = round(elem[0] / elem[1])
            vector[index] = elem

    return users_vectors


def find_min_max_distances(vectors):
    print("Finding min,max distances...")
    dist = []

    # Finding the min,max euclidian distances of the vectors
    for i in range(len(vectors)):
        for j in range(i+1, len(vectors)):
            dist.append(distance.euclidean(vectors[i], vectors[j]))
    return min(dist), max(dist)


def print_clusters(title, clusters):
    print('\n' + "<------ " + title + " ------>")
    print("\n==> total clusters: " + str(len(clusters)))
    for index, cluster in enumerate(clusters):
        print("\n==> cluster no. " + str(index))
        print("==> cluster size: " + str(len(cluster)) + " vectors")
        print("==> cluster vectors: " + str(cluster))


# ====== Question 1 ======

ratings = load("data/u.data", "\t")
users = load("data/u.user", "|")
movies = load("data/u.item", "|")

vectors = create_users_vectors(ratings, users, movies)
# vectors = [[1, 1], [2, 1], [100, 105], [102, 100]]  # Testing vectors


# ====== Question 2 ======

min_distance, max_distance = find_min_max_distances(vectors)

# Calculating theta upper and lower limits from formula
theta_min = min_distance + 0.25 * (max_distance - min_distance)
theta_max = min_distance + 0.75 * (max_distance - min_distance)

best_theta, max_clusters = Bsas().calculate_theta(theta_min, theta_max, vectors)

b_clusters = Bsas().find_clusters(vectors, best_theta, max_clusters)

print_clusters("Bsas clustering", b_clusters)


# ====== Question 3 ======

# K-means clustering
kmeans = KMeans(n_clusters=max_clusters, random_state=0).fit(vectors)

k_clusters = [[] for i in range(max_clusters)]

for i in range(len(vectors)):
    k_clusters[kmeans.labels_[i]].append(vectors[i])

print_clusters("K-means clustering", k_clusters)


# Hierarchical clustering
hierarchical = AgglomerativeClustering(n_clusters=max_clusters).fit(vectors)

h_clusters = [[] for i in range(max_clusters)]

for i in range(len(vectors)):
    h_clusters[hierarchical.labels_[i]].append(vectors[i])

print_clusters("Hierarchical clustering", h_clusters)
