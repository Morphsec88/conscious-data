
<img width="750" height="497" alt="consciousdata" src="https://github.com/user-attachments/assets/eb176d36-0c23-4ae5-ac52-c13ff8318609" />


# ConsciousEngine - Autonomous Data Capsule Space (2026)

ConsciousEngine is a paradigm-shifting storage engine built from scratch. It abandons outdated database patterns, heavy transaction logging, and messy hash tables. Instead, it treats data as an **autonomous entity** that fuses with its physical/logical coordinates upon generation.

## Core Architecture & Paradigm Shift

* **Search Narrowing:** Data aligns directly with a macroscopic coordinate (`Storage / Layer / Row`), completely removing micro-management over disk blocks and bringing sessional search times down to zero.
* **No Memory Hash Tables:** The system DOES NOT maintain any key-value memory map or index array. It relies purely on direct filesystem routing, avoiding index-heavy RAM consumption.
* **The Capsule Model:** Every data chunk wraps itself between deterministic Start (`\x02`) and End (`\x03`) control characters. The data inherently limits and knows its own length.
* **Fused Identity Stamp:** During creation, the directory coordinates and exact byte sizes are permanently baked into the capsule's header.
* **Validation Loop:** Upon retrieval, the engine performs a check between the physical file location and the data's internal consciousness stamp. If a file was manually tampered with or moved, the engine rejects it instantly.

## Matrix Density Levels (1 - 5 Config)

The engine introduces a dynamic **Matrix Density** regulator that adapts the data's internal "knowledge" and operational speed:

1. **Level 1 (Macro Space / Max Speed):** Minimal headers, zero extra calculations. Raw payload is pushed directly to the disk instantly.
2. **Level 2 (Balanced - Default):** Standard operational velocity with strict hard-enforced physical disk synchronization (`os.fsync`) against write corruption.
3. **Level 3 (Deep Space):** Expands the data's awareness by embedding exact high-precision cryptographic creation timestamps.
4. **Level 4-5 (Atomic / Absolute Integrity):** Dense validation strata. Generates and embeds unique content checksums, verifying absolute byte integrity upon read execution.

## Collision Resolution (Sub-Index Stratum)

When multiple data bundles attempt to occupy the exact same coordinate row simultaneously, the system expands the row into sub-strata using an Excel-style endless index generator (`A`, `B`, `C` ... `Z`, then `A2`, `B2` ... `Z2`). 

Each bundle claims its exact available sub-index, burns it into its header metadata, and safely coexists side-by-side on the storage drive without any danger of overwriting.

## License

This project is protected and distributed under the **GNU Affero General Public License v3 (AGPLv3)**. See the LICENSE file for full core protection details.
