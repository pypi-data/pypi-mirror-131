from curators.models.bandits import BANDITS_BY_VAR_TYPE
from curators.models.bandits.beta_bandit import BetaBandit
from curators.models.bandits.bandit_base import BanditBase
from curators.models.model_base import ModelBase


class ClusterBandit(ModelBase):
    """A contextual bandit that lets the user define and manage their own clusters.

    For when you have users clustered and you want to assign an individual naive bandit to each cluster.  Clusters
    can be directly from your own cluster model's `predict` as you'll find in the demo, your own set of business
    rules, or really any form of mapping a given sample to a single cluster.  Under the hood, this class sits on a
    list of uniformly typed bandits with all basic bandit interfaces extended to accept a cluster id.
    """
    # The source of truth for this class. Used directly for file saving and
    # loading.  Used implicitly as the core of all interfaces.
    minimal_attributes = [
        'n_clusters', 'n_levers', 'target_var_type', 'models']

    def __init__(self,
                 n_clusters=2,
                 n_levers=3,

                 observations=None,
                 target_var_type='rate',

                 **bandit_kwargs
                 ):
        """Instantiate a ClusterBandit.

        For when you have users clustered and you want to assign an individual naive bandit to each cluster.  Clusters
        can be directly from your own cluster model's `predict` as you'll find in the demo, your own set of business
        rules, or really any form of mapping a given sample to a single cluster.  Under the hood, this class sits on a
        list of uniformly typed bandits with all basic bandit interfaces extended to accept a cluster id.

        Parameters
        ----------
        n_clusters : int
            the number of clusters, which is also the number of bandits created under the hood.
        n_levers : int
            number of levers available.  While you can whitelist specific levers on any given bandit.sample(), each
            individual bandit must be given the same number of levers.
        observations : list[list[list[i]]]
            For if you want to init the contained bandits to some non-empty state.  Needs to itself be a list, where
            item i in the list is the i-th bandit's observations as the contained bandit would expect.  This parameter
            likely to be change into the raw historical observations.
        target_var_type : {'rate'}
            Determines the underlying distribution used to model each lever.  At the moment, only `rate` is implemenated
            and yields the Beta type bandit.  Gaussian distribution used to model floats coming soon.
        **bandit_kwargs
            All remaining kwargs are passed to bandit inits.
        """
        # TODO: change observations to be raw rather than complicated aggregate structure
        # ################################
        # handle parameters
        assert type(n_clusters) == int, "n_clusters must be an int"
        assert type(n_levers) == int, "n_levers must be an int"
        assert n_clusters > 0, "you must have more than 0 clusters"
        assert n_levers > 0, "you must have more than 0 levers"

        if observations is not None:
            assert type(observations) == list, \
                "obsersvations needs to be a list where item i are the " \
                "aggregate observations for cluster i."
            assert len(observations) == n_clusters, ""
        else:
            observations = [None] * n_clusters

        assert target_var_type in BANDITS_BY_VAR_TYPE.keys(), \
            "please register bandit type."  # TODO: make this possible
        self.target_var_type = target_var_type
        bandit_model = BANDITS_BY_VAR_TYPE[self.target_var_type]
        assert issubclass(bandit_model, BanditBase), \
            "bandid_model must be derive from BanditBase"
        self.model_class = bandit_model

        if (type(n_levers) is int) and (n_levers > 0):
            self.n_levers = n_levers

        # ################################
        # initialize internal state

        self.n_clusters = n_clusters

        self.models = []
        for i in range(n_clusters):
            self.models.append(
                self.model_class(
                    n_levers=self.n_levers,
                    observations=observations[i],
                    **bandit_kwargs
                )
            )

    def update_one(self, cluster_id, lever_id, result):
        """Updates model state using a single raw observation.

        Parameters
        ----------
        cluster_id : int
            id of cluster associated with the given sample
        lever_id : int
            lever that was selected for the given sample
        result : int
            result observed for the given sample.
        """
        self.models[cluster_id].update_one(lever_id, result)

    def update(self, raw_observations):
        """Updates model state using a batch of raw observations.

        Parameters
        ----------
        raw_observations : list[list[int]]
            observations = [
                [cluster_id_1, lever_id_1, result_1],
                [cluster_id_2, lever_id_2, result_2],
                ...,
                [cluster_id_N, lever_id_N, result_N]]
            Also works as an (N, 3) numpy array.  Results must already be in the proper response type matching your
            bandit type.

        """
        for cluster_id, lever_id, result in raw_observations:
            self.update_one(cluster_id, lever_id, result)

    def update_with_aggregates(self, aggregate_observations):
        raise NotImplementedError()

    def sample_one(self, cluster_id):
        """Samples a single action.

        Balance the goals of exploitation and exploration given the knowledge encoded into the model's internal state to
        pick a next good action.  Sample algorithm defaults to Thompson sampling.

        Parameters
        ----------
        cluster_id : int
            The id of the cluster associated with the entity you wish to select an action for.


        Returns
        -------
        int
            index of chosen lever
        """
        # TODO: at the least, pass kwargs through to let users customize the sampler and whitelist levers
        chosen_lever_id = self.models[cluster_id].sample_one()
        return chosen_lever_id

    def sample(self, cluster_ids):
        """Samples a batch of next actions.

        Balance the goals of exploitation and exploration given the knowledge encoded into the model's internal state to
        pick a batch of next good actions.  Sample algorithm defaults to Thompson sampling.

        Parameters
        ----------
        cluster_ids : list[int]
            A list of the cluster ids associated with the entity you wish to select an action for.  The length of this
            list will determine the number of actions selected.

        Returns
        -------
        list[int]
            indices of chosen levers
        """
        # TODO: at the least, pass kwargs through to let users customize the sampler and whitelist levers
        lever_ids = []
        for cluster_id in cluster_ids:
            this_lever_id = self.sample_one(cluster_id)
            lever_ids.append(this_lever_id)

        return lever_ids

    def get_minimal_representation(self):
        """
        Returns the dictionary of key:value pairs that encodes what a given model instance says is its minimal
        attributes.  Primarily used for model load.

        The class's self.minimal_attributes is the core mechanism that lets us ensure modelsave
        compatability across versions by letting us explicitly control what is saved.
        """
        attributes = {}
        for attr_key in self.minimal_attributes:
            if attr_key != "models":
                attr_val = getattr(self, attr_key)
            else:  # convert models to model reps
                models = getattr(self, attr_key)
                model_reps = []
                for model in models:
                    model_reps.append(model.get_minimal_representation())
                attr_val = model_reps
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
            if k == 'models':  # convert model reps to models.
                models = []
                for model_rep in v:
                    # TODO: once I get more than one model var type, I'll need
                    #  to pull the right class here.  for now, hardcode beta.
                    models.append(BetaBandit.init_with_minimal_representation(
                        model_rep
                    ))
                v = models
            setattr(model, k, v)
        return model
