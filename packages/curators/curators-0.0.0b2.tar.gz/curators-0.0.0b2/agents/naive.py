from models.bandits import BANDITS_BY_VAR_TYPE


class NaiveAgent:
    """
    An abstraction around arbitrary k-armed bandits where the bandit configuration is parameterized.
    """
    def __init__(self, target_var_type, n_actions, observations=None):
        """Instantiate a NaiveAgent.

        Creates an instance of a naive agent - an abstraction around arbitrary k-armed bandits where the bandit
        configuration is parameterized.  While the Bandit class lets you both maintain a live model continually
        receiving updates, and/or quickly re-create a new class from scratch from the aggregate historical data, this
        Agent is only built to handle the "query full aggregate history and rebuild" pattern at the moment.  You'll only
        find the ability to set internal state within the class init with only having sampling functions available.

        Parameters
        ----------
        target_var_type : str
            defaults to rate.  See internal bandit class for instruction on customizing sample type.
        n_actions : int
            number of leverls for your bandit
        observations : list[list[int]]
            Aggregate historical performance of all levers represented by the number of positive responses and the
            number of negative responses.  Also accepts a numpy array of the same size and type.
            [(n_pos_l0, n_neg_l0), (n_pos_l1, ...
            This is the same format as the `observations` within the class init.

        """

        # ################################
        # handle parameters
        # TODO: test this assertion too?
        if target_var_type in BANDITS_BY_VAR_TYPE.keys():
            self.target_var_type = target_var_type
        else:
            raise ValueError("")

        # TODO: test both assertions
        if (type(n_actions) is int) and (n_actions > 0):
            self.n_actions = n_actions


        # ################################
        # initialize internal state
        self.model_class = BANDITS_BY_VAR_TYPE[self.target_var_type]
        self.model = self.model_class(
            n_levers=self.n_actions,
            observations=observations
        )  # is really self.model_instance

    def sample_one(self):
        """Samples a single action.

        Balance the goals of exploitation and exploration given the knowledge encoded into the model's internal state to
        pick a next good action.  Sample algorithm defaults to Thompson sampling.

        Returns
        -------
        int
            index of chosen lever
        """
        return self.model.sample_one()

    def sample(self, n):
        """Samples a batch of next actions.

        Balance the goals of exploitation and exploration given the knowledge encoded into the model's internal state to
        pick a batch of next good actions.  Sample algorithm defaults to Thompson sampling.


        Returns
        -------
        list[int]
            indices of chosen levers
        """
        return self.model.sample(n)

