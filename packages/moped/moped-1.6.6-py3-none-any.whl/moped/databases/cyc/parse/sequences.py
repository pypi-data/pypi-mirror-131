from __future__ import annotations

import re
from typing import Dict, Iterator

__all__ = ["SequenceParser"]


class SequenceParser:
    def parse(self, file: Iterator[str]) -> Dict[str, str]:
        RE_PAT = re.compile(r"^>gnl\|.*?\|")
        sequences: Dict[str, str] = {}
        while True:
            try:
                id_ = re.sub(RE_PAT, "", next(file)).split(" ", maxsplit=1)[0]
                sequence = next(file).strip()
                sequences[id_] = sequence
            except StopIteration:
                break
        return sequences
