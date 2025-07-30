# Monad Testnet Automation Scripts

This repository contains a collection of Python scripts designed to automate various tasks on the Monad Testnet, including staking, swapping, deploying contracts, and sending transactions. The scripts are integrated with a central `main.py` file for easy navigation and execution, supporting multiple private keys and a user-friendly CLI interface

## Setup Instructions:

- Python 3.7 or higher (recommended 3.9 or 3.10 due to `asyncio` usage).
- `pip` (Python package installer)

## Installation
1. **Clone this repository:**
- Open cmd or Shell, then run the command:
```sh
git clone https://github.com/BUpikgypbijpiv/monad-testnet-bot.git
```
```sh
cd Monad-testnet-bot
```
2. **Install Dependencies:**
- Open cmd or Shell, then run the command:
```sh
pip install -r requirements.txt
```
3. **Create Required Input Files:**
- Create and open `pvkey.txt`: Add your private keys (one per line) in the root directory.
```sh
nano pvkey.txt 
```
- create and open `address.txt`(optional): Add recipient addresses (one per line) for `sendtx.py`.
```sh
nano address.txt 
```
4. **Run:**
- Open cmd or Shell, then run command:
```sh
python main.py
```


## Features Overview

### 2.Kintsu Staking
- **Description**: Automates staking and unstaking MON tokens on the Kitsu Staking contract.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Random staking amounts (0.01-0.05 MON).
  - Random delays (1-3 minutes) between actions.
  - Stake and unstake cycles with detailed transaction logging.
  - Bilingual output (Vietnamese/English).
- **Usage**: Select from `main.py` menu, input number of cycles.

### 3.Bean Swap
- **Description**: Automates swapping between MON and tokens (USDC, USDT, BEAN, JAI) on Bean Swap.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Random swaps (MON → Token or Token → MON).
  - Configurable cycles and random delays (1-3 minutes).
  - Balance checking before and after swaps.
  - Detailed transaction logs with Tx Hash and explorer links.
- **Usage**: Select from `main.py` menu, input cycles.

### 4.Uniswap Swap
- **Description**: Automates swapping between MON and tokens (DAC, USDT, WETH, MUK, USDC, CHOG) on Uniswap V2.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Random swaps (MON → Token or Token → MON).
  - Configurable cycles and random delays (1-3 minutes).
  - Balance checking before and after swaps.
  - Detailed transaction logs with Tx Hash and explorer links.
- **Usage**: Select from `main.py` menu, input cycles.

### 5.Contract Deployment
- **Description**: Deploys a simple Counter contract to Monad Testnet.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - User input for contract name and symbol (e.g., "Thog Token", "THOG").
  - Configurable deployment cycles with random delays (4-6 seconds).
  - Displays contract address and Tx Hash after deployment.
  - Bilingual output (Vietnamese/English).
- **Usage**: Select from `main.py` menu, input cycles, then enter name and symbol for each deployment.

### 6.Send Transactions
- **Description**: Sends MON transactions to random addresses or addresses from a file.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Two modes:
    - Send to random addresses (user-defined transaction count).
    - Send to addresses from `address.txt`.
  - Configurable MON amount (default 0.000001, max 999).
  - Random delays (1-3 seconds) between transactions.
  - Detailed logs including sender, receiver, amount, gas, block, and balance.
- **Usage**: Select from `main.py` menu, input transaction count, amount, and mode.

### 7.Ambient Swap Bot
- **Description**: Automates token swapping on the Ambient DEX.
- **Features**:
  - Random Swap: Performs random swaps between USDC, USDT, and WETH with customizable amounts.
  - Manual Swap: Allows users to select source/destination tokens and input amounts.
  - Balance Checking: Displays MON and token balances (USDC, USDT, WETH).
  - Retry Mechanism: Retries failed transactions up to 3 times with a 5-second delay for RPC errors.
  - Extended Deadline: Swap transactions have a 1-hour deadline to avoid "Swap Deadline" errors.
  - Interactive Menu: Offers a CLI menu to choose between Random Swap, Manual Swap, or Exit.
- **Usage**: Select from `main.py` menu, choose Random/Manual mode, and follow prompts.

### 8.Rubic Swap Script
- **Description**: Automates swapping MON to USDT via the Rubic router.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Configurable swap cycles with random amounts (0.01 MON).
  - Random delays (1-3 minutes) between cycles and accounts.
  - Transaction tracking with Tx Hash and explorer links.
- **Usage**: Select from `main.py` menu, input number of cycles.

### 9.Monorail Transaction Script
- **Description**: Sends predefined transactions to the Monorail contract.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Sends 0.1 MON transactions with custom data.
  - Gas Estimation: Falls back to 500,000 if estimation fails.
  - Explorer Links: Provides transaction links for tracking.
  - Random delays (1-3 minutes) between accounts.
- **Usage**: Select from `main.py` menu, runs automatically for all accounts.

### 10.Apriori Staking
- **Description**: Automates staking, unstaking, and claiming MON on the Apriori Staking contract.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Random staking amounts (0.01-0.05 MON).
  - Configurable cycles with random delays (1-3 minutes) between actions.
  - Stake → Unstake → Claim sequence with API check for claimable status.
  - Detailed transaction logging with Tx Hash and explorer links.
  - Bilingual output (Vietnamese/English).
- **Usage**: Select from `main.py` menu, input number of cycles.

### 11.Bebop Wrap/Unwrap Script
- **Description**: Wraps MON to WMON and unwraps WMON back to MON via the Bebop contract (synchronous version).
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - User-defined MON amounts (0.01-0.05) for wrapping/unwrapping.
  - Configurable cycles with random delays (1-3 minutes).
  - Transaction tracking with Tx Hash and explorer links.
  - Bilingual output (Vietnamese/English).
- **Usage**: Select from `main.py` menu, input number of cycles and MON amount.

### 12.Izumi Wrap/Unwrap Script
- **Description**: Wraps MON to WMON and unwraps WMON back to MON via the Izumi contract (asynchronous version).
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Random wrap/unwrap amounts (0.01-0.05 MON).
  - Configurable cycles with random delays (1-3 minutes).
  - Transaction tracking with Tx Hash and explorer links.
  - Bilingual output (Vietnamese/English).
- **Usage**: Select from `main.py` menu, input number of cycles.

### 13.Magma Staking
- **Description**: Automates staking MON and unstaking gMON on the Magma contract.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Random staking amounts (0.01-0.05 MON).
  - Configurable cycles with random delays (1-3 minutes) between stake/unstake.
  - Transaction tracking with Tx Hash and explorer links.
  - Bilingual output (Vietnamese/English).
- **Usage**: Select from `main.py` menu, input number of cycles.
