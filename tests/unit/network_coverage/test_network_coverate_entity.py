import pytest
from src.network_coverage.domain.network_coverage import Provider, NetworkCoverage


# -------------------------
# Provider Tests
# -------------------------

def test_provider_name_mapping_known_code():
    provider = Provider(code=20801, twoG=True, threeG=False, fourG=True)
    assert provider.name == "Orange"


def test_provider_name_mapping_unknown_code():
    provider = Provider(code=99999, twoG=False, threeG=True, fourG=False)
    assert provider.name == "99999"   # Fallback to string of code


def test_provider_to_dict():
    provider = Provider(code=20815, twoG=True, threeG=True, fourG=False)
    
    result = provider.to_dict()

    assert result == {
        "Free": {
            "2G": True,
            "3G": True,
            "4G": False
        }
    }


# -------------------------
# NetworkCoverage Tests
# -------------------------

def test_networkcoverage_single_provider():
    provider = Provider(code=20821, twoG=True, threeG=False, fourG=True)
    nc = NetworkCoverage(long=10, lat=20, provider_set=[provider])

    result = nc.to_dict()

    assert result == {
        "Bouygues Telecom": {
            "2G": True,
            "3G": False,
            "4G": True
        }
    }


def test_networkcoverage_multiple_providers():
    p1 = Provider(code=20801, twoG=True, threeG=True, fourG=False)   # Orange
    p2 = Provider(code=20809, twoG=False, threeG=True, fourG=True)   # SFR

    nc = NetworkCoverage(long=100, lat=200, provider_set=[p1, p2])

    result = nc.to_dict()

    assert result == {
        "Orange": {
            "2G": True,
            "3G": True,
            "4G": False
        },
        "SFR": {
            "2G": False,
            "3G": True,
            "4G": True
        }
    }


def test_networkcoverage_empty_provider_list():
    nc = NetworkCoverage(long=0, lat=0, provider_set=[])

    result = nc.to_dict()

    assert result == {}  # No providers → empty dict
