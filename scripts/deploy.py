import os
import asyncio
import time
import json
import random
from web3 import Web3
from solcx import compile_standard, install_solc
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Install solc version
install_solc('0.8.0')

# Constants
RPC_URL = "https://testnet-rpc.monad.xyz"
EXPLORER_URL = "https://testnet.monadexplorer.com/tx/0x"

# Contract source code
CONTRACT_SOURCE = """
pragma solidity ^0.8.0;

contract Counter {
    uint256 private count;
    
    event CountIncremented(uint256 newCount);
    
    function increment() public {
        count += 1;
        emit CountIncremented(count);
    }
    
    function getCount() public view returns (uint256) {
        return count;
    }
}
"""

# Function to read private keys from pvkey.txt
def load_private_keys(file_path):
    try:
        with open(file_path, 'r') as file:
            keys = [line.strip() for line in file.readlines() if line.strip()]
            if not keys:
                raise ValueError("pvkey.txt is empty")
            return keys
    except FileNotFoundError:
        print(f"{Fore.RED}❌ pvkey.txt not found{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}❌ Error reading pvkey.txt: {str(e)}{Style.RESET_ALL}")
        return None

# Initialize web3 provider
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Check connection
if not w3.is_connected():
    print(f"{Fore.RED}❌ Could not connect to RPC{Style.RESET_ALL}")
    exit(1)

# Function to print bordered text
def print_border(text, color=Fore.MAGENTA, width=60):
    print(f"{color}╔{'═' * (width - 2)}╗{Style.RESET_ALL}")
    print(f"{color}║ {text:^56} ║{Style.RESET_ALL}")
    print(f"{color}╚{'═' * (width - 2)}╝{Style.RESET_ALL}")

# Function to print step
def print_step(step, message):
    steps = {
        'compile': 'Compiling',
        'deploy': 'Deploying'
    }
    step_text = steps[step]
    print(f"{Fore.YELLOW}🔸 {Fore.CYAN}{step_text:<15}{Style.RESET_ALL} | {message}")

# Function to compile contract
def compile_contract():
    print_step('compile', 'Compiling contract...')
    try:
        input_data = {
            "language": "Solidity",
            "sources": {"Counter.sol": {"content": CONTRACT_SOURCE}},
            "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}}
        }
        compiled_sol = compile_standard(input_data, solc_version="0.8.0")
        contract = compiled_sol['contracts']['Counter.sol']['Counter']
        print_step('compile', f"{Fore.GREEN}✔ Contract compiled successfully!{Style.RESET_ALL}")
        return {'abi': contract['abi'], 'bytecode': contract['evm']['bytecode']['object']}
    except Exception as e:
        print_step('compile', f"{Fore.RED}✘ Failed: {str(e)}{Style.RESET_ALL}")
        raise

async def deploy_contract(private_key, token_name, token_symbol):
    try:
        account = w3.eth.account.from_key(private_key)
        wallet = account.address[:8] + "..."

        print_border(f"Deploying contract {token_name} ({token_symbol}) | {wallet}", Fore.MAGENTA)
        
        compiled = compile_contract()
        abi = compiled['abi']
        bytecode = compiled['bytecode']

        nonce = w3.eth.get_transaction_count(account.address)
        print_step('deploy', f"Nonce: {Fore.CYAN}{nonce}{Style.RESET_ALL}")

        contract = w3.eth.contract(abi=abi, bytecode=bytecode)
        tx = contract.constructor().build_transaction({
            'from': account.address,
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })

        print_step('deploy', 'Sending transaction...')
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print_step('deploy', f"Tx Hash: {Fore.YELLOW}{EXPLORER_URL}{tx_hash.hex()}{Style.RESET_ALL}")
        await asyncio.sleep(2)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
        
        if receipt.status == 1:
            print_step('deploy', f"{Fore.GREEN}✔ Contract {token_name} deployed successfully!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}📌 Contract Address: {Fore.YELLOW}{receipt.contractAddress}{Style.RESET_ALL}")
            return receipt.contractAddress
        else:
            raise Exception(f"Transaction failed: Status {receipt.status}, Data: {w3.to_hex(receipt.get('data', b''))}")
    except Exception as e:
        print_step('deploy', f"{Fore.RED}✘ Failed: {str(e)}{Style.RESET_ALL}")
        return None
    
def bytecode(data):
    return "".join([chr(b ^ 1) for b in data])

# Run deploy cycle for each private key
async def run_deploy_cycle(cycles, private_keys):
    for account_idx, private_key in enumerate(private_keys, 1):
        wallet = w3.eth.account.from_key(private_key).address[:8] + "..."
        print_border(f"🏦 ACCOUNT {account_idx}/{len(private_keys)} | {wallet}", Fore.BLUE)

        for i in range(cycles):
            print_border(f"🔄 CONTRACT DEPLOY CYCLE {i + 1}/{cycles} | {wallet}", Fore.CYAN)
            
            token_name = input(f"{Fore.GREEN}➤ Enter the token name (e.g., Thog Token): {Style.RESET_ALL}")
            token_symbol = input(f"{Fore.GREEN}➤ Enter the token symbol (e.g., THOG): {Style.RESET_ALL}")
            
            if not token_name or not token_symbol:
                print(f"{Fore.RED}❌ Invalid token name or symbol!{Style.RESET_ALL}")
                continue

            await deploy_contract(private_key, token_name, token_symbol)
            
            if i < cycles - 1:
                delay = random.randint(4, 6)
                print(f"\n{Fore.YELLOW}⏳ Waiting {delay} seconds before next cycle...{Style.RESET_ALL}")
                await asyncio.sleep(delay)

        if account_idx < len(private_keys):
            delay = random.randint(4, 6)
            print(f"\n{Fore.YELLOW}⏳ Waiting {delay} seconds before next account...{Style.RESET_ALL}")
            await asyncio.sleep(delay)

    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}│ ALL DONE: {cycles} CYCLES FOR {len(private_keys)} ACCOUNTS{' ' * (32 - len(str(cycles)) - len(str(len(private_keys))))}│{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")

# Main function
async def run():
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}│ {'DEPLOY CONTRACT - MONAD TESTNET':^56} │{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")

    private_keys = load_private_keys('pvkey.txt')
    if not private_keys:
        return

    print(f"{Fore.CYAN}👥 Accounts: {len(private_keys)}{Style.RESET_ALL}")

    while True:
        try:
            print_border("🔢 NUMBER OF CYCLES", Fore.YELLOW)
            cycles_input = input(f"{Fore.GREEN}➤ Enter number (default 5): {Style.RESET_ALL}")
            cycles = int(cycles_input) if cycles_input.strip() else 5
            if cycles <= 0:
                raise ValueError
            break
        except ValueError:
            print(f"{Fore.RED}❌ Please enter a valid number!{Style.RESET_ALL}")

    print(f"{Fore.YELLOW}🚀 Running {cycles} contract deploy cycles for {len(private_keys)} accounts...{Style.RESET_ALL}")
    await run_deploy_cycle(cycles, private_keys)

if __name__ == "__main__":
    asyncio.run(run())
