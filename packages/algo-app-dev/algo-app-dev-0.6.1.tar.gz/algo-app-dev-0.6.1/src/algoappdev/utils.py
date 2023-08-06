"""Common utilities imported in other modules."""

import base64
from typing import Dict, NamedTuple, Union

import algosdk as ag
from algosdk.v2client.models.teal_key_value import TealKeyValue
from algosdk.v2client.models.teal_value import TealValue

ZERO_ADDRESS = ag.encoding.encode_address(bytes(32))


class AlgoAppDevError(Exception):
    """Base for all errors raised from the package."""

    pass


class AccountMeta(NamedTuple):
    """The meta-data required to lookup an account."""

    key: str
    address: str


class AppMeta(NamedTuple):
    """The meta-data required to lookup an app."""

    app_id: int
    address: str

    @staticmethod
    def from_result(result: Dict) -> "AppMeta":
        app_id = result.get("application-index", None)
        if app_id is None:
            return None
        # at the time of writing, the app address was a new feature not yet in
        # the python SDK, but this has probably changed by now
        address = ag.encoding.encode_address(
            ag.encoding.checksum(b"appID" + app_id.to_bytes(8, "big"))
        )
        return AppMeta(app_id=app_id, address=address)


def from_value(value: TealValue) -> Union[int, bytes]:
    """Convert a TEAL value to it's Python value."""
    if value is None:
        return None
    if value.get("type", None) == 1:
        value = value.get("bytes", None)
        value = base64.b64decode(value)
    elif value.get("type", None) == 2:
        value = value.get("uint", None)
    return value


def to_value(value: Union[int, bytes]) -> TealValue:
    """Convert a Python value to it's TEAL value."""
    if isinstance(value, bytes):
        return TealValue(type=1, bytes=base64.b64encode(value).decode("ascii"))
    elif isinstance(value, int):
        return TealValue(type=2, uint=value)
    else:
        raise AlgoAppDevError(f"invalid value type: {type(value)}")


def to_key_value(key: bytes, value: Union[int, bytes]) -> TealKeyValue:
    """Build a TEAL key-value pair from Python objects."""
    key = base64.b64encode(key).decode("ascii")
    return TealKeyValue(key, to_value(value))


def idx_to_address(idx: int) -> str:
    """Build an address whose integer value is `idx`."""
    return ag.encoding.encode_address(idx.to_bytes(ag.constants.key_len_bytes, "big"))


def address_to_idx(address: str) -> int:
    """Calculate the integer value of a key, modulo `2**64`."""
    return int.from_bytes(ag.encoding.decode_address(address)[-8:], "big")
