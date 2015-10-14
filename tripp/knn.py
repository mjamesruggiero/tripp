from collections import Counter
import algebra


def majority_vote(labels):
    """assumes that labels are ordered from nearest to farthest"""
    vote_counts = Counter(labels)
    winner, winner_count = vote_counts.most_common(1)[0]
    num_winners = len([count
                       for count in vote_counts.values()
                       if count == winner_count])
    if num_winners == 1:
        return winner
    else:
        return majority_vote(labels[:-1])


def knn_classify(k, labeled_points, new_point):
    """each labeled point should be a pair (point, label)"""
    by_distance = sorted(labeled_points,
                         key=lambda (point, _): algebra.distance(point,
                                                                 new_point))

    k_nearest_labels = [label for _, label in by_distance[:k]]

    return majority_vote(k_nearest_labels)
