#!/usr/bin/env python3
import os
import json
import struct
import time
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

class ConsciousMatrix:
    def __init__(self) -> None:
        self.START_MARKER = b"\x02[CONSCIOUS_START]"
        self.END_MARKER = b"[CONSCIOUS_END]\x03"

    def make_capsule(self, payload: bytes, storage: str, layer: str, row: str, sub_index: str, density: int) -> bytes:
        payload_length = len(payload)
        
        # Alap metaadatok, amiket minden szint rögzít
        meta_content = {
            "storage": storage,
            "layer": layer,
            "row": row,
            "sub_index": sub_index,
            "payload_size": payload_length,
            "density": density
        }
        
        # 3-as szinttől felette az adat "időbeli tudása" mélyül: pontos időbélyeget kap
        if density >= 3:
            meta_content["timestamp"] = time.time()
            
        # 4-es szinttől felette egy egyszerű integritás-ellenőrző összeget is rendelünk hozzá
        if density >= 4:
            meta_content["checksum"] = sum(payload) & 0xFFFFFFFF

        meta_bytes = json.dumps(meta_content).encode("utf-8")
        meta_length = len(meta_bytes)
        
        header = self.START_MARKER + struct.pack(">I", meta_length)
        return header + meta_bytes + payload + self.END_MARKER

    def unpack_capsule(self, raw_bytes: bytes, expected_loc: Dict[str, str]) -> bytes:
        if not raw_bytes.startswith(self.START_MARKER):
            raise ValueError("Sérült adat: hiányzik a nyitó karakterlánc.")
            
        start_offset = len(self.START_MARKER)
        meta_length = struct.unpack(">I", raw_bytes[start_offset : start_offset + 4])[0]
        
        meta_bytes = raw_bytes[start_offset + 4 : start_offset + 4 + meta_length]
        meta_content = json.loads(meta_bytes.decode("utf-8"))
        
        # Keresztellenőrzési hurok
        if (meta_content["storage"] != expected_loc["storage"] or
            meta_content["layer"] != expected_loc["layer"] or
            meta_content["row"] != expected_loc["row"] or
            meta_content["sub_index"] != expected_loc["sub_index"]):
            raise RuntimeError("Helyváltoztatási anomália: a belső koordináta-pecsét eltér a fizikai helytől.")
            
        payload_size = meta_content["payload_size"]
        payload_start = start_offset + 4 + meta_length
        payload_end = payload_start + payload_size
        
        payload = raw_bytes[payload_start:payload_end]
        
        # Szigorú szintű ellenőrzések visszaolvasáskor
        if meta_content["density"] >= 4:
            current_checksum = sum(payload) & 0xFFFFFFFF
            if meta_content["checksum"] != current_checksum:
                raise ValueError("Integritási hiba: az adat belső összege megváltozott (sérülés).")

        actual_end_marker = raw_bytes[payload_end : payload_end + len(self.END_MARKER)]
        if actual_end_marker != self.END_MARKER:
            raise ValueError("Sérült vagy csonka adat: a lezáró marker nincs a helyén.")
            
        return payload

class StorageLocation:
    def __init__(self, storage: str, layer: Optional[str] = None, row: Optional[str] = None, sub_index: str = "A") -> None:
        self.storage = storage
        self.layer = layer or "default"
        self.row = row or "default"
        self.sub_index = sub_index

    def to_dict(self) -> Dict[str, str]:
        return {
            "storage": self.storage,
            "layer": self.layer,
            "row": self.row,
            "sub_index": self.sub_index
        }

class ConsciousEngine:
    def __init__(self, root_path: str | Path = "./storage_pool", density: int = 2) -> None:
        self.root = Path(root_path).resolve()
        self.matrix = ConsciousMatrix()
        # 1 és 5 közötti sűrűségi szint korlátozása
        self.density = max(1, min(5, density))
        self.root.mkdir(parents=True, exist_ok=True)

    def _target_path(self, loc: StorageLocation) -> Path:
        suffix = "" if loc.sub_index == "A" else f"_{loc.sub_index}"
        return self.root / loc.storage / loc.layer / f"row_{loc.row}{suffix}.dat"

    def _generate_next_sub_index(self, iteration: int) -> str:
        abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        cycle = iteration // len(abc)
        letter = abc[iteration % len(abc)]
        return letter if cycle == 0 else f"{letter}{cycle + 1}"

    def write(self, payload: bytes, storage: str, layer: Optional[str] = None, row: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        current_layer = layer or "default"
        current_row = row or "default"
        
        iteration = 0
        while True:
            chosen_sub = self._generate_next_sub_index(iteration)
            temp_loc = StorageLocation(storage, current_layer, current_row, sub_index=chosen_sub)
            if not self._target_path(temp_loc).exists():
                break
            iteration += 1

        loc = StorageLocation(storage, current_layer, current_row, sub_index=chosen_sub)
        target = self._target_path(loc)
        target.parent.mkdir(parents=True, exist_ok=True)
        
        full_package = self.matrix.make_capsule(payload, loc.storage, loc.layer, loc.row, loc.sub_index, self.density)
        
        with open(target, "wb") as f:
            f.write(full_package)
            # 2-es szinttől felette kényszerítjük ki a hardveres azonnali kiírást (sebesség vs biztonság)
            if self.density >= 2:
                f.flush()
                os.fsync(f.fileno())
            
        return target.stem, loc.to_dict()

    def read(self, storage: str, layer: Optional[str] = None, row: Optional[str] = None, sub_index: str = "A") -> bytes:
        loc = StorageLocation(storage, layer, row, sub_index)
        target = self._target_path(loc)
        
        if not target.exists():
            raise FileNotFoundError(f"Nem található adat a koordinátán: {target}")
            
        with open(target, "rb") as f:
            raw_bytes = f.read()
            
        return self.matrix.unpack_capsule(raw_bytes, loc.to_dict())
