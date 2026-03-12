# RoleplayCore Database Report

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue) ![License: MIT](https://img.shields.io/github/license/VoxCore84/roleplaycore-report) ![GitHub release](https://img.shields.io/github/v/release/VoxCore84/roleplaycore-report)

Database quality and optimization report for VoxCore (TrinityCore-based WoW 12.x server).

Generates a comprehensive analysis of world/characters/auth/hotfixes databases including:

- Schema validation and orphan detection
- Data quality scoring by category
- Cross-table referential integrity checks
- Optimization recommendations

## Usage

```bash
python build_site.py
```

## Output

Produces a static HTML report with interactive charts and filterable tables.

## License

MIT
