import asyncio
import asyncpg
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, inspect

# Import your existing config and model
from app.config import settings
from app.models import Base, MapBankCampaignData

def generate_mock_row(index: int) -> dict:
    """Generates a realistic BFSI customer row, dynamically filling the 200+ columns."""
    
    # 1. Core identifiable & demographic data (explicitly defined)
    row = {
    "unique_customer_id": f"CUST{random.randint(10000000, 99999999)}",
    "bankid": random.randint(1, 5),
    "bank": random.choice(["HDFC", "ICICI", "SBI", "AXIS", "KOTAK"]),
    "membershipno": random.randint(1000000000, 9999999999),
    "firstname": random.choice(["Rajesh", "Priya", "Amit", "Sneha", "Vikram", "Anjali"]),
    "middlename": random.choice(["Kumar", "Devi", "Singh", None]),
    "lastname": random.choice(["Sharma", "Patel", "Reddy", "Iyer", "Gupta"]),
    "dateofbirth": datetime(1960, 1, 1) + timedelta(days=random.randint(0, 20000)),
    "gender": random.choice(["M", "F", "Other"]),
    "age": round(random.uniform(18, 70), 1),
    "res_city": random.choice(["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Pune"]),
    "res_state": random.choice(["Maharashtra", "Delhi", "Karnataka", "Telangana", "Tamil Nadu"]),
    "pin": str(random.randint(100000, 999999)),
    "mobile_valid": random.randint(0, 1),
    "email_valid": random.randint(0, 1),
    "mobile": f"98{random.randint(10000000, 99999999)}",
    "email": f"user{index}@testbank.com",
    "cardtype": random.choice(["Credit", "Debit"]),
    "islive": random.choice([True, False]),
    "enrollmentdate": datetime(2015, 1, 1) + timedelta(days=random.randint(0, 3000)),
    "txn": random.randint(10, 1000),
    "spend": round(random.uniform(5000, 500000), 2),
    "atv": round(random.uniform(500, 5000), 2),
    "firsttxndate": datetime(2018, 1, 1) + timedelta(days=random.randint(0, 2000)),
    "lasttxndate": datetime(2023, 1, 1) + timedelta(days=random.randint(0, 500)),
    "dnd": random.randint(0, 1),
    "reject_flag": random.randint(0, 1),
    "NRI_flag": random.randint(0, 1),
}

    # Dynamically fill remaining columns based on naming patterns
    mapper = inspect(MapBankCampaignData)
    for column in mapper.columns:
        col_name = column.name
        if col_name in row:
            continue
        
        col_type = str(column.type).lower()
        
        if "score" in col_name:
            row[col_name] = round(random.uniform(0.1, 0.95), 4)
        elif "txn" in col_name or "count" in col_name or "redemptions" in col_name:
            row[col_name] = random.randint(0, 50)
        elif "spend" in col_name or "amount" in col_name or "atv" in col_name or "point" in col_name:
            row[col_name] = round(random.uniform(100, 25000), 2)
        elif "date" in col_name or "dt" in col_name:
            if "date" in col_type:
                row[col_name] = (datetime.now() - timedelta(days=random.randint(1, 1000))).date()
            else:
                row[col_name] = datetime.now() - timedelta(days=random.randint(1, 1000))
        elif any(x in col_name for x in ["flag", "valid", "active", "dormant", "nevercontactless", "reachable"]):
            row[col_name] = random.randint(0, 1)
        elif "boolean" in col_type:
            row[col_name] = random.choice([True, False])
        elif "bigint" in col_type or "integer" in col_type:
            row[col_name] = random.randint(0, 100)
        elif "numeric" in col_type or "real" in col_type:
            row[col_name] = round(random.uniform(0, 1000), 2)
        elif "varchar" in col_type or "character" in col_type:
            row[col_name] = random.choice(["Active", "Inactive", "N/A", "Yes", "No", None])
        else:
            row[col_name] = None

    return row

async def seed_database():
    print("🚀 Starting Database Seeding Process...")
    
    # TWO different URLs needed:
    # 1. SQLAlchemy needs the +psycopg driver suffix
    sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql+psycopg://")

    # 2. asyncpg needs a plain postgresql:// URL
    async_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

    print(f"🔌 Connecting to: {async_url.split('@')[1] if '@' in async_url else async_url}")

    sync_engine = create_engine(sync_url)

    print("📦 Creating schema and tables (if not exists)...")
    Base.metadata.create_all(sync_engine)
    print("✅ Schema `marketingdb` and table `map_bank_campaign_data` ready.")

    print("⏳ Generating 10,000 mock records...")
    records = [generate_mock_row(i) for i in range(10000)]

    print("⚡ Inserting records via asyncpg...")
    conn = await asyncpg.connect(async_url)  # <-- Use plain postgresql:// URL
    try:
        columns = [col.name for col in inspect(MapBankCampaignData).columns]
        
        values = [tuple(record.get(col) for col in columns) for record in records]
        
        await conn.copy_records_to_table(
            "map_bank_campaign_data",
            records=values,
            columns=columns,
            schema_name="marketingdb",
            timeout=60
        )
        print("🎉 Successfully inserted 10,000 rows!")
        
        row_count = await conn.fetchval("SELECT COUNT(*) FROM marketingdb.map_bank_campaign_data")
        print(f"🔍 Verification: Table now contains {row_count} rows.")
        
    except Exception as e:
        print(f"❌ Error during insertion: {type(e).__name__}: {e}")
        raise
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(seed_database())