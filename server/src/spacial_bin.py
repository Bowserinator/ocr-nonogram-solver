"""
Dictionary but similar keys are mapped
to the same value
"""
class SpacialBin(object):
    def __init__(self, tolerance):
        """
        Construct a spacial bin
        :param tolerance: Tolerance for keys, keys
                          within this value are mapped to the same slot
        """
        self.dict = {}
        self.keys = set()
        self.tolerance = tolerance

    def _mapkey(self, key):
        """
        Set key to the nearest key within tolerance, or just
        the key itself
        :param key:
        :return: Mapped key
        """
        for k in self.keys:
            if abs(k - key) <= self.tolerance:
                return k
        return key

    def haskey(self, key):
        """
        Does the key exist in the set?
        :param key:
        :return: bool
        """
        key = self._mapkey(key)
        return key in self.keys

    def add(self, key, val):
        """
        :param key: Key to add to
        :param val: Value to add
        """
        key = self._mapkey(key)
        self.keys.add(key)
        self.dict[key] = val

    def get(self, key, default = None):
        """
        Get a dict value by key, defaults to default
        if key doesn't exist
        :param key:
        :return: dict item
        """
        key = self._mapkey(key)
        return self.dict.get(key, default)

    def set(self, key, val):
        """
        Set a dict value by key
        :param key:
        :param val:
        """
        key = self._mapkey(key)
        self.keys.add(key)
        self.dict[key] = val

    def to_list(self):
        """
        Convert to sorted array sorted by key
        :return: this list
        """
        return [x[1] for x in sorted(self.dict.items(), key=lambda x: x[0])]
