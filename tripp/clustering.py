import algebra
import argparse
import matplotlib.image as matimage
import matplotlib.pyplot as pyplot
import random
import logging

logging.basicConfig(level=logging.DEBUG, format="%(lineno)d\t%(message)s")


class KMeans(object):
    """performs k-means clustering"""
    def __init__(self, k):
        self.k = k
        self.means = None

    def classify(self, input):
        """return the index of the cluster closest to the input"""
        return min(range(self.k),
                   key=lambda i: algebra.squared_distance(input, self.means[i]))

    def train(self, inputs):
        """choose k random points as the initial means"""
        self.means = random.sample(inputs, self.k)
        assignments = None

        while True:
            # find new assignments
            new_assignments = map(self.classify, inputs)

            # if none have changed, we're done
            if assignments == new_assignments:
                return

            # otherwise, keep the new assignments
            assignments = new_assignments

            for i in range(self.k):
                i_points = [p for p, a in zip(inputs, assignments) if a == i]

                if i_points:
                    self.means[i] = algebra.vector_mean(i_points)


def squared_clustering_errors(inputs, k):
    """finds the total squared error from k-means clustering the inputs"""
    clusterer = KMeans(k)
    clusterer.train(inputs)
    means = clusterer.means
    assignments = map(clusterer.classify, inputs)

    return sum(algebra.squared_distance(input, means[cluster])
               for input, cluster
               in zip(inputs, assignments))


def is_leaf(cluster):
    """a cluster of a leaf if it has length 1"""
    return len(cluster) == 1


def get_children(cluster):
    """returns the two children of this cluster if it's a merged cluster;
    raises if this is a leaf cluster"""
    if is_leaf(cluster):
        raise TypeError("a leaf cluster has no children")
    else:
        return cluster[1]


def get_values(cluster):
    """returns the value in this cluster (if it's a leaf cluster)
    or all the values in the leaf clusters below (if it's not)"""
    if is_leaf(cluster):
        return cluster
    else:
        return [value
                for child in get_children(cluster)
                for value in get_values(child)]


def cluster_distance(cluster1, cluster2, distance_agg=min):
    """compute all the pairwise distances between cluster1 and cluster2
    and apply distance_agg to the resulting list"""
    return distance_agg([algebra.distance(input1, input2)
                         for input1 in get_values(cluster1)
                         for input2 in get_values(cluster2)])


def merge_order(cluster):
    if is_leaf(cluster):
        return float('inf')
    else:
        return cluster[0]  # merge_order is the first element of 2-tuple


def bottom_up_cluster(inputs, distance_agg=min):
    # start with every input in a leaf cluster / 1-tuple
    clusters = [(input,) for input in inputs]

    # as long as we have more than one cluster left ...
    while(len(clusters)) > 1:
        c1, c2 = min([(cluster1, cluster2)
                      for i, cluster1 in enumerate(clusters)
                      for cluster2 in clusters[:i]],
                     key=lambda (x, y): cluster_distance(x, y, distance_agg))

        # remove them from the list of clusters
        clusters = [c for c in clusters if c != c1 and c != c2]

        # merge them, using merge_order = # clusters left
        merged_cluster = (len(clusters), [c1, c2])

        # and add their merge
        clusters.append(merged_cluster)

    return clusters[0]


def generate_clusters(base_cluster, num_clusters):
    """generates any number of clusters
    by performing the appropriate number of unmerges"""
    clusters = [base_cluster]

    while len(clusters) < num_clusters:
        # choose the last-merged of our clusters
        next_cluster = min(clusters, key=merge_order)
        # remove it from the list
        clusters = [c for c in clusters if c != next_cluster]
        # add its cildren to the list (or un-merge it)
        clusters.extend(get_children(next_cluster))

    return clusters

def example_clustering():
    three_clusters = [get_values(c)
                      for c in generate_clusters(base_cluster, 3)]


def decolor(asset, target_asset="/tmp/new-image.png"):
    """De-color PNG assets to a 5-color analog"""
    img = matimage.imread(asset)

    top_row = img[0]
    top_left_pixel = top_row[0]

    logging.info("destructuring the top left pixel")
    red, green, blue = top_left_pixel

    logging.info("about to read pixels")
    pixels = [pixel for row in img for pixel in row]
    clusterer = KMeans(5)

    logging.info("training... might take a while...")
    clusterer.train(pixels)

    def recolor(pixel):
        """map index of closest cluster to its mean"""
        cluster = clusterer.classify(pixel)
        return clusterer.means[cluster]

    new_img = [[recolor(pixel) for pixel in row] for row in img]

    logging.info("displaying image")

    pyplot.imshow(new_img)
    pyplot.axis('off')
    pyplot.savefig(target_asset)


if __name__ == '__main__':

    DESCRIPTION = 'Converts PNG to five colors'
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument('png', action="store")
    parser.add_argument('destination_asset', action="store")

    results = parser.parse_args()
    path_to_png = results.png
    destination_asset = results.destination_asset

    decolor(path_to_png, destination_asset)
