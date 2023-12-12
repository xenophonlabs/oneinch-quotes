"""
Provides configuration for database and helpers.
"""

import os
from dotenv import load_dotenv
from .tokens import TOKEN_DTOs

load_dotenv()

username = os.getenv("PG_USERNAME")
password = os.getenv("PG_PASSWORD")
database = os.getenv("PG_DATABASE")

URI = (
    f"postgresql://{username}:{password}@localhost/{database}"  # defaults to port 5432
)

# Convenience maps
ADDRESS_TO_SYMBOL = {k: v.symbol for k, v in TOKEN_DTOs.items()}
SYMBOL_TO_ADDRESS = {v.symbol: k for k, v in TOKEN_DTOs.items()}
