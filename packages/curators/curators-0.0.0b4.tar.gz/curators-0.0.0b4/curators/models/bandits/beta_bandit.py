import logging

import numpy as np
from numpy.core import argmax
from scipy.stats import beta

from curators.models.bandits.bandit_base import BanditBase

logger = logging.getLogger(__name__)


# In case of Upper Confidence bound:
# * check out https://www.analyticsvidhya.com/blog/2018/09/reinforcement-multi-armed-bandit-scratch-python/
# * Though bailed on that because it is deterministic on the next lever to pull
#   to balance exploitation/exploration, so fails with the Batch interface.

# A good resource:
# https://github.com/WhatIThinkAbout/BabyRobot/blob/master/Multi_Armed_Bandits/Part%205%20-%20Thompson%20Sampling.ipynb
# See that page for some good graphs and overlapping code, and a gaussian
# version of this BetaBandit


class BetaBandit(BanditBase):
    """A k-armed bandit with levers modeled as rates

    Designed to be either
    * loaded from scratch just given proper counts, as you would do in production loading data from a db.
    * iteratively built as you could do when testing on simulated data.

    """

    # TODO: bring back a notion of learning rate
    # TODO: this should certainly collapse into doing numpy-native matrix
    #  math rather than manually looping
    def _sample_one_thompson(self, lever_subset=None):
        """Use Thompson sampling to select a single action.

        Parameters
        ----------
        lever_subset : list[int]
            The levers available to this call.
            `None` as the default, which uses all actions.
            Accepts a list or a set.
            An empty list or empty set is ambiguous, so returns an error.
            0-indexed.  i.e., if you have a 3-lever bandit, the defined indices
            are 0, 1, and 2.

        Returns
        -------
        int
            index of chosen lever
        """

        # These assertions being checked on the innermost loop isn't efficient.
        # Not a huge deal, since bandits are so insanely fast compared to any
        # other model, but we should still fix this down the road.
        if lever_subset is None:
            lever_subset = list(range(self.n_levers))
        else:
            # These checks are only worth doing if they are from the user:
            if (min(lever_subset) < 0) | (max(lever_subset) >= self.n_levers):
                raise ValueError("All lever_subset indices must be valid.")
            if len(lever_subset) == 0:
                raise ValueError("Empty lever_subset is ambiguous.  Define at "
                                 "least one lever subset.  None defaults to "
                                 "using all levers.")

        xs = []
        for a, b, i in zip(self.alphas, self.betas, range(self.n_levers)):
            if i in lever_subset:
                xs.append(beta.rvs(a, b, size=1)[0])
            else:
                xs.append(-1)
        this_choice = argmax(xs)
        logger.debug("a,b,[x_0,x_1,...], this_choice:", a, b, xs, this_choice)
        return this_choice

    sample_method_mapping = {
        'thompson': _sample_one_thompson
    }
    alphas = None
    betas = None

    # The source of truth for this class. Used directly for file saving and
    # loading.  Used implicitly as the core of all interfaces.
    minimal_attributes = ['n_levers', 'alphas', 'betas']

    # TODO: make the default use case expect numpy array for priors and observed
    def __init__(self,
                 n_levers=2,

                 learning_rate=1.0,

                 observations=None, priors=None
                 ):
        """Instantiate a BetaBandit.

        Defaults to giving you a beta bandit with (1,1) as the priors.  You can
        override the priors and/or pass in historical performance data.

        Parameters
        ----------
        n_levers : int
            The "k" of this "k-armed bandit".  Defaults to 2.
        learning_rate : float
            Learning rate for new samples.
        observations : list[list[int]]
            The aggregate historical performance of all levers represented by the number of positive reponses and the
            number of negative responses.  Also accepts a numpy array of the same size and type.
            [(n_pos_l0, n_neg_l0), (n_pos_l1, ...
            default is None, which is equivalent to all zeros
        priors  : list[list[int]]
            list shaped thing holding the alphas and betas for all priors.  Also accepts a numpy array of the same size
            and shape.
            [(alpha_l0, beta_l0), (alpha_l1, ...
            default is None, which is equivalent to ((1, 1), (1, 1), ...)

        """
        # TODO: Does alpha tolerate floats?  Could be a nice alternative
        #  interface to give the prior as a ratio and an N instead.

        assert type(n_levers) == int, "n_levers must be an int"
        assert n_levers > 0, "n_levers must be greater than 0"
        self.n_levers = n_levers

        self.alphas = np.zeros(n_levers)
        self.betas = np.zeros(n_levers)

        if priors is None:
            priors = [(1, 1) for i in range(n_levers)]
        self.update_with_aggregates(priors)
        self.update_with_aggregates(observations)

    def update_one(self, lever_id, result):
        """Updates model state using a single raw observation.

        Parameters
        ----------
        lever_id : int
            lever that was selected for the given sample
        result : int
            result observed for the given sample.
        """
        # TODO: assertions around lever_id
        assert result in (0, 1, 0., 1.), "beta bandit results are binary"
        if int(result) == 0:
            self.betas[lever_id] += 1
        else:
            self.alphas[lever_id] += 1

    def update(self, raw_observations):
        """Updates model state using a batch of raw observations.

        Parameters
        ----------
        raw_observations : list[list[int]]
            observations = [
                [lever_id_1, result_1],
                [lever_id_2, result_2],
                ...,
                [lever_id_N, result_N]]
            Also works as an (N,2) numpy array
        """
        for lever_id, result in raw_observations:
            self.update_one(lever_id=lever_id, result=result)

    def update_with_aggregates(self, aggregate_observations):
        """Update model state using pre-aggregated observations.

        Parameters
        ----------
        aggregate_observations : list[list[int]]
            The aggregate historical performance of all levers represented by the number of positive responses and the
            number of negative responses.  Also accepts a numpy array of the same size and type.
            [(n_pos_l0, n_neg_l0), (n_pos_l1, ...
            This is the same format as the `observations` within the class init.
        """
        # This is convertible to a np.array conversion, slicing alphas from
        # betas (or n_pos from n_neg), and vector addition.

        # TODO: TEST: that both np.array and list-of-lists work here.
        if aggregate_observations is not None:
            for i, this_obs in enumerate(aggregate_observations):
                n_pos, n_neg = this_obs
                self.alphas[i] += n_pos
                self.betas[i] += n_neg

    def sample_one(self, type='thompson', lever_subset=None):
        """Samples a single action.

        Balance the goals of exploitation and exploration given the knowledge encoded into the model's internal state to
        pick a next good action.  Sample algorithm defaults to Thompson sampling.

        Parameters
        ----------
        type : str
            Defaults to `thompson` sampling, which is currently the only sampling method available.  Custom sample
            methods can be added to this class's `sample_method_mapping` thus enabling them to be used during sampling
            by selecting your new sampling method's key.
        lever_subset : list[int]
            The levers available to this call.
            `None` as the default, which uses all actions.
            Accepts a list or a set.
            An empty list or empty set is ambiguous, so returns an error.
            0-indexed.  i.e., if you have a 3-lever bandit, the defined indices
            are 0, 1, and 2.


        Returns
        -------
        int
            index of chosen lever
        """

        # TODO:
        #  * should move this sample function selection to class init like
        #  we're doing with the bandit type.
        #  * should then use
        assert type in self.sample_method_mapping, \
            f"available sampling methods for {self.__class__.__name__} " \
            f"are {self.sample_method_mapping.keys()}"
        sampler = self.sample_method_mapping[type]
        return sampler(self, lever_subset)

    # TODO: reconsider naming here.  "choose lever"?
    def sample(self, n, type='thompson', lever_subset=None):
        """Samples a batch of next actions.

        Balance the goals of exploitation and exploration given the knowledge encoded into the model's internal state to
        pick a batch of next good actions.  Sample algorithm defaults to Thompson sampling.

        Parameters
        ----------
        n : int
            Number of samples to pull
        type : str
            Defaults to `thompson` sampling, which is currently the only sampling method available.  Custom sample
            methods can be added to this class's `sample_method_mapping` thus enabling them to be used during sampling
            by selecting your new sampling method's key.

        Returns
        -------
        list[int]
            indices of chosen levers
        """
        # Certainly theoretically faster to pull all `beta.rvs`s of the proper
        # size and solve for the winner as vector math, but code wise this is
        # simpler at the moment
        choices = []
        for i in range(n):
            choices.append(self.sample_one(
                type=type, lever_subset=lever_subset))
        return choices
