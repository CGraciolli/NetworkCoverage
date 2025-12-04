from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Provider:
    name: str
    coverage: Dict[str, bool]

    def to_dict(self) -> dict:
        return {
            self.name: self.coverage
        }

@dataclass
class NetworkCoverage:
    provider_set: List[Provider]

    def to_dict(self) -> dict:
        dict_representation = {}
        for provider in self.provider_set:
            dict_representation.update(provider.to_dict())
        return dict_representation
          