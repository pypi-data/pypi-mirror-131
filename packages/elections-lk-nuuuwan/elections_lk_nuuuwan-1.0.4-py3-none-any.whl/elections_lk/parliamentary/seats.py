"""Various seat related utils."""

from elections_lk._constants import COUNTRY_ID
from elections_lk.parliamentary.YEAR_TO_REGION_TO_SEATS import \
    YEAR_TO_REGION_TO_SEATS

MAX_SEATS, MIN_SEATS = 255, 0

ELIG_LIMIT_FOR_ED = 0.05


def get_eligible_party_list(group_id, party_to_votes):
    """Get parties eligble for seats."""
    ELIG_LIMIT = 0 if (group_id == COUNTRY_ID) else ELIG_LIMIT_FOR_ED
    total_votes = sum(party_to_votes.values())

    if total_votes == 0:
        return []

    return list(
        filter(
            lambda party: party_to_votes[party] / total_votes > ELIG_LIMIT,
            party_to_votes.keys(),
        )
    )


def get_party_to_seats(year, group_id, party_to_votes):
    """Give votes by party, compute seats for party."""
    eligible_party_list = get_eligible_party_list(
        group_id,
        party_to_votes,
    )
    if not eligible_party_list:
        return {}

    n_seats = YEAR_TO_REGION_TO_SEATS[year][group_id]
    n_seats_bonus = 0 if (group_id == COUNTRY_ID) else 1
    n_seats_non_bonus = n_seats - n_seats_bonus

    winning_party = sorted(party_to_votes.items(), key=lambda x: -x[1],)[
        0
    ][0]

    party_to_seats = {winning_party: n_seats_bonus}

    relevant_num = sum(
        list(
            map(
                lambda party: party_to_votes[party],
                eligible_party_list,
            )
        )
    )

    party_r = []
    n_seats_r = n_seats_non_bonus
    resulting_num = (int)(relevant_num / n_seats_non_bonus)
    for party in eligible_party_list:
        seats_r = party_to_votes[party] / resulting_num
        seats_non_bonus_whole = (int)(seats_r)

        party_to_seats[party] = (
            party_to_seats.get(party, 0) + seats_non_bonus_whole
        )

        party_r.append((party, seats_r % 1))
        n_seats_r -= seats_non_bonus_whole

    party_r = sorted(party_r, key=lambda x: -x[1])
    for i in range(0, n_seats_r):
        party = party_r[i][0]
        party_to_seats[party] = party_to_seats.get(party, 0) + 1

    return party_to_seats


if __name__ == '__main__':
    print(
        get_party_to_seats(
            2020,
            'EC-03',
            {
                'SLPP': 448699,
                'SJB': 171988,
            },
        )
    )
