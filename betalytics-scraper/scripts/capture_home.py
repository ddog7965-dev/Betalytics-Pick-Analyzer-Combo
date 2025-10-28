#!/usr/bin/env python3
import asyncio
from betalytics_scraper.capture import run_capture

if __name__ == "__main__":
    asyncio.run(run_capture())
