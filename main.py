import os
import sys
import importlib
import inquirer
import asyncio
from scripts.apriori import get_quote
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Fixed border width
BORDER_WIDTH = 80

def print_border(text: str, color=Fore.CYAN, width=BORDER_WIDTH):
    text = text.strip()
    if len(text) > width - 4:
        text = text[:width - 7] + "..."
    padded_text = f" {text} ".center(width - 2)
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│{padded_text}│{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

def _banner():
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
    print_border("MONAD TESTNET", Fore.GREEN)
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")

def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_available_scripts():
    return [
        {"name": "1. Rubic Swap", "value": "rubic"},
        {"name": "2. Magma Staking", "value": "magma"},
        {"name": "3. Izumi Swap", "value": "izumi"},
        {"name": "4. aPriori Staking", "value": "apriori"},
        {"name": "5. Kintsu Staking", "value": "kintsu"},
        {"name": "6. Bean Swap", "value": "bean"},
        {"name": "7. Monorail Swap", "value": "mono"},
        {"name": "8. Bebop Swap", "value": "bebop"},
        {"name": "9. Ambient Finance Swap", "value": "ambient"},
        {"name": "10. Uniswap Swap", "value": "uniswap"},
        {"name": "11. Deploy Contract", "value": "deploy"},
        {"name": "12. Send Random TX or File (address.txt)", "value": "sendtx"},
        {"name": "13. Bima Deposit bmBTC", "value": "bima"},
        {"name": "14. Mint NFT Lil Chogstars", "value": "lilchogstars"},
        {"name": "17. Exit", "value": "exit"}
    ]

def run_script(script_module):
    """Run script whether it's async or not."""
    run_func = script_module.run
    if asyncio.iscoroutinefunction(run_func):
        asyncio.run(run_func())
    else:
        run_func()

def main():
    _clear()
    _banner()

    while True:
        _clear()
        _banner()
        get_quote()
        print_border("MAIN MENU", Fore.YELLOW)

        available_scripts = get_available_scripts()
        questions = [
            inquirer.List('script',
                          message=f"{Fore.CYAN}Select script to run{Style.RESET_ALL}",
                          choices=[script["name"] for script in available_scripts],
                          carousel=True)
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            continue

        selected_script_name = answers['script']
        selected_script_value = next(script["value"] for script in available_scripts if script["name"] == selected_script_name)

        if selected_script_value == "exit":
            print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border("EXITING", Fore.GREEN)
            print(f"{Fore.YELLOW}👋 {'Goodbye!':^76}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            sys.exit(0)

        try:
            print(f"{Fore.CYAN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(f"RUNNING: {selected_script_name}", Fore.CYAN)
            script_module = importlib.import_module(f"scripts.{selected_script_value}")
            run_script(script_module)
            print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(f"Completed {selected_script_name}", Fore.GREEN)
            input(f"{Fore.YELLOW}⏎ Press Enter to continue...{Style.RESET_ALL:^76}")
        except ImportError:
            print(f"{Fore.RED}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(f"Script not found: {selected_script_value}", Fore.RED)
            input(f"{Fore.YELLOW}⏎ Press Enter to continue...{Style.RESET_ALL:^76}")
        except Exception as e:
            print(f"{Fore.RED}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(f"Error: {str(e)}", Fore.RED)
            input(f"{Fore.YELLOW}⏎ Press Enter to continue...{Style.RESET_ALL:^76}")

if __name__ == "__main__":
    main()
