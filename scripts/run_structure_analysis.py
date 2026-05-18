import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.structure_analysis_service import StructureAnalysisService


def main():
    structure_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    reference_date = sys.argv[2] if len(sys.argv) > 2 else "2026-05-15"

    service = StructureAnalysisService()

    result = service.analyze(
        structure_id=structure_id,
        reference_date=reference_date,
        dte_min=None,
        spread_pct_medio=0.02,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
