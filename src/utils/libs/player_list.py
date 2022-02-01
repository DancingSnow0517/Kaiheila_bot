from typing import Optional, Tuple, List

import parse


def get_server_player_list(old: str) -> Optional[Tuple[int, int, List[str]]]:
    formatters = (
        # <1.16
        # There are 6 of a max 100 players online: 122, abc, xxx, www, QwQ, bot_tob
        r'There are {amount:d} of a max {limit:d} players online:{players}',
        # >=1.16
        # There are 1 of a max of 20 players online: Fallen_Breath
        r'There are {amount:d} of a max of {limit:d} players online:{players}',
    )

    for formatter in formatters:
        parsed = parse.parse(formatter, old)
        if parsed is not None and parsed['players'].startswith(' '):
            return parsed['amount'], parsed['limit'], parsed['players'][1:]
