import pickle

from constants import MODELSAVE_VERSION

MSV_KEY = "modelsave_version"
ATR_KEY = "attributes"


class ModelBase:
    minimal_attributes = None  # define within subclasses

    def get_minimal_representation(self):
        """
        Returns the dictionary of key:value pairs that encodes what a given model instance says is its minimal
        attributes.  Primarily used for model load.

        The class's self.minimal_attributes is the core mechanism that lets us ensure modelsave
        compatability across versions by letting us explicitly control what is saved.
        """
        attributes = {}
        for attr_key in self.minimal_attributes:
            attr_val = getattr(self, attr_key)
            attributes[attr_key] = attr_val
        return attributes

    @classmethod
    def init_with_minimal_representation(cls, attributes: dict):
        """Fully override the inner state of this class instance with the given attributes.  Primarily used for model
        laod from file.


        Parameters
        ----------
        attributes : dict
            dictionary of attributes to load into model.

        Returns
        -------
        ModelBase
        """
        model = cls()  # let defaults be whatever.
        for k, v in attributes.items():  # overwrite internal state
            setattr(model, k, v)
        return model

    def save(self, filename):
        """Save the current model into a file.

        We wrap python's pickle to allow us to internally specify the exact members saved.  That way, we can provide
        support for using a modelsave generated in one curators version in another version by abstracting a
        higher unit of versioning MODELSAVE_VERSION.

        Parameters
        ----------
        filename : str
            filename at which to save the current model.
        """
        # TODO: add "overwrite" flag?

        attributes = self.get_minimal_representation()
        to_save = {
            MSV_KEY: MODELSAVE_VERSION,
            ATR_KEY: attributes
        }

        with open(filename, 'wb') as handle:
            pickle.dump(to_save, handle)

    @classmethod
    def load(cls, filename, binary=True):
        """Load a model instance from file.

        Parameters
        ----------
        filename : str
            filename at which to save the current model.
        binary  : bool
            Flag for if the file should be saved as binary or not.  Defaults to binary.

        Returns
        -------
        ModelBase
            Instance of laoded model, a class that inherits ModelBase.
        """
        mode = 'r' + ('b' if binary else '')
        with open(filename, mode) as handle:
            response = pickle.load(handle)

        assert ((MSV_KEY in response) and
                (ATR_KEY in response) and
                (response[MSV_KEY] == MODELSAVE_VERSION)
                ), "Model file invalid."

        attributes = response[ATR_KEY]

        model = cls.init_with_minimal_representation(attributes)
        return model

