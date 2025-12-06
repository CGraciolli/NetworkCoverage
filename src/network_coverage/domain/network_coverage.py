from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Provider:
    code: int
    twoG: bool
    threeG: bool
    fourG: bool

    def __post_init__(self):
        provider_map = {
            20801: "Orange", 20802: "Orange", 20803: "MobiquiThings", 20804: "Netcom Group",
            20805: "Globalstar",20808: "Completel",20809: "SFR",20810: "SFR",20811: "SFR",
            20813: "SFR",20814: "RFF",20815: "Free",20816: "Free",20817: "Legos",
            20818: "Voxbone",20819: "Altitude",20820: "Bouygues Telecom",20821: "Bouygues Telecom",
            20822: "Transatel Mobile",20824: "MobiquiThings",20825: "Lycamobile",20827: "Coriolis",
            20828: "AIF",20830: "Syma Mobile",20832: "Orange",20834: "Cellhire",20835: "Free"
            }
        self.name = provider_map.get(self.code, str(self.code))
    
    def to_dict(self) -> Dict[str, Dict[str, bool]]:
        return {self.name: {
            "2G": self.twoG,
            "3G": self.threeG,
            "4G": self.fourG
        }}
    
    def add_to_dict(self, dict_of_providers: dict):
        if self.name not in dict_of_providers.keys():
            dict_of_providers[self.name] = {
                "2G": self.twoG,
                "3G": self.threeG,
                "4G": self.fourG
            }
        else:
            dict_of_providers[self.name]["2G"] = dict_of_providers[self.name]["2G"] or self.twoG
            dict_of_providers[self.name]["3G"] = dict_of_providers[self.name]["3G"] or self.threeG
            dict_of_providers[self.name]["4G"] = dict_of_providers[self.name]["4G"] or self.fourG

@dataclass
class NetworkCoverage:
    long: int
    lat: int
    provider_list: List[Provider]

    def to_dict(self) -> Dict[str, Dict[str, bool]]:
        coverage_dict = {}
        for provider in self.provider_list:
            coverage_dict.update(provider.to_dict())
        return coverage_dict
            