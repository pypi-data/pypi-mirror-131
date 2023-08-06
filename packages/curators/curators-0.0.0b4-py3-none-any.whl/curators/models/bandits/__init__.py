from .beta_bandit import BetaBandit
from .gaussian_bandit import GaussianBandit


BANDITS_BY_VAR_TYPE = {
    'rate': BetaBandit,
    'float': GaussianBandit
}

__all__ = [
    'BetaBandit',
    'GaussianBandit',
    'BANDITS_BY_VAR_TYPE'
]
