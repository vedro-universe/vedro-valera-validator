from vedro import Plugin

from vedro_valera_validator import ValeraValidator


def test_valera_validator():
    assert isinstance(ValeraValidator(), Plugin)
