import os 

class Config:
    N2YO_API_KEY = os.getenv("N2YO_API_KEY")
    BASE_URL = 'https://api.n2yo.com/rest/v1/satellite'
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    RATE_LIMIT = int(os.getenv("RATE_LIMIT", 100))  
    RATE_PERIOD = int(os.getenv("RATE_PERIOD", 60))  
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")