import os
from dotenv import load_dotenv


load_dotenv()


LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek")
MAX_STEPS = int(os.getenv("MAX_STEPS", "5"))