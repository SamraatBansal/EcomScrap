# EcomScrap

## Overview
EcomScrap is a tool designed to scrape e-commerce websites to extract structured product data such as product name, price, currency, and URL. It utilizes the Together API with the meta-llama/Llama-3.3-70B-Instruct-Turbo model for accurate data parsing. The tool performs web crawling using `crawl4ai` and integrates with SerpAPI for Google search results.

## Installation and CLI Guide

### Prerequisites
- Python 3.9+
- Virtual environment setup (recommended)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd EcomScrap
   ```
2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in a `.env` file:
   ```
   DESIRED_RESULT_LENGTH=3
   SERPAPI_API_KEY=<your-serpapi-key>
   TOGETHER_API_KEY=<your-together-api-key>
   SAVE_MARKDOWN_FILES=false
   LLM_MODEL=meta-llama/Llama-3.3-70B-Instruct-Turbo
   WEBOUTPUT_FILENAME=webOutput.json
   ```

### CLI Usage
Run the scraper with the following command:
```bash
python app.py --location "<country-code>" --query "<product-name>"
```

Example:
```bash
python app.py --location "JP" --query "matcha powder"
```

## Flow Explanation
1. **Search**: The tool uses SerpAPI to perform a Google search based on the provided location and product query.
2. **Crawling**: It uses `crawl4ai` to crawl the URLs obtained from the search results and extracts markdown content.
3. **Processing**: The markdown content is processed using the Together API to extract product information.
4. **Output**: The extracted data is sorted by price and saved to `result.json`. The console output is styled using `rich` for better readability.

## Example CLI Output

- Here's an example of the CLI output when running the scraper for "iphone 16 Pro, 128GB":
   ```bash
   python app.py --location "US" --query "iphone 16 Pro, 128GB"
   ```

   ```
   Scraped Products
   ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃ Name                ┃  Price ┃ Currency ┃ URL                                                                                                ┃
   ┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
   │ Apple iPhone 16 Pro │ 749.99 │   USD    │ https://www.amazon.com/Apple-iPhone-Version-128GB-Titanium/dp/B0DHJG6JPH                           │
   │ iPhone 16 Pro       │ 999.00 │   USD    │ https://www.apple.com/shop/buy-iphone/iphone-16-pro                                                │
   │ iPhone 16 Pro       │ 999.00 │   USD    │ https://www.apple.com/shop/buy-iphone/iphone-16-pro/6.3-inch-display-128gb-black-titanium-unlocked │
   └─────────────────────┴────────┴──────────┴────────────────────────────────────────────────────────────────────────────────────────────────────┘
   ```

  <img width="1274" alt="Screenshot 2025-07-07 at 5 36 45 AM" src="https://github.com/user-attachments/assets/88580837-a36c-4962-b785-6680062df170" />

- Searching for "Ola S1 Pro Electric" in India:
  ```bash
  python app.py --location "IN" --query "Ola S1 Pro Electric"
  ```
  
  Output:
  ```
  Scraped Products
  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
  ┃ Name                        ┃     Price ┃ Currency ┃ URL                                                             ┃
  ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
  │ OLA S1 Pro Electric Scooter │ 129999.00 │   INR    │ https://www.amazon.in/OLA-S1-Pro-Electric-Scooter/dp/B0DF2XPD8N │
  │ Ola S1 Pro+                 │  148999.0 │   INR    │ https://www.olaelectric.com/s1-pro                              │
  └─────────────────────────────┴───────────┴──────────┴─────────────────────────────────────────────────────────────────┘
  ```
  
   <img width="1263" alt="Screenshot 2025-07-07 at 5 51 00 AM" src="https://github.com/user-attachments/assets/5f9dac49-1a79-4390-8917-6c8ca1aafc16" />


- Searching for "matcha powder" in Japan:
  ```bash
  python app.py --location "JP" --query "matcha powder"
  ```
  Output:
  ```
  Performing CLI search for 'matcha powder' in location code 'JP'...
  Results successfully saved to webOutput.json
  Scraped Products
  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
  ┃ Name                                ┃ Price ┃ Currency ┃ URL                                                                       ┃
  ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
  │ Tsujiri Matcha Milk, 6.7 oz (190 g) │   984 │   JPY    │ https://www.amazon.co.jp/-/en/Green-Tea-Matcha-Powdered-Beverages/s?rh=n… │
  │ New Harvest Matcha 20g Can          │  3000 │   JPY    │ https://global.ippodo-tea.co.jp/collections/matcha                        │
  └─────────────────────────────────────┴───────┴──────────┴───────────────────────────────────────────────────────────────────────────┘
  Sorted results successfully saved to result.json
  ```
