import random
import algebra

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
