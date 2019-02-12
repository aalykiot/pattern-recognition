from random import shuffle
from scipy.spatial import distance
from .utils import mode_f


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
