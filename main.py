import sys
import logging
import time
import typer
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from codeforces_scraper import CodeforcesScraper

app = typer.Typer(help="A CLI tool to scrape Codeforces problems and contests.")
console = Console()


@app.command()
def scrape_problem(
    url: str = typer.Option(..., prompt="Enter the problem URL(e.g., https://codeforces.com/contest/2092/problem/B)", help="The URL of the Codeforces problem to scrape")
) -> None:
    """
    Scrape a single Codeforces problem.
    """
    scraper = CodeforcesScraper(problem_url=url, console=console)
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Scraping problem...", start=False)
        progress.start_task(task)
        try:
            scraper.scrape_problem()
            progress.update(task, description="Scraping complete!")
            time.sleep(0.5)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            raise typer.Exit(code=1)

@app.command()
def scrape_contest(
    url: str = typer.Option(..., prompt="Enter the contest URL(e.g., https://codeforces.com/contest/2092)", help="The URL of the Codeforces contest to scrape")
) -> None:
    """
    Scrape all problems from a Codeforces contest.
    """
    scraper = CodeforcesScraper(contest_url=url, console=console)
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Scraping contest...", start=False)
        progress.start_task(task)
        try:
            scraper.scrape_contest_problems()
            progress.update(task, description="Scraping complete!")
            time.sleep(0.5)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            raise typer.Exit(code=1)

def get_browser_choice() -> str:
    """
    Prompt the user to select a browser.
    """
    console.print("\n[bold]Select a browser:[/bold]\n")
    console.print("1. Chrome")
    console.print("2. Firefox")
    console.print("3. Exit\n")
    try:
        browser_choice = typer.prompt("Enter your choice", type=int)
    except Exception:
        console.print("[red]Invalid input. Exiting.[/red]")
        raise typer.Exit()
    if browser_choice == 1:
        return "chrome"
    elif browser_choice == 2:
        return "firefox"
    elif browser_choice == 3:
        console.print("Goodbye! 👋")
        raise typer.Exit()
    else:
        console.print("[red]Invalid choice. Please try again.[/red]")
        return get_browser_choice()

def main_menu() -> None:
    """
    Displays an interactive menu if no command is provided.
    """
    banner = Panel.fit(
        "[bold magenta]Welcome to Codeforces Scraper CLI![/bold magenta]\n"
        "[green]Scrape Codeforces problems and contests easily[/green]",
        title="[bold blue]Codeforces Scraper[/bold blue]",
        border_style="bright_blue",
        box=box.DOUBLE_EDGE,
    )
    console.print(banner)
    browser = get_browser_choice()

    console.print("\n[bold]Select an option:[/bold]\n")
    console.print("1. Scrape a single problem")
    console.print("2. Scrape a contest")
    console.print("3. Exit\n")
    try:
        choice = typer.prompt("Enter your choice", type=int)
    except Exception:
        console.print("[red]Invalid input. Exiting.[/red]")
        raise typer.Exit()

    if choice == 1:
        url = typer.prompt("Enter the problem URL(e.g., https://codeforces.com/contest/2092/problem/B)")
        scrape_problem_callback(url, browser)
    elif choice == 2:
        url = typer.prompt("Enter the contest URL(e.g., https://codeforces.com/contest/2092)")
        scrape_contest_callback(url, browser)
    elif choice == 3:
        console.print("Goodbye! 👋")
        raise typer.Exit()
    else:
        console.print("[red]Invalid choice. Please try again.[/red]")
        raise typer.Exit()

def scrape_problem_callback(url: str, browser: str) -> None:
    """
    Callback for scraping a single problem using the provided URL.
    """
    scraper = CodeforcesScraper(problem_url=url, console=console, browser=browser)
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Scraping problem...", start=False)
        progress.start_task(task)
        try:
            scraper.scrape_problem()
            progress.update(task, description="Scraping complete!")
            time.sleep(0.5)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

def scrape_contest_callback(url: str, browser: str) -> None:
    """
    Callback for scraping a contest using the provided URL.
    """
    scraper = CodeforcesScraper(contest_url=url, console=console, browser=browser)
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Scraping contest...", start=False)
        progress.start_task(task)
        try:
            scraper.scrape_contest_problems()
            progress.update(task, description="Scraping complete!")
            time.sleep(0.5)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
    )
    if len(sys.argv) == 1:
        main_menu()
    else:
        app()
