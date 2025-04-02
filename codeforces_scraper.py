import logging
import re
from typing import Any, Dict
from bs4 import BeautifulSoup

from utils import clean_text, fetch_page, save_data

# Configure logging (you can also configure this in main.py if preferred)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')

class CodeforcesScraper:
    def __init__(self, contest_url: str = "", problem_url: str = "", console= None) -> None:
        """
        Initialize the scraper with a problem URL.
        """
        self.contest_url: str = contest_url
        self.editorial_url: str = ""
        self.problem_url: str = problem_url
        self.problem_data: Dict[str, Any] = {}
        self.solution_data: Dict[str, Any] = {}

        self.console = console

    def scrape_problem_statement(self) -> None:
        """
        Scrape problem details from the Codeforces problem page.
        """
        html_content = fetch_page(self.problem_url)
        if not html_content:
            raise Exception("Failed to fetch problem page")

        soup = BeautifulSoup(html_content, 'html.parser')

        # Scrape problem title
        title_div = soup.find('div', class_='title')
        if not title_div:
            raise Exception("Could not find problem title")
        self.problem_data['title'] = clean_text(title_div.text)

        # Scrape problem statement description
        problem_statement = soup.find('div', class_='problem-statement')
        if not problem_statement:
            raise Exception("Could not find problem statement")

        header = problem_statement.find('div', class_='header')
        if header:
            description = header.find_next_sibling('div')
            self.problem_data['description'] = clean_text(description.text if description else "")

        # Scrape input/output specifications
        for spec in ['input', 'output']:
            elem = soup.find('div', class_=f'{spec}-specification')
            self.problem_data[spec] = clean_text(elem.text if elem else "")

        # Scrape limits
        time_limit_div = soup.find('div', class_='time-limit')
        self.problem_data['time_limit'] = clean_text(time_limit_div.contents[-1] if time_limit_div else "")

        memory_limit_div = soup.find('div', class_='memory-limit')
        self.problem_data['memory_limit'] = clean_text(memory_limit_div.contents[-1] if memory_limit_div else "")

        # Scrape tags
        self.problem_data['tags'] = [clean_text(tag.text) for tag in soup.find_all('span', class_='tag-box')]

        # Scrape examples
        self.problem_data['examples'] = []
        examples = soup.find_all('div', class_='sample-test')
        for example in examples:
            input_data = example.find('div', class_='input')
            output_data = example.find('div', class_='output')
            if input_data and output_data:
                input_text = clean_text(input_data.text.replace('Input\n', '').replace('InputCopy', ''))
                output_text = clean_text(output_data.text.replace('Output\n', '').replace('OutputCopy', ''))
                self.problem_data['examples'].append({'input': input_text, 'output': output_text})

        if not self.editorial_url:
            # Find tutorial link
            tutorial_link = None
            for a_tag in soup.find_all('a'):
                if 'Tutorial' in a_tag.get_text():
                    tutorial_link = a_tag
                    break

            if tutorial_link and tutorial_link.get('href'):
                self.editorial_url = "https://codeforces.com" + tutorial_link['href']
            else:
                logging.info("Tutorial link not found")

    def scrape_problem_solution(self) -> None:
        """
        Scrape solution details from the Codeforces tutorial page.
        """
        if not self.editorial_url:
            logging.info("No solution URL available")
            return

        html_content = fetch_page(self.editorial_url)
        if not html_content:
            logging.info("Failed to fetch solution page")
            return

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the problem link in the tutorial page to locate the solution section
        problem_link = soup.find('a', href=re.compile(self.problem_url.replace('https://codeforces.com', '')))
        if not problem_link:
            logging.info("Could not locate problem in tutorial")
            return

        problem = problem_link.find_parent()
        solution_title = problem.find_next('b', string=lambda text: text and 'Solution' in text)
        if not solution_title:
            logging.info("Could not find Solution section")
            return

        solution_description = solution_title.find_next_sibling('div')
        if solution_description:
            self.solution_data['description'] = clean_text(solution_description.text.strip())

            # Find code blocks
            solution_code = solution_description.find_next('b', string=lambda text: text and ('Python' in text or 'python' in text))
            if solution_code is None:
                solution_code = solution_description.find_next('b', string=lambda text: text and ('Code' in text or 'code' in text))
            if solution_code:
                code_block = solution_code.find_next_sibling('div')
                if code_block:
                    self.solution_data['code'] = code_block.text

    def scrape_problem(self) -> None:
        """
        Perform the scraping of problem and solution details.
        """
        self.scrape_problem_statement()
        if self.editorial_url:
            self.scrape_problem_solution()
        data = {'problem': self.problem_data, 'solution': self.solution_data}
        title = data.get("problem", {}).get("title", "problem").strip()
        save_data(title, data, self.console)

    def scrape_contest_problems(self) -> None:
        """
        Scrape all problems from a Codeforces contest page.
        """
        html_content = fetch_page(self.contest_url)
        soup = BeautifulSoup(html_content, 'html.parser')
        # Find problem links in the contest page (links matching /contest/{id}/problem/{letter})
        problem_links = soup.find_all('a', href=re.compile(r'/contest/\d+/problem/'))
        unique_links = set()
        for link in problem_links:
            href = link.get('href')
            if href:
                full_url = "https://codeforces.com" + href
                unique_links.add(full_url)
        if not unique_links:
            self.console.print("[yellow]No problems found for the provided contest URL.[/yellow]")
        for url in unique_links:
            try:
                self.problem_url = url
                self.scrape_problem()
            except Exception as e:
                logging.error("Error scraping problem %s: %s", url, e)