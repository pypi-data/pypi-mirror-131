from __future__ import annotations

from typing import Dict

from ....core.reaction import KineticData
from ..data import ParseReaction


def fix_kinetic_data(rxns: Dict[str, ParseReaction]) -> Dict[str, ParseReaction]:
    for rxn in rxns.values():
        rxn.kinetic_data = {
            k: KineticData(km=v.get("km", {}), kcat=v.get("kcat", {})) for k, v in rxn.enzrxns.items()
        }
        # del rxn.enzrxns
    return rxns
