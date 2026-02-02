# 🤖 BotDiscordHero - Ragnarok Scraper Bot

A powerful Discord bot that scrapes and provides real-time Ragnarok Online information directly in Discord. Monitor item prices, track price changes, and search item details with interactive slash commands.

## ✨ Features

- **Item Search** (`/item`) - Get real-time item information from Ragnarok Online markets
- **Price Stalker** (`/stalker`) - Monitor item prices continuously and receive updates
- **Help System** (`/help`) - Access all available commands and their usage
- **Rich Embeds** - Beautiful formatted responses with item details and pricing
- **Real-time Data** - Scrapes live market data from Ragnarok Online sources
- **User Persistence** - Tracks monitored items per user with local storage

## 🛠️ Tech Stack

- **Python 3.11+** - Main programming language
- **discord.py** - Discord API wrapper
- **BeautifulSoup4** - Web scraping
- **Requests** - HTTP client
- **Pydantic** - Settings management
- **Poetry** - Dependency management

## 📋 Requirements

- Python 3.11 or higher
- Discord bot token
- Administrator/appropriate permissions in your Discord server
- Internet connection for scraping live data

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd BotDiscordHero
```

### 2. Install Dependencies

Using Poetry (recommended):
```bash
poetry install
```

Or using pip:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```
DISCORD_TOKEN=seu_token_aqui
OWNER_ID=seu_discord_id_aqui
```

**How to get your Discord Token:**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Name your bot
4. Go to "Bot" → "Add Bot"
5. Copy the token from "TOKEN"
6. Paste it in the `.env` file

**How to get your Discord ID:**
1. Enable "Developer Mode" in Discord (User Settings → Advanced → Developer Mode)
2. Right-click your username
3. Click "Copy User ID"
4. Paste it in the `.env` file as `OWNER_ID`

### 4. Configure Bot Permissions

Go to OAuth2 → URL Generator and select:
- **Scopes:** `bot`
- **Permissions:** 
  - Send Messages
  - Embed Links
  - Read Messages/View Channels

Copy the generated URL and open it in your browser to add the bot to your server.

## 🚀 Running the Bot

### Option 1: Direct Execution

Using Poetry:
```bash
poetry run python scraper_ragnarok/app.py
```

Or directly:
```bash
python scraper_ragnarok/app.py
```

### Option 2: Using Tasks

The project includes task commands configured in `pyproject.toml`:

```bash
# Development mode with auto-reload
task dev
```

### Option 3: Direct with Task
```bash
poetry run task dev
```

## 📝 Code Quality

The project uses several tools for code quality:

- **Ruff** - Fast Python linter and formatter
- **Pytest** - Unit testing framework
- **Pre-commit hooks** via taskipy

Run code quality checks:
```bash
# Lint check
task lint

# Auto-fix issues
task pre_format

# Format code
task format

```

## 📖 Comandos Disponíveis

### `/help`
Shows all available commands and their descriptions.

**Example:**
```
/help
```

### `/item <item_id> [max_value] [currency]`
Search for real-time item information from Ragnarok Online market.

**Parameters:**
- `item_id` (required) - The ID of the item to search
- `max_value` (optional) - Maximum price filter
- `currency` (optional) - Currency type for filtering

**Example:**
```
/item 547
```

**Returns:**
- Store name
- Refinement level
- Amount in ROP
- Value type
- Available quantity

### `/stalker <item_id> [interval] [max_value] [currency]`
Monitor an item's price and receive periodic updates about price changes.

**Parameters:**
- `item_id` (required) - The ID of the item to monitor
- `interval` (optional, default: 60) - Update interval in minutes
- `max_value` (optional) - Maximum price filter
- `currency` (optional) - Currency type for filtering

**Example:**
```
/stalker 547 120
```

This will monitor item 547 and send price updates every 120 minutes.

## 📁 Project Structure

```
BotDiscordHero/
├── scraper_ragnarok/
│   ├── app.py                          # Main bot entry point
│   ├── abstract/
│   │   ├── scrapers.py                 # Abstract scraper interfaces
│   │   └── storage.py                  # Abstract storage interfaces
│   ├── bot/
│   │   ├── commands/
│   │   │   ├── help/                   # Help command implementation
│   │   │   ├── item/                   # Item search command
│   │   │   └── stalker/                # Price stalker command
│   │   ├── services/                   # Business logic layer
│   │   ├── storage/                    # User data persistence
│   │   └── views/
│   │       ├── embeds/                 # Discord embed templates
│   │       └── templates/              # Response templates
│   ├── handlers/
│   │   └── exceptions/                 # Custom exceptions
│   ├── model/
│   │   └── settings.py                 # Configuration management
│   └── scraper/
│       └── extractor.py                # Web scraping logic
├── pyproject.toml                      # Project metadata & dependencies
├── requirements.txt                    # Pip requirements
├── README.md                           # This file
└── .env                                # Environment variables (do not commit)
```

## 🏗️ Architecture

The project follows a layered architecture pattern:

- **Commands Layer** - Discord slash commands (item, stalker, help)
- **Services Layer** - Business logic that processes commands
- **Storage Layer** - User data and monitored items persistence
- **Views Layer** - Discord embeds and response formatting
- **Scraper Layer** - Web scraping and data extraction
- **Model Layer** - Settings and configuration management
- **Handlers Layer** - Custom exceptions and error handling

## 🔐 Security

⚠️ **Important Security Notes:**

- **NEVER** share your `DISCORD_TOKEN`
- Always use `.env` to store credentials
- Add `.env` to `.gitignore` to prevent accidental commits
- Keep your `OWNER_ID` private
- Use environment variables for all sensitive data

## 🐛 Troubleshooting

### Bot doesn't respond?
- Verify the token is correct in `.env`
- Confirm the bot is added to the server
- Check bot permissions in server settings

### Connection error?
- Check your internet connection
- Try restarting the bot
- Check console for detailed error messages

### Item not found?
- Verify the item ID is correct
- Check if the Ragnarok website is accessible
- Try searching with a different item ID

### Bot commands not showing up?
- Use `/` to refresh the command list
- Check bot permissions (Send Messages, Embed Links)
- Wait a few moments for Discord to sync commands
- Restart the bot if commands still don't appear

### Project Dependencies

Key dependencies managed in `pyproject.toml`:
- `discord.py` (2.3.2+) - Discord bot framework
- `requests` (2.32.5+) - HTTP requests
- `beautifulsoup4` (4.14.3+) - HTML parsing
- `pydantic-settings` (2.12.0+) - Settings validation

## 📝 Notes

- The bot uses slash commands (`/command`)
- Information is fetched in real-time from the website
- Supports multiple stores per item
- User data is stored locally for stalker functionality
- The stalker feature runs in background tasks
- Market data is fetched dynamically on each request


Made with ❤️ for the Ragnarok community by [@jaydder](https://github.com/jaydder)
