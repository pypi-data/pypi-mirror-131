import os

from utils import www
from utils.cache import cache

from elections_lk._constants import CACHE_NAME, CACHE_TIMEOUT
from elections_lk._utils import log


def _clean_by_party(by_party):
    return {
        'party_id': by_party['party_code'],
        'votes': (int)(by_party['vote_count']),
    }


def _clean_pd_result(pd_result):
    cleaned_result = {}
    cleaned_result['ed_id'] = 'EC-' + pd_result['ed_code']
    cleaned_result['pd_id'] = 'EC-' + pd_result['pd_code']
    cleaned_result['ed_name'] = pd_result['ed_name']
    cleaned_result['pd_name'] = pd_result['pd_name']
    cleaned_result['timestamp'] = pd_result['timestamp']

    cleaned_result['by_party'] = sorted(
        list(
            map(
                _clean_by_party,
                pd_result['by_party'],
            )
        ),
        key=lambda for_party: -for_party['votes'],
    )

    cleaned_result['summary'] = {
        'valid': pd_result['summary']['valid'],
        'rejected': pd_result['summary']['rejected'],
        'polled': pd_result['summary']['polled'],
        'electors': pd_result['summary']['electors'],
    }

    return cleaned_result


@cache(CACHE_NAME, CACHE_TIMEOUT)
def get_election_data(year):
    url = os.path.join(
        'https://raw.githubusercontent.com/nuuuwan/elections_lk/data',
        'gen_elec_sl.ec.results.%d.json' % year,
    )
    log.info('Downloading data from %s', url)
    all_results = www.read_json(url)
    pd_results = list(
        filter(
            lambda result: result['level'] == 'POLLING-DIVISION',
            all_results,
        )
    )
    cleaned_pd_results = list(
        map(
            _clean_pd_result,
            pd_results,
        )
    )
    return cleaned_pd_results


if __name__ == '__main__':
    print(get_election_data(2020))
