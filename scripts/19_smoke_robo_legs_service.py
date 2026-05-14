from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.robo_legs_service import RoboLegsService


def main() -> None:
    service = RoboLegsService()

    timestamps = []
    try:
        timestamps = service.repo.list_timestamps("BOVA11")
    except Exception as exc:
        raise RuntimeError(f"falha ao listar timestamps: {exc}") from exc

    print("TIMESTAMPS ENCONTRADOS:", timestamps[:5])

    if timestamps:
        legs = service.get_legs("BOVA11", timestamps[0], validate=False)
        print("LEGS CARREGADAS:", [vars(leg) for leg in legs[:3]])
    else:
        print("SEM DADOS PARA BOVA11, MAS IMPORT/QUERY OK")

    print("ROBO LEGS SERVICE SMOKE OK")


if __name__ == "__main__":
    main()
