import asyncio
import json
import sys
from pathlib import Path

from loguru import logger

from pipeline.adapters import adapters

BASE_DIR = Path(__file__).parent.parent


async def main(source: str = "REDDIT"):
    adapter = adapters[source]
    result = await adapter()
    logger.info(f"Done.\n{json.dumps(result, indent=2)}")
    return result


if __name__ == "__main__":
    asyncio.run(main((sys.argv[1:2] or ["REDDIT"])[0]))
