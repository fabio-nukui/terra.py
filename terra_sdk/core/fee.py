"""Data objects about Fee."""

from __future__ import annotations

from typing import Dict, List, Optional

import attr
from terra_proto.cosmos.tx.v1beta1 import Fee as Fee_pb

from terra_sdk.core.bech32 import AccAddress
from terra_sdk.core.coins import Coins
from terra_sdk.util.json import JSONSerializable

__all__ = ["Fee"]


@attr.s
class Fee(JSONSerializable):
    """Data structure holding information for a transaction fee.

    Args:
        gas (int): gas to use ("gas requested")
        amount (Coins.Input): fee amount
    """

    gas_limit: int = attr.ib(converter=int)
    amount: Coins = attr.ib(converter=Coins)
    payer: Optional[AccAddress] = attr.ib(default=None)
    granter: Optional[AccAddress] = attr.ib(default=None)

    def to_amino(self) -> dict:
        return {"gas": str(self.gas_limit), "amount": self.amount.to_amino()}

    @classmethod
    def from_data(cls, data: dict) -> Fee:
        return cls(
            int(data["gas_limit"]),
            Coins.from_data(data["amount"]),
            data["payer"],
            data["granter"],
        )

    def to_data(self) -> dict:
        return {
            "gas_limit": str(self.gas_limit),
            "amount": self.amount.to_data(),
            "payer": self.payer if self.payer else "",
            "granter": self.granter if self.granter else "",
        }

    def to_proto(self) -> Fee_pb:
        return Fee_pb(
            amount=self.amount.to_proto(),
            gas_limit=self.gas_limit,
            payer=self.payer,
            granter=self.granter,
        )

    @classmethod
    def from_proto(cls, proto: Fee_pb) -> Fee:
        return cls(
            gas_limit=proto.gas_limit,
            amount=Coins.from_proto(proto.amount),
            payer=AccAddress(proto.payer),
            granter=AccAddress(proto.granter),
        )

    @classmethod
    def from_proto_bytes(cls, data: bytes) -> Fee:
        return cls.from_proto(Fee_pb.FromString(data))

    @property
    def gas_prices(self) -> Coins:
        return self.amount.to_dec_coins().div(self.gas_limit)
