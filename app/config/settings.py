import os
from dotenv import load_dotenv

load_dotenv()

if os.environ.get("OPENAI_API_KEY"):
    print("✅ API Key loaded successfully.")
else:
    print("❌ API Key NOT found. Check your .env file.")

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
JWT_SECRET_KEY="T0OojyNpFx1lwKJTUXd648vwfnRuFyMNt4TVWgDvFaK8FlbV5F8TR8ggkvQuSOVhn_PijFBcbeY1N7ac3NLMqA"
JWT_ALGORITHM="HS256"
JWT_EXPIRE_MINUTES=60

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))