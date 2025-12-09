import pytest  # noqa: F401
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
    nc = NetworkCoverage(long=10, lat=20, provider_list=[provider])

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

    nc = NetworkCoverage(long=100, lat=200, provider_list=[p1, p2])

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
    nc = NetworkCoverage(long=0, lat=0, provider_list=[])

    result = nc.to_dict()

    assert result == {}  # No providers → empty dict


def test_add_to_dict_adds_new_provider():
    provider = Provider(code=20801, twoG=True, threeG=False, fourG=True)  # Orange
    providers_dict = {}

    provider.add_to_dict(providers_dict)

    assert providers_dict == {
        "Orange": {
            "2G": True,
            "3G": False,
            "4G": True
        }
    }


def test_add_to_dict_merges_existing_provider_all_false_to_true():
    # Existing provider with all False
    providers_dict = {
        "Orange": {"2G": False, "3G": False, "4G": False}
    }
    provider = Provider(code=20801, twoG=True, threeG=False, fourG=True)

    provider.add_to_dict(providers_dict)

    assert providers_dict == {
        "Orange": {
            "2G": True,   # False OR True → True
            "3G": False,  # False OR False → False
            "4G": True    # False OR True → True
        }
    }


def test_add_to_dict_merges_existing_provider_retains_true():
    # Existing provider with a mix
    providers_dict = {
        "Orange": {"2G": True, "3G": False, "4G": False}
    }
    provider = Provider(code=20801, twoG=False, threeG=True, fourG=False)

    provider.add_to_dict(providers_dict)

    assert providers_dict == {
        "Orange": {
            "2G": True,   # True OR False → True
            "3G": True,   # False OR True → True
            "4G": False   # False OR False → False
        }
    }


def test_add_to_dict_different_provider_names_do_not_merge():
    p1 = Provider(code=20801, twoG=True, threeG=False, fourG=False)  # Orange
    p2 = Provider(code=20809, twoG=False, threeG=True, fourG=True)  # SFR

    providers_dict = {}
    p1.add_to_dict(providers_dict)
    p2.add_to_dict(providers_dict)

    assert providers_dict == {
        "Orange": {"2G": True, "3G": False, "4G": False},
        "SFR": {"2G": False, "3G": True, "4G": True},
    }
