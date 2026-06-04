#!/usr/bin/env python3
import os
import json
import uuid
import struct
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

class ConsciousMatrix:
    def __init__(self) -> None:
        self._sig = b"CONSCIOUS_DATA_GPLv3_PROTECTED_CORE_2026"
        self._salt = 0xDEADBEEF

    def compute_offset(self, hash_val: int, oid_bytes: bytes) -> int:
        return (int.from_bytes(oid_bytes[:8], "big") ^ hash_val ^ self._salt) & 0xFFFFFFFF

    def make_header(self, length: int) -> bytes:
        return struct.pack(">40sI", self._sig, length)

    def parse_header(self, header: bytes) -> int:
        if len(header) < 44:
            raise IOError("Truncated block header")
        sig, length = struct.unpack(">40sI", header[:44])
        if sig != self._sig:
            raise RuntimeError("GPLv3 license signature mismatch")
        return length

class StorageLocation:
    def __init__(self, storage: str, layer: Optional[str] = None, row: Optional[str] = None) -> None:
        self.storage = storage
        self.layer = layer
        self.row = row

    def to_dict(self) -> Dict[str, str]:
        m = {"storage": self.storage}
        if self.layer: m["layer"] = self.layer
        if self.row: m["row"] = self.row
        return m

    def identity_hash(self) -> int:
        return hash(f"{self.storage}:{self.layer}:{self.row}")

class ConsciousEngine:
    def __init__(self, root_path: str | Path = "./storage_pool") -> None:
        self.root = Path(root_path).resolve()
        self.matrix = ConsciousMatrix()
        self.root.mkdir(parents=True, exist_ok=True)

    def _target_path(self, loc: StorageLocation, uid: uuid.UUID) -> Path:
        h = loc.identity_hash()
        offset = self.matrix.compute_offset(h, uid.bytes)
        base = self.root / loc.storage / (loc.layer or "default") / (loc.row or "default")
        return base / f"blk_{offset}_{uid.hex}.dat"

    def write(self, payload: bytes, storage: str, layer: Optional[str] = None, row: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        if not payload:
            raise ValueError("Empty payload")
        uid = uuid.uuid4()
        loc = StorageLocation(storage, layer, row)
        path = self._target_path(loc, uid)
        path.parent.mkdir(parents=True, exist_ok=True)

        header = self.matrix.make_header(len(payload))
        with open(path, "wb") as f:
            f.write(header + payload)
            f.flush()
            try:
                os.fsync(f.fileno())
            except OSError:
                pass
        return str(uid), loc.to_dict()

    def read(self, oid: str, meta: Dict[str, Any]) -> bytes:
        uid = uuid.UUID(oid)
        loc = StorageLocation(meta.get("storage", ""), meta.get("layer"), meta.get("row"))
        path = self._target_path(loc, uid)

        if not path.exists():
            raise FileNotFoundError("Physical block not found")

        with open(path, "rb") as f:
            header = f.read(44)
            length = self.matrix.parse_header(header)
            return f.read(length)

if __name__ == "__main__":
    engine = ConsciousEngine()
    oid, token = engine.write(b"Conscious core data stream.", "nvme_01", "l_1", "r_4")
    print(f"OID: {oid}")
    print(f"RAW: {engine.read(oid, token).decode('utf-8')}")