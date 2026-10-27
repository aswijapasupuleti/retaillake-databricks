import os, shutil
import pandas as pd

base = "/Volumes/retail/bronze/raw_landing"
src  = f"{base}/olist_source"
land = f"{base}/landing"

START_DATE = "2017-10-01"   # dense period of the dataset
NUM_DAYS   = 30             # start small, rerun later with more days

orders   = pd.read_csv(f"{src}/olist_orders_dataset.csv")
items    = pd.read_csv(f"{src}/olist_order_items_dataset.csv")
payments = pd.read_csv(f"{src}/olist_order_payments_dataset.csv")

orders["day"] = orders["order_purchase_timestamp"].str[:10]
days = sorted(d for d in orders["day"].unique() if d >= START_DATE)[:NUM_DAYS]

# Static tables: copied once as an initial file
for name, f in [("customers", "olist_customers_dataset.csv"),
                ("products",  "olist_products_dataset.csv")]:
    os.makedirs(f"{land}/{name}", exist_ok=True)
    shutil.copy(f"{src}/{f}", f"{land}/{name}/{name}_initial.csv")

# Transactional tables: one file per day
for d in days:
    o = orders[orders["day"] == d].drop(columns="day")
    ids = set(o["order_id"])
    daily = {
        "orders":         o,
        "order_items":    items[items["order_id"].isin(ids)],
        "order_payments": payments[payments["order_id"].isin(ids)],
    }
    for name, df in daily.items():
        df = pd.concat([df, df.sample(frac=0.02, random_state=1)])  # ~2% duplicates
        os.makedirs(f"{land}/{name}", exist_ok=True)
        out = f"{land}/{name}/{name}_{d}.csv"
        if not os.path.exists(out):          # don't overwrite existing days
            df.to_csv(out, index=False)

print(f"Landed {len(days)} days of data")