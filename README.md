# Telegram AutoPoster

Simple Python script for automatically posting messages to Telegram channels at scheduled times using **Telethon**.

## Features

- Scheduled message posting
- Support for multiple channels
- Uses Telegram **user account** (not a bot)
- Simple configuration
- Environment variables for API credentials

## Requirements

- Python 3.9+
- Telegram API credentials
- Telethon

Install dependencies:

```bash
pip install telethon python-dotenv
```

## Setup

Create `.env` file:

```
APP_ID=your_api_id
APP_HASH=your_api_hash
PHONE_NUMBER=+123456789
```

Create `post.txt` with the message you want to send.

Example:

```
Hello, this message was sent automatically.
```

## Usage

Edit posting times in the script:

```python
time_to_send = [[13, 57], [14, 53], [18, 30]]
```

Run:

```bash
python main.py
```

The script will send the content of `post.txt` to configured channels at the specified times.

## Channel Configuration

You can manually specify channel IDs:

```python
self.channels = [-1001234567890]
```

Or automatically fetch channels from the account.

## Disclaimer

Use responsibly. Excessive automation may violate Telegram terms.

## License

MIT