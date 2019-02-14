from random import shuffle
from scipy.spatial import distance
from sklearn.cluster import KMeans, AgglomerativeClustering

from mylib.utils import load, print_clusters
from mylib.bsas import Bsas


def create_users_vectors(ratings_data, users_data, movies_data):
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
    dist = []

    # Finding the min,max euclidian distances of the vectors
    for i in range(len(vectors)):
        for j in range(i+1, len(vectors)):
            dist.append(distance.euclidean(vectors[i], vectors[j]))
    return min(dist), max(dist)


# ====== Question 1 ======

print("\n==> Loading data...")
ratings = load("data/u.data", "\t")
users = load("data/u.user", "|")
movies = load("data/u.item", "|")

print("\n==> Creating vectors...")
#vectors = create_users_vectors(ratings, users, movies)
vectors = [[1, 1], [2, 1], [100, 105], [102, 100]]  # Test vectors


# ====== Question 2 ======

print("\n==> Finding min,max distances...")
min_distance, max_distance = find_min_max_distances(vectors)

print("\n==> Calculating theta...")
# Calculating theta upper and lower limits from formula
theta_min = min_distance + 0.25 * (max_distance - min_distance)
theta_max = min_distance + 0.75 * (max_distance - min_distance)

best_theta, max_clusters = Bsas().calculate_theta(theta_min, theta_max, vectors)

print("\n==> Running bsas algorithm...")
b_clusters = Bsas().find_clusters(vectors, best_theta, max_clusters)

print_clusters("Bsas clustering", b_clusters)


# ====== Question 3 ======

# K-means clustering
print("\n==> Running K-means algorithm...")
kmeans = KMeans(n_clusters=max_clusters, random_state=0).fit(vectors)

k_clusters = [[] for i in range(max_clusters)]

for i in range(len(vectors)):
    k_clusters[kmeans.labels_[i]].append(vectors[i])

print_clusters("K-means clustering", k_clusters)


# Hierarchical clustering
print("\n==> Running hierarchical algorithm...")
hierarchical = AgglomerativeClustering(n_clusters=max_clusters).fit(vectors)

h_clusters = [[] for i in range(max_clusters)]

for i in range(len(vectors)):
    h_clusters[hierarchical.labels_[i]].append(vectors[i])

print_clusters("Hierarchical clustering", h_clusters)
