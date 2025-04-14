# Changelog

**Repository:** `iris-api`\
**Description:** `Tracks all notable changes, version history, and roadmap toward 1.0.0 following Semantic Versioning.`\
**SPDX-License-Identifier:** `OGL-UK-3.0`

All notable changes to this repository will be documented in this file.
This project follows **Semantic Versioning (SemVer)** ([semver.org](https://semver.org/)), using the format:
 `[MAJOR].[MINOR].[PATCH]`
 - **MAJOR** (`X.0.0`) – Incompatible API/feature changes that break backward compatibility.
 - **MINOR** (`0.X.0`) – Backward-compatible new features, enhancements, or functionality changes.
 - **PATCH** (`0.0.X`) – Backward-compatible bug fixes, security updates, or minor corrections.
 - **Pre-release versions** – Use suffixes such as `-alpha`, `-beta`, `-rc.1` (e.g., `2.1.0-beta.1`).
 - **Build metadata** – If needed, use `+build` (e.g., `2.1.0+20250314`).

 ---

 ## Unreleased

 - Updated dependencies (2025-04-10)
 - The `/buildings` endpoint has been updated to expect viewport coordinates (e.g. a minimum and maximum longitude and latitude) rather than a geohash. It then generates a polygon from these coordinates, which is then used to run a GeoSPARQL query on a named graph.
 - The `/building/{uprn}` endpoint has been updated to run building-specific queries which fetch metadata about the roof, floors, walls etc. of the building. 
 - A new endpoint - `/epc-statistics/wards` - has been introduced, which queries a named graph to fetch the aggregated EPC statistics for the wards. 
 - A new `mappers.py` file has been introduced which exposes a set of functions mapping the responses received from the Secure Agent Graph to models.

 ## [0.90.1] – 2025-03-28

 ### Documentation

 - Updated NOTICE.md with correct formatting
 - Added endpoint to fetch user details
 - Added endpoint to fetch sign out links

 ---

 ## [0.90.0] – 2025-03-28

 ### Initial Public Release (Pre-Stable)

 This is the first public release of this repository under NDTP's open-source governance model.
 Since this release is **pre-1.0.0**, changes may still occur that are **not fully backward-compatible**.


 #### Initial Features
 - View a choropleth map, summarising average EPC ratings per ward
 - Search for a property via address
 - Filter properties based on EPC rating, building type, postcode, drawn area and flagged status
 - Filter properties based on further attributes (roof type, insulation type etc)
 - View details (roof type, EPC rating, insulation type etc) of properties
 - Download details of properties
 - Flag a property to signal it's under investigation
 - Unflagging a property with a rationale
 - Viewing the reason why a property was unflagged

 #### Known Limitations
 - Some components are subject to change before `1.0.0`.
 - APIs may evolve based on partner feedback and internal testing.

 ---

 ## Future Roadmap to `1.0.0`

 The `0.90.x` series is part of NDTP’s **pre-stable development cycle**, meaning:
 - **Minor versions (`0.91.0`, `0.92.0`...) introduce features and improvements** leading to a stable `1.0.0`.
 - **Patch versions (`0.90.1`, `0.90.2`...) contain only bug fixes and security updates**.
 - **Backward compatibility is NOT guaranteed until `1.0.0`**, though NDTP aims to minimise breaking changes.

 Once `1.0.0` is reached, future versions will follow **strict SemVer rules**.

 ## Versioning Policy  
1. **MAJOR updates (`X.0.0`)** – Typically introduce breaking changes that require users to modify their code or configurations.  
   - **Breaking changes (default rule)**: Any backward-incompatible modifications require a major version bump.  
   - **Non-breaking major updates (exceptional cases)**: A major version may also be incremented if the update represents a significant milestone, such as a shift in governance, a long-term stability commitment, or substantial new functionality that redefines the project’s scope.   
2. **MINOR updates (`0.X.0`)** – New functionality that is backward-compatible.  
3. **PATCH updates (`0.0.X`)** – Bug fixes, performance improvements, or security patches.  
4. **Dependency updates** – A **major dependency upgrade** that introduces breaking changes should trigger a **MAJOR** version bump (once at `1.0.0`).  
---
## How to Update This Changelog  
1. When making changes, update this file under the **Unreleased** section.  
2. Before a new release, move changes from **Unreleased** to a new dated section with a version number.  
3. Follow **Semantic Versioning** rules to categorise changes correctly.  
4. If pre-release versions are used, clearly mark them as `-alpha`, `-beta`, or `-rc.X`.  
---
**Maintained by the National Digital Twin Programme (NDTP).**  
© Crown Copyright 2025. This work has been developed by the National Digital Twin Programme and is legally attributed to the Department for Business and Trade (UK) as the governing entity.  
Licensed under the Open Government Licence v3.0.  
For full licensing terms, see [OGL_LICENSE.md](OGL_LICENSE.md).

