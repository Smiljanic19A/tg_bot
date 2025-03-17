from DexService import DexService
import json
import os
from TelegramService import TelegramService
import time
import schedule

def load_existing_tokens():
    """Load previously saved tokens from the JSON file if it exists."""
    filename = "token_profiles.json"
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            # If the file exists but is empty or invalid JSON
            return []
    return []

def save_tokens(tokens):
    """Save tokens to the JSON file."""
    filename = "token_profiles.json"
    with open(filename, 'w') as file:
        json.dump(tokens, indent=4, fp=file)

def get_token_key(token):
    """Create a unique key for a token based on chainId and tokenAddress."""
    return f"{token.get('chainId')}:{token.get('tokenAddress')}"

def check_for_new_tokens():
    print(f"\nChecking for new tokens at {time.strftime('%Y-%m-%d %H:%M:%S')}...")
    
    # Initialize DexService
    dex_service = DexService()

    # Get latest token profiles from the API
    new_token_profiles = dex_service.get_latest_token_profiles()

    # Load existing tokens
    existing_tokens = load_existing_tokens()

    # Create a set of existing token keys for faster lookup
    existing_token_keys = {get_token_key(token) for token in existing_tokens}

    # Filter out tokens that we've already seen
    new_unique_tokens = []
    for token in new_token_profiles:
        token_key = get_token_key(token)
        if token_key not in existing_token_keys:
            new_unique_tokens.append(token)
            existing_tokens.append(token)

    # Save all tokens (including new ones)
    save_tokens(existing_tokens)

    # Print information about what we found
    print(f"Found {len(new_token_profiles)} tokens in the API response")
    print(f"Added {len(new_unique_tokens)} new unique tokens")
    print(f"Total unique tokens saved: {len(existing_tokens)}")

    # Print the new unique tokens for inspection
    if new_unique_tokens:
        print("\nNew unique tokens:")
        print(json.dumps(new_unique_tokens, indent=4))
    else:
        print("\nNo new unique tokens found in this API response.")

    # Send Telegram messages for new tokens
    telegram_service = TelegramService()

    for token in new_unique_tokens:
        time.sleep(3)  # Wait 3 seconds between messages
        telegram_service.send_message(token.get('chainId'), token.get('name'), token.get('url'))

if __name__ == "__main__":
    # Run the function immediately once
    check_for_new_tokens()
    
    # Schedule to run every 4 minutes
    schedule.every(1).minutes.do(check_for_new_tokens)
    
    print(f"\nScheduler started at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("Script will check for new tokens every 1 minutes")
    print("Keep this window open to continue running")
    print("Press Ctrl+C to stop")
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped by user")


