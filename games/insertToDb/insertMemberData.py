from games.models import Brands
from datetime import datetime

# Data extracted from the table
brands_data = [
    {"name": "AIBots", "total_value": 500, "total_tokens": 1000000, "token_prices": 0.0005},
    {"name": "magic worlds", "total_value": 500, "total_tokens": 1000000, "token_prices": 0.0005},
    {"name": "MemeWorld", "total_value": 250, "total_tokens": 1000000, "token_prices": 0.00025},
    {"name": "Other", "total_value": 250, "total_tokens": 1000000, "token_prices": 0.00025},
]

# Create and save the data
for data in brands_data:
    brand = Brands(
        name=data["name"],
        total_value=data["total_value"],
        total_tokens=data["total_tokens"],
        token_prices=data["token_prices"],
        started_date=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    brand.save()
