from models.contextual_bandits import ClusterBandit

TYPE_MAPPING = {
    'cluster': ClusterBandit,
}

class ContextualAgent:
    """Coming Soon.
    """
    def __init__(self, n_profiles, n_actions, type='cluster'):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def sample_one(self, x):
        raise NotImplementedError

    def sample(self, X):
        actions = []
        for x in X:
            actions.append(self.sample_one(x))
        raise NotImplementedError

