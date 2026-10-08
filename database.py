import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def get_db():
    # Create a fresh client every time to avoid stale connections
    return create_client(SUPABASE_URL, SUPABASE_KEY)