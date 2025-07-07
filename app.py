import asyncio
import json
import argparse
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from search import perform_search
from crawler import crawl_streaming

load_dotenv()
console = Console()

# --- Main Execution Block ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the EcomScrap search tool in CLI mode.")
    parser.add_argument("--location", type=str, required=True, help="The two-letter country code for the search location (e.g., 'US', 'CA', 'UK', 'IN')")
    parser.add_argument("--query", type=str, required=True, help="The product to search for.")

    args = parser.parse_args()

    console.print(f"Performing CLI search for '[bold cyan]{args.query}[/bold cyan]' in location code '[bold cyan]{args.location}[/bold cyan]'...")

    search_results = perform_search(args.location, args.query)

    if "error" in search_results:
        console.print(f"[bold red]Error:[/] {search_results['error']}")
        exit()

    output_file = os.getenv("WEBOUTPUT_FILENAME", "webOutput.json")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(search_results, f, indent=2, ensure_ascii=False)
        console.print(f"Results successfully saved to [bold green]{output_file}[/bold green]")
    except IOError as e:
        console.print(f"[bold red]Error:[/] Failed to write to {output_file}. Reason: {e}")

    if 'organic_results' in search_results:
        urls_to_crawl = [result['link'] for result in search_results['organic_results']]
        desired_result_length = int(os.getenv("DESIRED_RESULT_LENGTH", 5)) * 2
        urls_to_crawl = urls_to_crawl[:desired_result_length]

        sorted_results_list = asyncio.run(crawl_streaming(urls_to_crawl, args.query))

        if sorted_results_list:
            table = Table(title="Scraped Products")
            table.add_column("Name", justify="left", style="cyan", no_wrap=True)
            table.add_column("Price", justify="right", style="magenta")
            table.add_column("Currency", justify="center", style="green")
            table.add_column("URL", justify="left", style="yellow")

            for item in sorted_results_list:
                table.add_row(item['name'], str(item['price']), item['currency'], item['url'])

            console.print(table)

            with open('result.json', 'w', encoding='utf-8') as result_file:
                json.dump(sorted_results_list, result_file, indent=2)
            console.print("Sorted results successfully saved to [bold green]result.json[/bold green]")
        else:
            console.print("[yellow]No products could be extracted from the crawled pages.[/yellow]")
