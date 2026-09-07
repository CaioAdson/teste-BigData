import json
import os
import random
import time
import uuid
from datetime import datetime, timezone

EVENTS = ["click", "add_to_cart", "purchase", "delivery_update"]
CATEGORIES = ["eletronicos", "livros", "casa", "moda", "esportes"]
REGIONS = ["CE", "SP", "RJ", "PE", "BA"]
OUTPUT = os.getenv("EVENT_FILE", "/data/events.jsonl")
INTERVAL = float(os.getenv("EVENT_INTERVAL_SECONDS", "1"))


def create_event():
    event_type = random.choices(EVENTS, weights=[55, 22, 15, 8], k=1)[0]
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "user_id": f"user-{random.randint(1, 100)}",
        "product_id": f"product-{random.randint(1, 20)}",
        "category": random.choice(CATEGORIES),
        "price": round(random.uniform(10, 1500), 2),
        "quantity": random.randint(1, 3),
        "region": random.choice(REGIONS),
        "delivery_status": random.choice(["preparing", "shipped", "delivered"])
        if event_type == "delivery_update"
        else None,
        "event_time": datetime.now(timezone.utc).isoformat(),
    }


os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
print(f"Gerando eventos em {OUTPUT}", flush=True)
while True:
    event = create_event()
    line = json.dumps(event, ensure_ascii=False)
    with open(OUTPUT, "a", encoding="utf-8") as file:
        file.write(line + "\n")
    print(line, flush=True)
    time.sleep(INTERVAL)
