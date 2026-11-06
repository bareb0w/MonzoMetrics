# Monzo Transaction Parser & Auto-Topup

## Setup

### 1. Configure Tailscale Funnel

First, configure a Tailscale Funnel to allow Monzo to redirect the OAuth callback to your server.

Run:

```bash
tailscale funnel --bg 8081
```

Take note of the HTTPS URL provided by Tailscale. You'll need this when configuring your OAuth application.

### 2. Create a Monzo OAuth application

Log into the [Monzo Developer Portal](https://developers.monzo.com/apps/home) and create a new **Confidential OAuth Client**.

Copy your `Client ID` and `Client Secret`.

Configure your redirect URL using your Tailscale Funnel address, including `/callback`.

For example:

```text
https://your-tailnet.ts.net/callback
```

### 3. Setup the environment

Create a python venv with:

```bash
python3 -m venv venv
```

And activate and install the requirements with:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Populate `.env` with your OAuth credentials and application configuration:

```env
CLIENT_SECRET=your_client_secret
CLIENT_ID=your_client_id
REDIRECT_URI=https://your-tailnet.ts.net/callback
```

### 5. Authenticate with Monzo

Run:

```bash
python3 monzo_auth_handler.py
```

Follow the browser login prompt and authorise the application.

Your OAuth tokens will be saved locally for subsequent API requests.

## Automated Balance Top-up

The application can automatically top up a designated Monzo account from a specified Pot when its balance falls below a configured target.

### Configuration

Configure the following variables in your `.env`:

```env
# Target balance in GBP
TARGET_BALANCE=100

# Day to top up (0 = Monday, 1 = Tuesday, etc.)
TOP_UP_DAY=0

# Account receiving the top-up
TARGET_ACCOUNT=acc_XXX

# Source Pot used to fund the top-up
SOURCE_POT=pot_XXX
```

### Scheduling with Cron

The top-up script can be scheduled using Cron.

Open the crontab editor:

```bash
crontab -e
```

Add the following entry, updating the path to your project and virtual environment:

```cron
0 4 * * 1 cd /path/to/project && /path/to/venv/bin/python3 -m card_topup.balance_top_up
```

This runs the top-up script every Monday at 04:00.

**Note:** Cron uses `0` for Sunday and `1` for Monday. This is separate from the `TOP_UP_DAY` environment variable, which uses `0` for Monday.

Ensure the Python script loads the `.env` file from the project directory, rather than relying on Cron's working directory.

## Security

Never commit your `.env` file or `monzo_tokens.json` to Git. These contain sensitive OAuth credentials and access tokens.

Only commit `.env.example` with placeholder values.