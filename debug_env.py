# debug_env.py
import os
from dotenv import load_dotenv

print("Attempting to load .env file...")

# Load environment variables from a .env file
load_dotenv()

# Get the API key from the environment
key = os.getenv("PERPLEXITY_API_KEY")

# Check if the key was found and print the result
if key:
    print("\nSUCCESS: The API key was found successfully.")
    print(f"Loaded Key: {key[:8]}...{key[-4:]}") # Prints the start and end of the key
else:
    print("\nFAILURE: The API key was NOT found in the environment.")
    print("This means the .env file was not loaded correctly.")

print("\n--- Diagnostic Complete ---")
