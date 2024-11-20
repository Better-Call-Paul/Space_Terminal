import os
import requests
import logging
from datetime import timedelta
import asyncio
import aiohttp 
import certifi
from dataclasses import dataclass, field
from typing import Optional, List 
import json

import flask
import redis

from n2yoasync import N2YO, N2YOSatelliteCategory




#GCRA algo with reids 


import aiohttp
import asyncio


class RateLimiter:
    def __init__():
        pass
    
"""
Data Object to store fields for api calls for a specific satellite 
Raises a ValueError if its not initialized with an api key 
"""
@dataclass
class SatelliteFetcher:
    SAT_ID: int = 0
    LAT: float = 0.0
    LNG: float = 0.0
    ALT: int = 0
    SECONDS: int = 0
    # set repr = false, to avoid exposing api key in __repr__()
    API_KEY: Optional[str] = field(default=None, repr=False)
    BASE_URL: str = field(default=None)
    
    def __post_init__(self):
        if not self.API_KEY:
            raise ValueError("Usage: API Key Required\n")
    
    


async def fetch_satellite_data(input: SatelliteFetcher) -> dict:
    
    url = f"{input.BASE_URL}/positions/{input.SAT_ID}/{input.LAT}/{input.LNG}/{input.ALT}/{input.SECONDS}/&apiKey={input.API_KEY}"
    # Create an aiohttp session with SSL verification disabled
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"HTTP Error: {response.status} - {await response.text()}")
    

async def main():

    
    data_client = SatelliteFetcher(
        API_KEY = os.getenv("N2YO_API_KEY"),
        BASE_URL = 'https://api.n2yo.com/rest/v1/satellite',
        SAT_ID = 25544,  # Example satellite ID (ISS)
        LAT = 40.7128,   # Example latitude
        LNG = -74.0060,  # Example longitude
        ALT = 0,         # Altitude of your observation point
        SECONDS = 300,   # Number of seconds to predict
    )
        
    try:
        data = await fetch_satellite_data(data_client)
        print(data)
        print(type(data))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
