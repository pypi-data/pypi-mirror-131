import colorsys
import re

from gig.ent_types import ENTITY_TYPE
from gig.ents import get_entity_index
from infographics import plotx
from infographics.Infographic import Infographic
from infographics.LKDorlingCartogram import LKDorlingCartogram

from elections_lk._constants import COUNTRY_ID
from elections_lk.parliamentary.parliamentary import get_election_data
from elections_lk.parliamentary.seats import get_party_to_seats
from elections_lk.parliamentary.YEAR_TO_REGION_TO_SEATS import \
    YEAR_TO_REGION_TO_SEATS

BASE_YEAR = 2020
P_P1, P_P2 = 0.6, 0.4
P_TURNOUT = 0.75
P_VALID = 0.95
P_P3_MAX = 0.075
INCR_VOTES = 1000


def ignore_vowels(s):
    return re.sub(r'[aeiou]', '', s)


def analyze():
    base_election_data = get_election_data(BASE_YEAR)
    ed_to_electors = {}
    for d in base_election_data:
        ed_id = d['ed_id']
        if ed_id not in ed_to_electors:
            ed_to_electors[ed_id] = 0

        summary = d['summary']
        electors = summary['electors']
        ed_to_electors[ed_id] += electors
    YEAR_TO_REGION_TO_SEATS[BASE_YEAR]
    ed_id_to_info_list = {}
    total_valid_votes = 0

    for ed_id, electors in ed_to_electors.items():
        valid_votes = electors * P_TURNOUT * P_VALID
        total_valid_votes += valid_votes
        votes_p3 = INCR_VOTES
        prev_seats_p3 = 0
        prev_votes_p3 = 0
        while votes_p3 <= valid_votes * P_P3_MAX:
            rem_votes = valid_votes - votes_p3
            votes_p1 = round(rem_votes * P_P1, 0)
            votes_p2 = round(rem_votes * P_P2, 0)
            p_p3 = votes_p3 / valid_votes

            party_to_seats = get_party_to_seats(
                BASE_YEAR,
                ed_id,
                {
                    'P1': votes_p1,
                    'P2': votes_p2,
                    'P3': votes_p3,
                },
            )
            seats_p3 = party_to_seats.get('P3', 0)
            if seats_p3 != prev_seats_p3 and seats_p3 > 0:
                d_votes = votes_p3 - prev_votes_p3
                prev_votes_p3 = votes_p3

                if ed_id not in ed_id_to_info_list:
                    ed_id_to_info_list[ed_id] = []
                ed_id_to_info_list[ed_id].append(
                    dict(
                        ed_id=ed_id,
                        seats_p3=seats_p3,
                        votes_p3=votes_p3,
                        d_votes=d_votes,
                        p_p3=p_p3,
                    )
                )

            prev_seats_p3 = seats_p3
            votes_p3 += INCR_VOTES

    ordered_info_list = []

    while ed_id_to_info_list:
        sorted_ed_id_and_info_list = sorted(
            list(
                map(
                    lambda x: list(x),
                    ed_id_to_info_list.items(),
                )
            ),
            key=lambda x: x[1][0]['d_votes'],
        )

        ordered_info_list.append(sorted_ed_id_and_info_list[0][1][0])
        if len(sorted_ed_id_and_info_list[0][1]) == 1:
            sorted_ed_id_and_info_list = sorted_ed_id_and_info_list[1:]
        else:
            sorted_ed_id_and_info_list[0][1] = sorted_ed_id_and_info_list[0][
                1
            ][1:]
        ed_id_to_info_list = dict(sorted_ed_id_and_info_list)

    ed_index = get_entity_index(ENTITY_TYPE.ED)

    cum_votes = 0
    cum_seats = 0
    round10 = 0
    prev_round10 = 0
    ed_to_p3_seats = {}
    ed_to_p3_p = {}
    ed_to_p3_votes = {}
    for d in ordered_info_list:
        ed_id = d['ed_id']
        ed = ed_index[ed_id]
        ed_name = ed['name']
        seats_p3 = d['seats_p3']
        cum_seats += 1
        d_votes = d['d_votes']
        cum_votes += d_votes
        p_p3 = d['p_p3']
        p_total = cum_votes / total_valid_votes

        # national list
        rem_votes = total_valid_votes - cum_votes
        votes_p1 = rem_votes * P_P1
        votes_p2 = rem_votes * P_P2
        party_to_seats = get_party_to_seats(
            BASE_YEAR,
            COUNTRY_ID,
            {
                'P1': votes_p1,
                'P2': votes_p2,
                'P3': cum_votes,
            },
        )
        national_list_seats = party_to_seats.get('P3', 0)
        all_seats = cum_seats + national_list_seats

        print(
            f'Seat {all_seats})\t{cum_votes:,}\t({p_total:.1%})\t+{d_votes}'
            + f'\t{ed_name} (Seat-{seats_p3}) ({p_p3:.1%})'
        )
        round10 = (int)(all_seats / 10)
        if prev_round10 != round10:
            print('.' * 32)

        prev_round10 = round10
        # ed_name_str = ignore_vowels(ed_name)
        # print(f'{ed_name_str} ({p_p3:.1%})')

        ed_to_p3_seats[ed_id] = seats_p3
        ed_to_p3_p[ed_id] = p_p3
        ed_to_p3_votes[ed_id] = d['votes_p3']

    # plot
    # print('.' * 64)
    # print(ed_to_p3_seats)
    # gpd_df = geodata.get_region_geodata('LK', ENTITY_TYPE.ED)
    #
    # gpd_df['seats'] = gpd_df['id'].map(ed_to_p3_seats)
    # gpd_df.plot(
    #     column='seats',
    #     legend=True,
    #     cmap='OrRd',
    #     figsize=(7, 9),
    # )
    #
    # plt.savefig('%s.png' % __file__)
    # plt.show()

    def _func_get_color_value(row):
        return row.id

    def _func_value_to_color(ed_id):
        p = ed_to_p3_p.get(ed_id, 0)
        h = 0
        s = 1.0
        lightness = 1 - p
        return colorsys.hls_to_rgb(h, lightness, s)

    def _func_format_color_value(ed_id):
        p = ed_to_p3_p.get(ed_id, 0)
        return f'{p:.1%}'

    def _func_render_label(row, x, y, spany):
        ed_id = _func_get_color_value(row)
        p = ed_to_p3_p.get(ed_id, 0)
        if p > 0:
            seats = ed_to_p3_seats.get(ed_id, 0)

            r2 = spany / 50
            plotx.draw_text(
                (x, y + r2 * 0.5), f'{seats} ({p:.1%})', fontsize=8
            )
            plotx.draw_text((x, y - r2 * 0.5), row['name'], fontsize=6)

    def _func_get_area_value(row):
        ed_id = row.id
        return ed_to_p3_votes.get(ed_id, 0)

    def _func_format_area_value(votes):
        return f'{votes:,.0f} votes'

    dorling = LKDorlingCartogram(
        sub_region_type=ENTITY_TYPE.ED,
        func_get_color_value=_func_get_color_value,
        func_value_to_color=_func_value_to_color,
        func_format_color_value=_func_format_color_value,
        func_render_label=_func_render_label,
        func_get_area_value=_func_get_area_value,
        func_format_area_value=_func_format_area_value,
    )

    Infographic(
        title='Hypothetical Sri Lankan Parliamentary Election',
        subtitle='Seats by "Third Party"',
        footer_text='\n'.join(
            [
                'visualization by @nuuuwan',
            ]
        ),
        children=[
            dorling,
        ],
    ).save('/tmp/elections_lk.analysis.easiest_seats.png')


if __name__ == '__main__':
    analyze()
