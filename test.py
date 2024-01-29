from dotenv import load_dotenv
import os                   # para operaciones del sistema operativo  

load_dotenv()
API_KEY = os.getenv("API_KEY")
print(API_KEY)