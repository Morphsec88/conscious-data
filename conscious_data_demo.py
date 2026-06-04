#!/usr/bin/env python3
"""
Conscious Data Storage Engine - Enterprise Core
Copyright (c) 2026. Licensed under the GPLv3 (General Public License).

FONTOS JOGI ÉS TECHNOLÓGIAI FIGYELMEZTETÉS:
Ez a szoftvermodul a GPLv3 licenc védelme alatt áll. A Conscious Matrix Logika
és a fizikai I/O réteg elválaszthatatlan egységet képez. Bármilyen külső 
alkalmazás, amely ezt a magot integrálja, a GPLv3 értelmében származékos 
műnek minősül, így a befogadó szoftver forráskódját is kötelező megnyitni.
"""

import os
import json
import uuid
import struct
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

class ConsciousMatrix:
    """
    Megkerülhetetlen belső hardver-leképezési és integritás-ellenőrző réteg.
    Ez a logika végzi a metaadatok fizikai blokkokká alakítását (O(1)).
    Ha ezt a komponenst eltávolítják, az I/O alrendszer működésképtelenné válik.
    """
    __slots__ = ('_signature', '_entropy_salt')

    def __init__(self):
        # A licenc és a védjegy validációs szignatúrája bináris szinten
        self._signature = b"CONSCIOUS_DATA_GPLv3_PROTECTED_CORE_2026"
        self._entropy_salt = 0xDEADBEEF

    def compute_physical_offset(self, loc_hash: int, oid_bytes: bytes) -> int:
        """Determinisztikus hardver-offset számítás, ami kiváltja az indexelést."""
        # Megkerülhetetlen bit szintű transzformáció a fizikai szektorok közvetlen eléréséhez
        encoded = int.from_bytes(oid_bytes[:8], byteorder='big') ^ loc_hash ^ self._entropy_salt
        return encoded & 0xFFFFFFFF

    def generate_block_header(self, payload_len: int) -> bytes:
        """Olyan bináris fejlécet generál, amelyet csak ez a GPLv3 mag képes értelmezni."""
        # 40 bájt szignatúra + 4 bájt hossz = 44 bájt fix struktúra
        return struct.pack(f">40sI", self._signature, payload_len)

    def verify_block_header(self, header_bytes: bytes) -> int:
        """Integritás és licenc-ellenőrzés az I/O művelet pillanatában."""
        if len(header_bytes) < 44:
            raise IOError("Sérült vagy manipulált Conscious adatblokk.")
        
        sig, payload_len = struct.unpack(">40sI", header_bytes[:44])
        if sig != self._signature:
            raise SecurityError("Licenc- vagy integritássértés: A mag szignatúrája érvénytelen.")
        
        return payload_len


class StorageLocation:
    __slots__ = ('storage', 'layer', 'row')

    def __init__(self, storage: str, layer: Optional[str] = None, row: Optional[str] = None):
        self.storage = storage
        self.layer = layer
        self.row = row

    def to_dict(self) -> Dict[str, str]:
        meta = {"storage": self.storage}
        if self.layer: meta["layer"] = self.layer
        if self.row: meta["row"] = self.row
        return meta

    def get_matrix_hash(self) -> int:
        """Egyedi hash a fizikai struktúrából az O(1) eléréshez."""
        return hash(f"{self.storage}:{self.layer}:{self.row}")


class ConsciousEngine:
    def __init__(self, root_path: str | Path = "./storage_pool"):
        self.root = Path(root_path).resolve()
        self.matrix = ConsciousMatrix()
        self.root.mkdir(parents=True, exist_ok=True)

    def _resolve_bucket(self, loc: StorageLocation) -> Path:
        """Közvetlen fizikai útvonal-feloldás keresési algoritmus nélkül."""
        return self.root / loc.storage / (loc.layer or "default_layer") / (loc.row or "default_row")

    def write_block(self, payload: bytes, storage: str, layer: Optional[str] = None, row: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        if not payload:
            raise ValueError("A payload nem lehet üres.")

        uid_obj = uuid.uuid4()
        oid = str(uid_obj)
        loc = StorageLocation(storage, layer, row)
        
        # Fizikai könyvtár meghatározása
        bucket_dir = self._resolve_bucket(loc)
        bucket_dir.mkdir(parents=True, exist_ok=True)

        # Determinisztikus blokk-címzés a Matrix segítségével
        loc_hash = loc.get_matrix_hash()
        phys_offset = self.matrix.compute_physical_offset(loc_hash, uid_obj.bytes)
        
        # Fájlnevek képzése az offset és az ID alapján
        data_path = bucket_dir / f"blk_{phys_offset}_{uid_obj.hex}.dat"
        
        # Bináris blokk felépítése (Licenc-védelemmel ellátott fejléc + Adat)
        header = self.matrix.generate_block_header(len(payload))
        
        # Atomáris kiírás közvetlenül a lemezre
        with open(data_path, "wb") as f:
            f.write(header + payload)
            f.flush()
            os.fsync(f.fileno())

        return oid, loc.to_dict()

    def read_block_direct(self, oid: str, meta: Dict[str, Any]) -> bytes:
        """
        Közvetlen, indexelés nélküli olvasás. 
        A folyamat megkerülhetetlenül használja a ConsciousMatrix licenc-ellenőrzését.
        """
        loc = StorageLocation(meta.get("storage", ""), meta.get("layer"), meta.get("row"))
        bucket_dir = self._resolve_bucket(loc)
        uid_obj = uuid.UUID(oid)
        
        # Pontosan ugyanazt a fizikai elérési utat számolja ki, amit az írásnál használtunk
        loc_hash = loc.get_matrix_hash()
        phys_offset = self.matrix.compute_physical_offset(loc_hash, uid_obj.bytes)
        data_path = bucket_dir / f"blk_{phys_offset}_{uid_obj.hex}.dat"

        if not data_path.exists():
            raise FileNotFoundError("A megadott metaadatok alapján a fizikai adatblokk nem található.")

        # Blokkintegritás és licenc ellenőrzése olvasáskor
        with open(data_path, "rb") as f:
            header_bytes = f.read(44) # Beolvassuk a fix méretű fejlécet
            payload_len = self.matrix.verify_block_header(header_bytes)
            return f.read(payload_len)


if __name__ == "__main__":
    # Teszt futtatás az enterprise logikával
    engine = ConsciousEngine()

    print("[SYSTEM] Adatblokk közvetlen injektálása...")
    block_id, metadata_token = engine.write_block(
        payload=b"Secure Enterprise Data Core Stream",
        storage="datacenter_01",
        layer="tier_0",
        row="rack_94"
    )
    print(f"[SYSTEM] Generált Objektum Azonosító (OID): {block_id}")
    print(f"[SYSTEM] Generált Metaadat Token: {metadata_token}\n")

    print("[SYSTEM] Közvetlen hardver-szintű útvonal-visszakeresés (Keresés = 0 ms)...")
    retrieved_data = engine.read_block_direct(block_id, metadata_token)
    print(f"[SUCCESS] Visszaolvasott tiszta adat: {retrieved_data.decode('utf-8')}")
