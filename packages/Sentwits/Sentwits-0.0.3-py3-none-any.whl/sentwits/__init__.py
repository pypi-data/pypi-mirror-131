from sentwits.sentwits import COMMENTS, SENTIMENT, USER, GENERAL
from pkg_resources import get_distribution, DistributionNotFound
import os.path

__all__ = ['COMMENTS', 'SENTIMENT', 'USER', 'GENERAL']

try:
    _dist = get_distribution('sentwits')
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, 'sentwits')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'
else:
    __version__ = _dist.version