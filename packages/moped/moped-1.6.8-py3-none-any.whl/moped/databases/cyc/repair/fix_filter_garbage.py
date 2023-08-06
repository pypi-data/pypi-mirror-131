from __future__ import annotations

from typing import Dict

from ..data import ParseCompound, ParseReaction
from ..utils import _reaction_is_bad


def fix_filter_garbage_reactions(
    rxns: Dict[str, ParseReaction],
    cpds: Dict[str, ParseCompound],
) -> Dict[str, ParseReaction]:
    new_reactions = {}
    for rxn_id, reaction in rxns.items():
        if _reaction_is_bad(reaction, cpds):
            continue
        new_reactions[rxn_id] = reaction
    return new_reactions
