# Stoa Group Review Scraper

This repository contains a Python script that collects public reviews for a list of Stoa Group properties by scraping Google Maps via a headless Chrome browser.  The reviews are aggregated into a JSON array and delivered to a Domo webhook.

## Features

* **Automated scraping** – The script uses Selenium with an undetected Chrome driver to search Google Maps for each property, opens the reviews panel and extracts reviewer names, ratings and comments.  Any missing results are logged.
* **JSON output** – Reviews are normalised into a simple JSON schema containing the property name, review author, rating, review text and (where available) timestamp.  When scraping, timestamps may be unavailable and will be `null`.
* **Webhook delivery** – Once all properties have been processed, the JSON payload is pushed to the configured Domo webhook endpoint.  The payload is newline‑delimited JSON, which is accepted by Domo's inbound data API.
* **Weekly scheduling** – The module includes a scheduler loop that runs the scraping routine once per week.  You can disable this behaviour and integrate the `scrape_and_send` function into your own scheduling system if you prefer.

## Usage

1. **Clone the repository** and install the dependencies:

   ```bash
   git clone <this-repo-url>
   cd StoaGoogleReviewScraper
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Provide configuration**.  The script does not require any Google API credentials.  It only needs a Domo webhook URL.  Set the following environment variable before running the script:

   * `DOMO_WEBHOOK_URL` – the Domo webhook URL provided by Stoa Group.

   You can set this in your shell or by creating a `.env` file and loading it yourself.  If the variable is not set, the script will exit.

3. **Run the scraper**.  To run the scraper once immediately, execute:

   ```bash
   python StoaGoogleReviewScraper.py --once
   ```

   To run continuously and scrape every week, run the script without arguments:

   ```bash
   python StoaGoogleReviewScraper.py
   ```

4. **Cron integration**.  If you prefer a system‑level scheduler instead of the built‑in loop, you can set up a cron job that calls `python StoaGoogleReviewScraper.py --once` at the desired interval.

## Review Schema

Each entry in the JSON payload has the following fields:

| Key           | Description                                             |
|---------------|---------------------------------------------------------|
| `property`    | Name of the Stoa Group property                         |
| `author`      | Name of the reviewer as reported by Google             |
| `rating`      | Integer rating out of 5                                 |
| `text`        | The content of the review                               |
| `timestamp`   | ISO 8601 date/time when the review was posted (UTC), or `null` if unavailable |

Example:

```json
[
  {
    "property": "The Waters at Bluebonnet",
    "author": "Jane Smith",
    "rating": 5,
    "text": "Great apartments with friendly staff!",
    "timestamp": "2025-07-25T14:37:00"
  },
  {
    "property": "The Flats at East Bay",
    "author": "John Doe",
    "rating": 4,
    "text": "Nice complex, a bit noisy on weekends.",
    "timestamp": "2025-07-24T11:22:00"
  }
]
```

## Disclaimer

This project does not bypass any Google Terms of Service.  You must supply your own API key with appropriate permissions, and you are responsible for complying with Google's usage policies and the laws in your jurisdiction.  The scraping code simply requests data through the official API.