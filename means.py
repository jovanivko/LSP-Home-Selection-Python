import np


class WeightedPowerMean:
    def __init__(self, weights, r):
        """
        Initialize the Weighted Power Mean aggregator.
        :param weights: A list of weights for each input
        :param r: Power exponent for the mean
        """
        self.weights = np.array(weights)
        assert np.isclose(np.sum(self.weights), 1), "Weights must sum to 1."
        self.r = r

    def aggregate(self, values):
        values = np.array(values)
        return np.sum(self.weights * (values ** self.r)) ** (1 / self.r)

class CounterHarmonicMean:
    def __init__(self, weights, r):
        """
        Initialize the Counter-Harmonic Mean (CHM) aggregator.
        :param weights: A list of weights for each input
        :param r: Exponent to control the behavior between means
        """
        self.weights = np.array(weights)
        assert np.isclose(np.sum(self.weights), 1), "Weights must sum to 1."
        self.r = r

    def aggregate(self, values):
        values = np.array(values)
        numerator = np.sum(self.weights * (values ** self.r))
        denominator = np.sum(self.weights * (values ** (self.r - 1)))
        return numerator / denominator