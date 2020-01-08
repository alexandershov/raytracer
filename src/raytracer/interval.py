from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Interval:
    min: Optional[float] = None
    max: Optional[float] = None

    def __contains__(self, item: float) -> bool:
        if self._has_min and item < self.min:
            return False
        if self._has_max and item > self.max:
            return False
        return True

    @property
    def _has_min(self) -> bool:
        return self.min is not None

    @property
    def _has_max(self) -> bool:
        return self.max is not None
