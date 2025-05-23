# Codeforces-Scraper
A ***Selenium-Python-based scraper*** designed to extract comprehensive problem and contest data from Codeforces. This tool retrieves essential information such as **problem descriptions, input specifications, output specifications, tags, examples, time limits, memory limits**, and more. Additionally, it captures **solution descriptions and code implementations** from the **official contest editorials** when available.

## Features

- **Scrape Single Problems:** Retrieve detailed problem data.
- **Scrape Contests:** Automatically extract and scrape all problems from a contest.
- **Solution Retrieval:** Fetch solution descriptions and code implementations from the contest editorials.

## Project Structure

```plaintext
codeforces-scraper/
├── main.py          # CLI entry point with Typer and Rich integration.
├── scraper.py       # Contains scraping logic for problems and contests.
├── utils.py         # Utility functions (e.g., text cleaning).
├── requirements.txt # Project dependencies.
├── .gitignore       # Files and directories to ignore.
└── README.md        # Project documentation.

```

## Installation
1. **Clone the repository:**
```bash
git clone https://github.com/Ret2Hell/Codeforces-Scraper.git
cd codeforces-scraper
```
1. **Install the required packages:**
```bash
pip install -r requirements.txt
```

## Requirements
- Python 3.8 or higher
- Google Chrome >= 135 (Make sure your Google Chrome browser is updated to version 135 or above for compatibility with undetected-chromedriver).

## Dependencies
This project depends on the following Python libraries:
- `selenium`: For web scraping and browser automation.
- `undetected-chromedriver`: For bypassing bot detection on Codeforces.
- `beautifulsoup4`: For parsing HTML content.
- `typer`: For building the command-line interface.
- `rich`: For creating beautiful terminal output.

## Usage
There are two ways to use this tool:
1. **Using Subcommands**
   - To scrape a single problem:
     ```bash
     python main.py scrape-problem
     ```
   - To scrape all problems from a contest:
     ```bash
     python main.py scrape-contest
     ```
2. **Interactive Menu**
    ```bash
    python main.py
    ```

## Example Output

The scraped data is saved as a JSON file in the `Examples` directory. The structure of the output file is as follows:

```json
{
    "problem": {
        "title": "A. Kamilka and the Sheep",
        "description": "Kamilka has a flock of nn sheep, the ii-th of which has a beauty level of aiai. All aiai are distinct. Morning has come, which means they need to be fed. Kamilka can choose a non-negative integer dd and give each sheep dd bunches of grass. After that, the beauty level of each sheep increases by dd.In the evening, Kamilka must choose exactly two sheep and take them to the mountains. If the beauty levels of these two sheep are xx and yy (after they have been fed), then Kamilka's pleasure from the walk is equal to gcd(x,y)gcd(x,y), where gcd(x,y)gcd(x,y) denotes the greatest common divisor (GCD) of integers xx and yy. The task is to find the maximum possible pleasure that Kamilka can get from the walk.",
        "input": "InputEach test consists of several test cases. The first line contains one integer tt (1≤t≤5001≤t≤500), the number of test cases. The description of the test cases follows. The first line of each test case contains one integer nn (2≤n≤1002≤n≤100), the number of sheep Kamilka has. The second line of each test case contains nn distinct integers a1,a2,…,an (1≤ai≤109)a1,a2,…,an (1≤ai≤109) — the beauty levels of the sheep.It is guaranteed that all aiai are distinct.",
        "output": "OutputFor each test case, output a single integer: the maximum possible pleasure that Kamilka can get from the walk.",
        "time_limit": "1 second",
        "memory_limit": "256 megabytes",
        "tags": [
            "greedy",
            "math",
            "number theory",
            "sortings",
            "*800"
        ],
        "examples": [
            {
                "input": "421 355 4 3 2 135 6 731 11 10",
                "output": "2 4 2 10"
            }
        ]
    },
    "solution": {
        "description": "First of all, it can be observed that for any two sheep with beauty levels x<yx<y, the maximum possible pleasure cannot exceed y−xy−x, since gcd(x,y)=gcd(x,y−x)gcd(x,y)=gcd(x,y−x).Secondly, we can choose x=min(a)x=min(a), y=max(a)y=max(a), and d=−xmod(y−x)d=−xmod(y−x), achieving a pleasure of max(a)−min(a)max(a)−min(a).Thus, the answer is max(a)−min(a)max(a)−min(a).",
        "code": "t = int(input())\n \nfor test in range(t):\n    n = int(input())\n    a = [int(i) for i in input().split()]\n    print(max(a) - min(a))\n\n"
    }
}
```

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [Codeforces](https://codeforces.com/) for providing a rich set of competitive programming problems.