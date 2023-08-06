class ElasticObject(dict):
    """
    This class allows you to create objects with custom members on the fly
    """

    def __getattr__(self, item):
        try:
            # Throws exception if not in prototype chain
            return object.__getattribute__(self, item)
        except AttributeError:
            try:
                return self[item]
            except KeyError:
                raise AttributeError(f"'{ElasticObject.__name__}' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, key)
        except AttributeError:
            try:
                self[key] = value
            except Exception:
                raise AttributeError(f"'{ElasticObject.__name__}' object has no attribute '{key}'")
        else:
            object.__setattr__(self, key, value)
