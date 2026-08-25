from pathlib import Path
from datetime import datetime



REPORT_DIR = Path(
    "storage/reports"
)



def generate_report(
    mission_id: str,
    data: dict,
):

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


    filename = (
        f"report_{mission_id}.txt"
    )


    path = (
        REPORT_DIR /
        filename
    )


    content = f"""
HORUS REPORT

Mission:
{mission_id}


Generated:
{datetime.now()}


Data:

{data}

"""


    path.write_text(
        content,
        encoding="utf-8"
    )


    return str(path)
