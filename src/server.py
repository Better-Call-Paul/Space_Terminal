import os
import requests
import logging
from datetime import timedelta
import asyncio
import aiohttp 
import aioredis
import certifi
from dataclasses import dataclass, field
from typing import Optional, List 
import json
from dotenv import load_dotenv

from flask import Flask, render_template, jsonify, request, send_from_directory, send_file
from flask_socketio import SocketIO
from flask_cors import CORS
 
import redis

from n2yoasync import N2YO, N2YOSatelliteCategory


import aiohttp
import asyncio

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/data")
def call():
    return {"x" : ["x", "y"]}


#GCRA algo with reids 
class RateLimiter:
    def __init__(self, limit: int, pool):
        self.limit = limit
        self.pool = pool
        
    """
    Returns whether or not a request is within the rate limit
    Utilizes the GCRA algorithm
    """
    def check_allowed(self, key: str, period: timedelta) -> bool:
        
        
        pass
        
    
"""
Data Object to store fields for api calls for a specific satellite 
Raises a ValueError if its not initialized with an api key 
"""
@dataclass
class SatelliteRequest:
    SAT_ID: Optional[int] = None
    LAT: Optional[float] = None
    LNG: Optional[float] = None
    ALT: Optional[int] = None
    SECONDS: Optional[int] = None
    DAYS: Optional[int] = None
    MIN_VISIBILITY: Optional[int] = None 
    # set repr = false, to avoid exposing api key in __repr__()
    API_KEY: str = field(default=None, repr=False)
    BASE_URL: str = field(default=None)
    
    
    def __post_init__(self):
        if not self.API_KEY:
            raise ValueError("Usage: API Key Required\n")
        if not self.BASE_URL:
            raise ValueError("Usage: URL is Required")
    
    @staticmethod
    def for_identify_satellite(sat_id: int):
        """
        Factory method to create request object for TLE retrieval API call
        """
        return SatelliteRequest(SAT_ID=sat_id)
    
    @staticmethod
    def for_satellite_position(sat_id: int, observer_lat: float, observer_lng: float, observer_alt: float, seconds: int):
        """
        Factory method to create request object for satellite position API call
        """
        return SatelliteRequest(
            SAT_ID=sat_id,
            LAT=observer_lat,
            LNG=observer_lng,
            ALT=observer_alt,
            SECONDS=seconds
        )
        
    @staticmethod
    def for_satellite_visual_pass(sat_id: int, observer_lat: float, observer_lng: float, observer_alt: float, days: int, min_visibility: int):
        """
        Factory method to create request object for predicted visual passes for any satellite relative to a location on earth
        """
        return SatelliteRequest(
            SAT_ID=sat_id,
            LAT=observer_lat,
            LNG=observer_lng,
            ALT=observer_alt,
            DAYS=days,
            MIN_VISIBILITY=min_visibility
        )
        
    @staticmethod
    def for_radio_passes(sat_id: int, observer_lat: float, observer_lng: float, observer_alt: float, days: int, min_elevation: int, api_key: str):
        """
        Factory method to create request object for radio passes 
        """
        return SatelliteRequest(
            SAT_ID=sat_id,
            LAT=observer_lat,
            LNG=observer_lng,
            ALT=observer_alt,
            DAYS=days,
            MIN_ELEVATION=min_elevation,
            API_KEY=api_key
        )

    
    
    
class SatelliteAPIClient:
    
    def __init__(self, satellite_fetcher: SatelliteRequest, redis_url: str = "redis://localhost"):
        self.fetcher = satellite_fetcher
        self.redis = None
        self.redis_url = redis_url
        
    async def fetch_from_api(
        self,
        endpoint: str,
        params: dict[str, any],
        cache_key: str, 
        expiration: int = 3600,
        retries: int = 3,
        backoff_factor: float = 0.5
    ) -> dict[str, any]:
        pass
                    
        
        

async def main():

    N2YO_API_KEY = os.getenv("N2YO_API_KEY")
    
    """
    data_client = SatelliteRequest(
        API_KEY = N2YO_API_KEY,
        BASE_URL = 'https://api.n2yo.com/rest/v1/satellite',
        SAT_ID = 25544,  # Example satellite ID (ISS)
        LAT = 40.7128,   # Example latitude
        LNG = -74.0060,  # Example longitude
        ALT = 0,         # Altitude of your observation point
        SECONDS = 300,   # Number of seconds to predict
    )
    
    client = SatelliteAPIClient(data_client)
        
    try:
        data = await client.get_satellite_position()
        print(data)
        print(type(data))
        for key, value in data.items():
            print(f"Key: {key}, Type: {type(value)}")
            for v in value:
                print(type(v))
                for p in v:
                    print(p)
                    
        print(data.keys())
    except Exception as e:
        print(f"An error occurred: {e}")
    """

if __name__ == "__main__":
    asyncio.run(main())
    #app.run(debug=True)
