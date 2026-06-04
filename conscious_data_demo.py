#!/usr/bin/env python3
# conscious_data.py
#
# Röviden: ez a fájl a Conscious Data modell egy minimális,
# de működő példája. A program szabadon használható és módosítható
# a GPLv3 feltételei szerint.
#
# (A teljes licencszöveg külön LICENSE fájlban legyen.)

import uuid
from dataclasses import dataclass


@dataclass
class Location:
    storage: str
    layer: str | None = None
    row: str | None = None

    def to_meta(self):
        m = {"storage": self.storage}
        if self.layer:
            m["layer"] = self.layer
        if self.row:
            m["row"] = self.row
        return m

    @staticmethod
    def from_meta(meta):
        return Location(
            storage=meta["storage"],
            layer=meta.get("layer"),
            row=meta.get("row"),
        )


class ConsciousStorage:
    def __init__(self, name):
        self.name = name
        self._data = {}
        self._meta = {}

    def save(self, content: bytes, layer=None, row=None):
        oid = str(uuid.uuid4())
        loc = Location(self.name, layer, row)
        self._data[oid] = content
        self._meta[oid] = loc.to_meta()
        return oid

    def load(self, oid):
        return self._data[oid]

    def where(self, oid):
        return Location.from_meta(self._meta[oid])


if __name__ == "__main__":
    store = ConsciousStorage("disk-A")

    oid = store.save(
        b"Conscious Data teszt",
        layer="L1",
        row="R3"
    )

    print("ID:", oid)
    print("Tartalom:", store.load(oid).decode("utf-8"))

    loc = store.where(oid)
    print("Hely:")
    print("  storage:", loc.storage)
    print("  layer:", loc.layer)
    print("  row:", loc.row)
