<img width="1254" height="1254" alt="28CDA1F0-4302-4AD7-9685-3463989AC51B" src="https://github.com/user-attachments/assets/77bcd180-c886-4c8f-8593-aaefcf75d41b" />

<img width="750" height="497" alt="consciousdata" src="https://github.com/user-attachments/assets/eb176d36-0c23-4ae5-ac52-c13ff8318609" />

# ConsciousEngine - Autonomous Data Capsule Space (2026)

ConsciousEngine is a minimalist, high-integrity storage engine archetype that abandons traditional monolithic database patterns, global index maintenance, and runtime hash tables. Instead, it encapsulates data chunks into **Autonomous Data Capsules**—self-describing, location-aware binary structures that actively validate their own contextual and physical integrity.

## Core Architectural Concepts

*   **Location-Aware Cryptographic/Coordinate Stamps:** Every capsule hardcodes its intended physical coordinates (`storage`, `layer`, `row`, `sub_index`) directly into its binary header. The data knows exactly where it belongs.
*   **Zero Global Index Overhead:** Rather than querying central index tables or B-trees to resolve queries, the engine relies on predictable matrix-coordinate generation. 
*   **Density-Driven Engine Behavior:** The persistence, security, and metadata depth scale dynamically based on a strict `density` layout configuration (Levels 1–5).

---

## Technical Specifications & Features

### 1. Capsule Format Anatomy
A capsule is generated as a unified, immutable binary block:
`[START_MARKER]` ➔ `[META_LENGTH]` ➔ `[JSON_METADATA]` ➔ `[RAW_PAYLOAD]` ➔ `[END_MARKER]`

### 2. Density Levels (Strict Scaling)
The engine behavior modifies itself seamlessly based on the runtime `density` setting:
*   **Density ≥ 2 (Hardware Enforcement):** Bypasses OS write-buffering. Every single write operation triggers a strict file descriptor flush and hardware barrier sync (`fsync`) directly to physical storage. This eliminates the necessity of standard transactional write-ahead logs (WAL).
*   **Density ≥ 3 (Temporal Integration):** Injects precise UNIX epoch micro-timestamps into the local capsule metadata for temporal tracking.
*   **Density ≥ 4 (Active Integrity / Immunization):** Computes and binds an internal checksum of the raw payload. 

### 3. Verification Loop & Relocation Anomalies
During extraction, the capsule undergoes a reverse verification loop. If a capsule is manually moved, renamed, or tampered with on the disk, the engine detects a structural drift and raises a `RuntimeError ("Relocation anomaly: internal coordinate stamp mismatch")`. The data refuses to compile if it is not in its rightful location.

---

## Production Disclaimer (Simulation vs. Raw Metal)

> [!NOTE]
> This repository acts as a **High-Level Architectural Simulation (Proof of Concept)** written in Python. It maps coordinates to directory paths via standard I/O abstractions. 
> 
> The native production design (intended for C/Rust implementation) is architected to operate directly on **Raw Block Devices**. By bypassing the OS filesystem completely, capsules write directly to physical sectors via logical block addressing (LBA), completely eliminating standard partition overhead and underlying filesystem hash tables.

---

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**. 
For more details, see the official GNU documentation.
