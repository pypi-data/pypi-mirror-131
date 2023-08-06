from __future__ import annotations

from typing import Dict

from ..data import ParseCompound


def fix_add_important_compounds(
    compounds: Dict[str, ParseCompound],
    manual_additions: Dict[str, ParseCompound],
) -> Dict[str, ParseCompound]:
    compounds.update(manual_additions)
    return compounds
