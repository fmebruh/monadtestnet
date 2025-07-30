import os
import random
import asyncio
from web3 import Web3
from eth_account import Account
from scripts.deploy import bytecode
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Constants
NETWORK_URL = "https://testnet-rpc.monad.xyz/"
CHAIN_ID = 10143
EXPLORER_URL = "https://testnet.monadexplorer.com/tx/0x"

# Initialize web3 provider
w3 = Web3(Web3.HTTPProvider(NETWORK_URL))

# Check connection
if not w3.is_connected():
    raise Exception("Cannot connect to network")

# Function to read private keys from pvkey.txt
def load_private_keys(file_path):
    try:
        with open(file_path, 'r') as file:
            keys = [line.strip() for line in file.readlines() if len(line.strip()) in [64, 66]]
            if not keys:
                raise ValueError("No valid private keys found in file")
            return keys
    except FileNotFoundError:
        print(f"{Fore.RED}❌ pvkey.txt not found{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}❌ Error reading pvkey.txt: {str(e)}{Style.RESET_ALL}")
        return None

# Function to read addresses from address.txt
def load_addresses(file_path):
    try:
        with open(file_path, 'r') as file:
            addresses = [line.strip() for line in file if line.strip()]
            if not addresses:
                raise ValueError("No valid addresses found in file")
            return addresses
    except FileNotFoundError:
        print(f"{Fore.RED}❌ address.txt not found{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}❌ Error reading address.txt: {str(e)}{Style.RESET_ALL}")
        return None

# Function to display pretty border
def print_border(text, color=Fore.MAGENTA, width=60):
    print(f"{color}╔{'═' * (width - 2)}╗{Style.RESET_ALL}")
    print(f"{color}║ {text:^56} ║{Style.RESET_ALL}")
    print(f"{color}╚{'═' * (width - 2)}╝{Style.RESET_ALL}")

# Function to display step
def print_step(step, message):
    step_text = "Send Transaction" if step == 'send' else step
    print(f"{Fore.YELLOW}🔸 {Fore.CYAN}{step_text:<15}{Style.RESET_ALL} | {message}")

# Random address with checksum
def get_random_address():
    random_address = '0x' + ''.join(random.choices('0123456789abcdef', k=40))
    return w3.to_checksum_address(random_address)

# Function to send transaction
async def send_transaction(private_key, to_address, amount):
    account = Account.from_key(private_key)
    sender_address = account.address

    try:
        nonce = w3.eth.get_transaction_count(sender_address)
        latest_block = w3.eth.get_block('latest')
        base_fee_per_gas = latest_block['baseFeePerGas']
        max_priority_fee_per_gas = w3.to_wei(2, 'gwei')
        max_fee_per_gas = base_fee_per_gas + max_priority_fee_per_gas

        tx = {
            'nonce': nonce,
            'to': w3.to_checksum_address(to_address),
            'value': w3.to_wei(amount, 'ether'),
            'gas': 21000,
            'maxFeePerGas': max_fee_per_gas,
            'maxPriorityFeePerGas': max_priority_fee_per_gas,
            'chainId': CHAIN_ID,
        }

        print_step('send', 'Sending transaction...')
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_link = f"{EXPLORER_URL}{tx_hash.hex()}"
        
        await asyncio.sleep(2)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
        
        if receipt.status == 1:
            print_step('send', f"{Fore.GREEN}✔ Transaction successful! Tx: {tx_link}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Sender: {sender_address}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Receiver: {to_address}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Amount: {amount:.6f} MONAD{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Gas: {receipt['gasUsed']}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Block: {receipt['blockNumber']}{Style.RESET_ALL}")
            balance = w3.from_wei(w3.eth.get_balance(sender_address), 'ether')
            print(f"{Fore.YELLOW}Balance: {balance:.6f} MONAD{Style.RESET_ALL}")
            return True
        else:
            print_step('send', f"{Fore.RED}✘ Transaction failed! Tx: {tx_link}{Style.RESET_ALL}")
            return False
    except Exception as e:
        print_step('send', f"{Fore.RED}✘ Failed: {str(e)}{Style.RESET_ALL}")
        return False


# Send transactions to random addresses
async def send_to_random_addresses(amount, tx_count, private_keys):
    print_border(f'Starting {tx_count} random transactions', Fore.CYAN)
    
    count = 0
    for _ in range(tx_count):
        for private_key in private_keys:
            to_address = get_random_address()
            if await send_transaction(private_key, to_address, amount):
                count += 1
            await asyncio.sleep(random.uniform(1, 3))  # Random delay 1-3 seconds
    
    print(f"{Fore.YELLOW}Total successful transactions: {count}{Style.RESET_ALL}")
    return count

# Send transactions to addresses from file
async def send_to_file_addresses(amount, addresses, private_keys):
    print_border(f'Starting transactions to {len(addresses)} addresses from file', Fore.CYAN)
    
    count = 0
    for private_key in private_keys:
        for to_address in addresses:
            if await send_transaction(private_key, to_address, amount):
                count += 1
            await asyncio.sleep(random.uniform(1, 3))  # Random delay 1-3 seconds
    
    print(f"{Fore.YELLOW}Total successful transactions: {count}{Style.RESET_ALL}")
    return count

# Main function
async def run():
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}│ {'SEND TX - MONAD TESTNET':^56} │{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")

    private_keys = load_private_keys('pvkey.txt')
    if not private_keys:
        return

    print(f"{Fore.CYAN}👥 Accounts: {len(private_keys)}{Style.RESET_ALL}")

    while True:
        try:
            print_border("🔢 NUMBER OF TRANSACTIONS", Fore.YELLOW)
            tx_count_input = input(f"{Fore.GREEN}➤ Enter number (default 5): {Style.RESET_ALL}")
            tx_count = int(tx_count_input) if tx_count_input.strip() else 5
            if tx_count <= 0:
                raise ValueError
            break
        except ValueError:
            print(f"{Fore.RED}❌ Please enter a valid number!{Style.RESET_ALL}")

    while True:
        try:
            print_border("💰 AMOUNT OF MONAD", Fore.YELLOW)
            amount_input = input(f"{Fore.GREEN}➤ Enter amount (default 0.000001, max 999): {Style.RESET_ALL}")
            amount = float(amount_input) if amount_input.strip() else 0.000001
            if 0 < amount <= 999:
                break
            raise ValueError
        except ValueError:
            print(f"{Fore.RED}❌ Amount must be greater than 0 and not exceed 999!{Style.RESET_ALL}")

    while True:
        print_border("🔧 TRANSACTION TYPE", Fore.YELLOW)
        print(f"{Fore.CYAN}1. Send to random address{Style.RESET_ALL}")
        print(f"{Fore.CYAN}2. Send to addresses from file (address.txt){Style.RESET_ALL}")
        choice = input(f"{Fore.GREEN}➤ Enter choice (1/2): {Style.RESET_ALL}")

        if choice == '1':
            await send_to_random_addresses(amount, tx_count, private_keys)
            break
        elif choice == '2':
            addresses = load_addresses('address.txt')
            if addresses:
                await send_to_file_addresses(amount, addresses, private_keys)
            break
        else:
            print(f"{Fore.RED}❌ Invalid choice!{Style.RESET_ALL}")

    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}│ ALL DONE: {tx_count} TRANSACTIONS FOR {len(private_keys)} ACCOUNTS{' ' * (32 - len(str(tx_count)) - len(str(len(private_keys))))}│{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")

# Run the program if it's the main file
if __name__ == "__main__":
    asyncio.run(run())
