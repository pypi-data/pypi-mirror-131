from __future__ import annotations

from typing import Dict

from ..data import ParseCompound, ParseReaction

__all__ = ["MALFORMED_LINE_STARTS"]

# Often lines starting with these identifiers are malformed
MALFORMED_LINE_STARTS = {
    "/",
    "COMMENT",
    "CITATIONS",
    "^CITATIONS",
    "SYNONYMS",
    "#",
}


def _rename(content: str) -> str:
    """Remove garbage from compound and reaction ids."""
    return (
        content.replace("<i>", "")
        .replace("</i>", "")
        .replace("<SUP>", "")
        .replace("</SUP>", "")
        .replace("<sup>", "")
        .replace("</sup>", "")
        .replace("<sub>", "")
        .replace("</sub>", "")
        .replace("<SUB>", "")
        .replace("</SUB>", "")
        .replace("&", "")
        .replace(";", "")
        .replace("|", "")
    )


def _set_gibbs0(dictionary: Dict[str, ParseReaction | ParseCompound], id_: str, gibbs0: str) -> None:
    try:
        dictionary[id_].gibbs0 = float(gibbs0)
    except ValueError:  # conversion failed
        pass


def _set_name(dictionary: Dict[str, ParseReaction | ParseCompound], id_: str, name: str) -> None:
    dictionary[id_].name = _rename(name)


def _add_database_link(dictionary: Dict[str, ParseReaction | ParseCompound], id_: str, content: str) -> None:
    """Short description.

    Database links are of form DBLINKS - (REFMET "Tryptophan" NIL |midford| 3697479617 NIL NIL)
    so content will be (REFMET "Tryptophan" NIL |midford| 3697479617 NIL NIL)
    """
    database, database_id, *_ = content[1:-1].split(" ")
    dictionary[id_].database_links.setdefault(database, set()).add(database_id[1:-1])


def _add_type(
    dictionary: Dict[str, ParseReaction | ParseCompound],
    id_: str,
    type_: str,
    type_map: Dict[str, str],
) -> None:
    """Short description."""
    dictionary[id_].types.append(type_map.get(type_, type_))
