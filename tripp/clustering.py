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

if __name__ == '__main__':

    DESCRIPTION = 'Converts PNG to five colors'
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument('png', action="store")

    results = parser.parse_args()
    path_to_png = results.png

    img = matimage.imread(path_to_png)

    top_row = img[0]
    top_left_pixel = top_row[0]
    red, green, blue, _ = top_left_pixel

    pixels = [pixel for row in img for pixel in row]
    clusterer = KMeans(5)
    clusterer.train(pixels)

    def recolor(pixel):
        """map index of closest cluster to its mean"""
        cluster = clusterer.classify(pixel)
        return clusterer.means[cluster]

    new_img = [[recolor(pixel) for pixel in row] for row in img]

    logging.info("displaying image")

    pyplot.imshow(new_img)
    pyplot.axis('off')
    pyplot.show()
