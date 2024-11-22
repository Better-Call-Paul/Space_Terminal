from asyncio import exceptions
import os
import aiohttp.connector
import aioredis
import requests
import logging
from datetime import timedelta, datetime, timezone
import asyncio
import aiohttp 
import certifi
from dataclasses import dataclass, field
from typing import Optional, List 
import json
from dotenv import load_dotenv
import logging 

from flask import Flask, render_template, jsonify, request, send_from_directory, send_file
from flask_socketio import SocketIO
from flask_cors import CORS

from aioredis import Redis 
from aioredis.exceptions import LockError



import aiohttp
import asyncio

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/data")
def call():
    return {"x" : ["x", "y"]}


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class RateLimitExceededError(Exception):
    "Exception raised for API Rate Limit errors "
    def __init__(self, message="Rate Limit Exceeded. Please try again later."):
        self.message = message
        super().__init__(self.message)
        
        
#GCRA algo with redis 
class RateLimiter:
    
    """
    Initialize the RateLimiter.

    :param limit: Maximum number of allowed requests within the period.
    :param redis_pool: Shared Redis connection pool.
    :param lock_timeout: Timeout for acquiring the Redis lock in seconds.
    :param default_ttl: Time-to-live for the rate limit key in seconds.
    """
    def __init__(self, limit: int, pool: Redis, lock_timeout: int = 10, default_time_to_live: int = 3600):
        self.pool = pool
        self.limit = limit 
        self.lock_timeout = lock_timeout
        self.default_ttl = default_time_to_live
        
        
    async def is_allowed(self, period: timedelta, key: str) -> bool:
        
        current_time = datetime.now(timezone.utc).timestamp()
        period_in_seconds = int(timedelta)
        inter_request_interval = period_in_seconds / self.limit 
        
        await self.redis.setnx(key, current_time)
        
        try:
            async with self.redis.lock(f"rate_limiter_lock:{key}", timeout=self.lock_timeout):
                theoretical_arrival_time_str = await self.redis.get(key)
                theoretical_arrival_time = float(theoretical_arrival_time_str) if theoretical_arrival_time_str else current_time
                
                delta = theoretical_arrival_time - current_time
                
                if delta > period_in_seconds:
                    new_theoretical_arrival_time = current_time + inter_request_interval
                    await self.redis.set(key, new_theoretical_arrival_time, ex=self.default_ttl)
                    return True
                    
                elif delta >= 0:
                    new_theoretical_arrival_time = max(theoretical_arrival_time, current_time) + inter_request_interval
                    await self.redis.set(key, new_theoretical_arrival_time, ex=self.default_ttl)
                    return True
                    
                else: 
                    return False
                    
        except exceptions.LockError:
            return False 
        
    
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
    
    def __init__(self, satellite_request: SatelliteRequest, redis_pool: aioredis.Redis, rate_limiter: RateLimiter):
        self.satellite_request = satellite_request
        self.redis_pool = redis_pool
        self.rate_limiter = rate_limiter
        
    async def fetch_from_api(
        self,
        endpoint: str,
        params: dict[str, any],
        cache_key: str,
        period: timedelta,
        expiration: int = 3600,
        retries: int = 3,
        backoff_factor: float = 0.5
    ) -> dict[str, any]:
        
        
        for attempt in range(1, retries + 1):
            try:

                allowed = await self.rate_limiter.is_allowed(cache_key, period)
                if not allowed:
                    raise RateLimitExceededError()

                # First check if data is in Redis cache
                cached_data = await self.redis.get(cache_key)
                if cached_data:
                    logger.info(f"Cache hit for key: {cache_key}")
                    return json.loads(cached_data)
                else:
                    logger.info(f"Cache miss for key: {cache_key}. Making API call.")

                params["apiKey"] = self.fetcher.API_KEY

                # Construct the full URL
                url = f"{self.fetcher.BASE_URL}{endpoint}"

                # Make the API request
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            # Store the response in Redis cache
                            await self.redis.set(cache_key, json.dumps(data), expire=expiration)
                            logger.info(f"API call successful for endpoint: {endpoint}")
                            return data
                        elif response.status == 429:

                            raise RateLimitExceededError("API responded with 429 Too Many Requests.")
                        else:
                            error_text = await response.text()
                            logger.error(f"HTTP Error {response.status}: {error_text}")
                            return {}
            except RateLimitExceededError as e:
                if attempt < retries:
                    wait_time = backoff_factor * (2 ** (attempt - 1))
                    logger.warning(f"Attempt {attempt}/{retries}: {e}. Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"Attempt {attempt}/{retries}: {e}. No more retries left.")
                    raise e
            except aiohttp.ClientError as e:
                if attempt < retries:
                    wait_time = backoff_factor * (2 ** (attempt - 1))
                    logger.warning(f"Attempt {attempt}/{retries}: Network error: {e}. Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"Attempt {attempt}/{retries}: Network error: {e}. No more retries left.")
                    return {}

        logger.error(f"All {retries} attempts failed for endpoint: {endpoint}")
        return {}
    
    async def get_tle(self) -> dict[str, any]:
        """Retrieve the Two Line Elements (TLE) for a satellite."""
        endpoint = f"tle/{self.fetcher.SAT_ID}"
        params = {}  
        cache_key = f"tle:{self.fetcher.SAT_ID}"
        period = timedelta(hours=1)  
        return await self.fetch_from_api(endpoint, params, cache_key, period)

    async def get_satellite_position(self) -> dict[str, any]:
        """Retrieve future positions of the satellite."""
        endpoint = f"positions/{self.fetcher.SAT_ID}/{self.fetcher.LAT}/{self.fetcher.LNG}/{self.fetcher.ALT}/{self.fetcher.SECONDS}"
        params = {}  
        cache_key = f"positions:{self.fetcher.SAT_ID}:{self.fetcher.LAT}:{self.fetcher.LNG}:{self.fetcher.ALT}:{self.fetcher.SECONDS}"
        period = timedelta(seconds=self.fetcher.SECONDS)  
        return await self.fetch_from_api(endpoint, params, cache_key, period)

    async def get_visual_passes(self) -> dict[str, any]:
        """Retrieve predicted visual passes for the satellite."""
        endpoint = f"visualpasses/{self.fetcher.SAT_ID}/{self.fetcher.LAT}/{self.fetcher.LNG}/{self.fetcher.ALT}/{self.fetcher.DAYS}/{self.fetcher.MIN_VISIBILITY}"
        params = {}  
        cache_key = f"visualpasses:{self.fetcher.SAT_ID}:{self.fetcher.LAT}:{self.fetcher.LNG}:{self.fetcher.ALT}:{self.fetcher.DAYS}:{self.fetcher.MIN_VISIBILITY}"
        period = timedelta(days=self.fetcher.DAYS) 
        return await self.fetch_from_api(endpoint, params, cache_key, period)

    async def get_radio_passes(self) -> dict[str, any]:
        """Retrieve predicted radio passes for the satellite."""
        endpoint = f"radiopasses/{self.fetcher.SAT_ID}/{self.fetcher.LAT}/{self.fetcher.LNG}/{self.fetcher.ALT}/{self.fetcher.DAYS}/{self.fetcher.MIN_ELEVATION}"
        params = {}  
        cache_key = f"radiopasses:{self.fetcher.SAT_ID}:{self.fetcher.LAT}:{self.fetcher.LNG}:{self.fetcher.ALT}:{self.fetcher.DAYS}:{self.fetcher.MIN_ELEVATION}"
        period = timedelta(days=self.fetcher.DAYS) 
        return await self.fetch_from_api(endpoint, params, cache_key, period)
    
    async def store_data_in_redis(self, key: str, data: dict[str, any], expiration: int = 3600):
        """Store arbitrary data in Redis."""
        await self.redis.set(key, json.dumps(data), expire=expiration)
        logger.info(f"Data stored in Redis under key: {key}")
    
    
                    
        
        

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
