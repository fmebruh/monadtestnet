# Monad Testnet Automation Scripts

This repository contains a collection of Python scripts designed to automate various tasks on the Monad Testnet. The scripts are integrated with a central `main.py` for easy execution of tasks like swapping, staking, and contract deployment.

## Getting Started

### Prerequisites
* Python 3.7 or higher
* `pip` (Python package installer)

### Installation
1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/fmebruh/monadtestnet.git](https://github.com/fmebruh/monadtestnet.git)
    cd monadtestnet
    ```
2.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
3.  **Add Private Keys:**
    Create a file named `pvkey.txt` in the root directory and add your private keys, one per line.
    ```sh
    nano pvkey.txt
    ```
4.  **Add Recipient Addresses (Optional):**
    For sending transactions, create an `address.txt` file and add recipient addresses, one per line.
    ```sh
    nano address.txt
    ```
5.  **Run the main script:**
    ```sh
    python main.py
    ```

---

## Scripts Overview

The main menu allows you to choose from the following scripts:

### 1. Rubic Swap
* **Description**: Swaps MON to USDT using the Rubic router.
* **Features**:
    * Takes a user-defined number of cycles to run.
    * Wraps MON to WMON before swapping.
    * Includes random delays between 60 and 180 seconds.

### 2. Magma Staking
* **Description**: Stakes MON and unstakes gMON on the Magma contract.
* **Features**:
    * Stakes a random amount between 0.01 and 0.05 MON.
    * Waits for a random delay of 1-3 minutes between staking and unstaking.

### 3. Izumi Swap
* **Description**: Wraps MON to WMON and unwraps it back using the Izumi contract.
* **Features**:
    * Uses a random amount between 0.01 and 0.05 MON for each cycle.
    * Asynchronous operations for wrapping and unwrapping.

### 4. aPriori Staking
* **Description**: A complete stake, unstake, and claim cycle on the aPriori Staking contract.
* **Features**:
    * Stakes a random amount of MON (0.01-0.05).
    * Requests to unstake the corresponding aprMON.
    * Waits 11 minutes before checking and claiming the unstaked MON.

### 5. Kintsu Staking
* **Description**: Stakes MON and unstakes sMON on the Kitsu Staking contract.
* **Features**:
    * Stakes a random amount of MON (0.01-0.05).
    * Unstakes the same amount after a random 1-3 minute delay.

### 6. Bean Swap
* **Description**: Swaps MON with various tokens (USDC, USDT, BEAN, JAI) on Bean Swap.
* **Features**:
    * Randomly chooses between swapping MON to a token or a token back to MON.
    * Uses random amounts between 0.001 and 0.01 MON for swaps.

### 7. Monorail Swap
* **Description**: Sends a predefined transaction to the Monorail contract.
* **Features**:
    * Sends a fixed 0.1 MON transaction with custom data.
    * Estimates gas dynamically and includes a fallback.

### 8. Bebop Swap
* **Description**: Wraps MON to WMON and unwraps it back via the Bebop contract.
* **Features**:
    * User provides a MON amount between 0.01 and 999 to wrap and unwrap.
    * Synchronous operations.

### 9. Ambient Finance Swap
* **Description**: Swaps tokens on the Ambient DEX.
* **Features**:
    * Performs random swaps between a list of supported tokens including USDC, USDT, and WETH.
    * Includes a retry mechanism for failed transactions.

### 10. Uniswap Swap
* **Description**: Swaps between MON and a list of tokens on Uniswap V2.
* **Features**:
    * Swaps MON to all supported tokens and then swaps them all back to MON in each cycle.
    * Uses a random MON amount between 0.0001 and 0.01 for swaps.

### 11. Deploy Contract
* **Description**: Deploys a simple `Counter` smart contract to the Monad Testnet.
* **Features**:
    * Prompts the user for a token name and symbol for the contract.
    * Displays the transaction hash and the new contract address upon successful deployment.

### 12. Send Random TX or File
* **Description**: Sends MON transactions to either random addresses or a list of addresses from a file.
* **Features**:
    * User can choose to send to randomly generated addresses or addresses from `address.txt`.
    * User defines the number of transactions and the amount of MON to send.

### 13. Bima Deposit bmBTC
* **Description**: Gets bmBTC from the faucet and deposits it as collateral on Bima Finance.
* **Features**:
    * Logs into Bima, requests tokens from the faucet, and supplies them as collateral.
    * Lends a random percentage (20-30%) of the bmBTC balance.


JOIN FOR MORE - https://t.me/ChainScripters

### 14. Mint NFT Lil Chogstars
* **Description**: Mints Lil Chogstars NFTs.
* **Features**:
    * Mints a random number of NFTs for each account, between 1 and 3.
    * Checks the existing balance to avoid minting more than the target amount.
