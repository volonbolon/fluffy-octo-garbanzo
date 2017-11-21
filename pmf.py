import logging
import math
import random
import operator

class _DictWrapper(object):
    """An object that contains a dictionary."""

    def __init__(self, d=None, name=''):
        # if d is provided, use it; otherwise make a new dict
        if d == None:
            d = {}
        self.d = d
        self.name = name

    def get_dict(self):
        """Gets the dictionary."""
        return self.d

    def values(self):
        """Gets an unsorted sequence of values.

        Note: one source of confusion is that the keys in this
        dictionaries are the values of the Hist/Pmf, and the
        values are frequencies/probabilities.
        """
        return self.d.keys()

    def items(self):
        """Gets an unsorted sequence of (value, freq/prob) pairs."""
        return self.d.items()

    def render(self):
        """Generates a sequence of points suitable for plotting.

        Returns:
            tuple of (sorted value sequence, freq/prob sequence)
        """
        return zip(*sorted(self.items()))

    def print(self):
        """Prints the values and freqs/probs in ascending order."""
        for val, prob in sorted(self.d.iteritems()):
            print
            val, prob

    def set(self, x, y=0):
        """Sets the freq/prob associated with the value x.

        Args:
            x: number value
            y: number freq or prob
        """
        self.d[x] = y

    def incr(self, x, term=1):
        """Increments the freq/prob associated with the value x.

        Args:
            x: number value
            term: how much to increment by
        """
        self.d[x] = self.d.get(x, 0) + term

    def mult(self, x, factor):
        """Scales the freq/prob associated with the value x.

        Args:
            x: number value
            factor: how much to multiply by
        """
        self.d[x] = self.d.get(x, 0) * factor

    def remove(self, x):
        """Removes a value.

        Throws an exception if the value is not there.

        Args:
            x: value to remove
        """
        del self.d[x]

    def total(self):
        """Returns the total of the frequencies/probabilities in the map."""
        total = sum(self.d.itervalues())
        return total

    def max_like(self):
        """Returns the largest frequency/probability in the map."""
        return max(self.d.itervalues())


class Histogram(_DictWrapper):
    """Represents a histogram, which is a map from values to frequencies.

    Values can be any hashable type; frequencies are integer counters.
    """

    def copy(self, name=None):
        """Returns a copy of this Hist.

        Args:
            name: string name for the new Hist
        """
        if name is None:
            name = self.name
        return Histogram(dict(self.d), name)

    def freq(self, x):
        """Gets the frequency associated with the value x.

        Args:
            x: number value

        Returns:
            int frequency
        """
        return self.d.get(x, 0)

    def freqs(self):
        """Gets an unsorted sequence of frequencies."""
        return self.d.values()

    def is_subset(self, other):
        """Checks whether the values in this histogram are a subset of
        the values in the given histogram."""
        for val, freq in self.items():
            if freq > other.freq(val):
                return False
        return True

    def subtract(self, other):
        """Subtracts the values in the given histogram from this histogram."""
        for val, freq in other.items():
            self.incr(val, -freq)

    def mode(self):
        mode, max_freq = 0, 0
        for val, freq in self.items():
            if freq > max_freq:
                max_freq = freq
                mode = val
        return mode

    def all_modes(self):
        s = self.items()
        sorted_freqs = sorted(self.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_freqs


class PMF(_DictWrapper):
    """Represents a probability mass function.

    Values can be any hashable type; probabilities are floating-point.
    Pmfs are not necessarily normalized.
    """

    def copy(self, name=None):
        """Returns a copy of this Pmf.

        Args:
            name: string name for the new Pmf
        """
        if name is None:
            name = self.name
        return PMF(dict(self.d), name)

    def prob(self, x, default=0):
        """Gets the probability associated with the value x.

        Args:
            x: number value
            default: value to return if the key is not there

        Returns:
            float probability
        """
        return self.d.get(x, default)

    def probs(self):
        """Gets an unsorted sequence of probabilities."""
        return self.d.values()

    def normalize(self, fraction=1.0):
        """Normalizes this PMF so the sum of all probs is 1.

        Args:
            fraction: what the total should be after normalization
        """
        total = self.total()
        if total == 0.0:
            raise ValueError('total probability is zero.')
            logging.warning('Normalize: total probability is zero.')
            return

        factor = float(fraction) / total
        for x in self.d:
            self.d[x] *= factor

    def random(self):
        """Chooses a random element from this PMF.

        Returns:
            float value from the Pmf
        """
        if len(self.d) == 0:
            raise ValueError('Pmf contains no values.')

        target = random.random()
        total = 0.0
        for x, p in self.d.iteritems():
            total += p
            if total >= target:
                return x

        # we shouldn't get here
        assert False

    def mean(self):
        """Computes the mean of a PMF.

        Returns:
            float mean
        """
        mu = 0.0
        for x, p in self.d.iteritems():
            mu += p * x
        return mu

    def var(self, mu=None):
        """Computes the variance of a PMF.

        Args:
            mu: the point around which the variance is computed;
                if omitted, computes the mean

        Returns:
            float variance
        """
        if mu is None:
            mu = self.mean()

        var = 0.0
        for x, p in self.d.iteritems():
            var += p * (x - mu) ** 2
        return var

    def log(self):
        """Log transforms the probabilities."""
        m = self.max_like()
        for x, p in self.d.iteritems():
            self.set(x, math.log(p / m))

    def exp(self):
        """Exponentiates the probabilities."""
        m = self.max_like()
        for x, p in self.d.iteritems():
            self.set(x, math.exp(p - m))


def make_hist_from_list(t, name=''):
    """Makes a histogram from an unsorted sequence of values.

    Args:
        t: sequence of numbers
        name: string name for this histogram

    Returns:
        Hist object
    """
    hist = Histogram(name=name)
    [hist.incr(x) for x in t]
    return hist


def make_hist_from_dict(d, name=''):
    """Makes a histogram from a map from values to frequencies.

    Args:
        d: dictionary that maps values to frequencies
        name: string name for this histogram

    Returns:
        Hist object
    """
    return Histogram(d, name)


def make_PMF_from_list(t, name=''):
    """Makes a PMF from an unsorted sequence of values.

    Args:
        t: sequence of numbers
        name: string name for this PMF

    Returns:
        Pmf object
    """
    hist = make_hist_from_list(t, name)
    return make_PMF_from_hist(hist)


def make_PMF_from_dict(d, name=''):
    """Makes a PMF from a map from values to probabilities.

    Args:
        d: dictionary that maps values to probabilities
        name: string name for this PMF

    Returns:
        Pmf object
    """
    pmf = PMF(d, name)
    pmf.normalize()
    return pmf


def make_PMF_from_hist(hist, name=None):
    """Makes a normalized PMF from a Hist object.

    Args:
        hist: Hist object
        name: string name

    Returns:
        Pmf object
    """
    if name is None:
        name = hist.name

    # make a copy of the dictionary
    d = dict(hist.get_dict())
    pmf = PMF(d, name)
    pmf.normalize()
    return pmf


def make_PMF_from_Cdf(cdf, name=None):
    """Makes a normalized Pmf from a Cdf object.

    Args:
        cdf: Cdf object
        name: string name for the new Pmf

    Returns:
        Pmf object
    """
    if name is None:
        name = cdf.name

    pmf = PMF(name=name)

    prev = 0.0
    for val, prob in cdf.items():
        pmf.incr(val, prob - prev)
        prev = prob

    return pmf


def make_mixture(pmfs, name='mix'):
    """Make a mixture distribution.

    Args:
      pmfs: Pmf that maps from Pmfs to probs.
      name: string name for the new Pmf.

    Returns: Pmf object.
    """
    mix = PMF(name=name)
    for pmf, prob in pmfs.items():
        for x, p in pmf.items():
            mix.incr(x, p * prob)
    return mix