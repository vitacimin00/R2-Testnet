from web3 import Web3
from eth_abi import encode
from curl_cffi import requests
from decimal import Decimal
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from eth_account import Account
from rich import box
import json
import time
import os
import concurrent.futures

console = Console()
web3 = Web3(Web3.HTTPProvider("https://eth-sepolia.public.blastapi.io"))
chainId = web3.eth.chain_id

console.print(Panel.fit(
    "[bold cyan]🚀 R2 Testnet Auto - Multi Account\n[green]By ADFMIND TEAM[/green]\n[link=https://t.me/AirdropFamilyIDN]Join Telegram[/link]",
    title="🔥 Welcome",
    subtitle="Testnet Tools"))

if web3.is_connected():
    console.print("✅ [green]Web3 Connected[/green]\n")
else:
    console.print("❌ [red]Error Connecting. Please Try Again...[/red]")
    exit()

PRIVATE_KEYS_FILE = "pvkey.txt"  
MAX_RETRIES = 3
DELAY_BETWEEN_ACCOUNTS = 30  
TRANSACTION_AMOUNT = 1 * 10**6  
DEFAULT_PROCESSES_COUNT = 1  

if not os.path.exists(PRIVATE_KEYS_FILE):
    console.print(f"[bold red]❌ Private keys file '{PRIVATE_KEYS_FILE}' not found![/bold red]")
    console.print(f"[yellow]Please create a file named '{PRIVATE_KEYS_FILE}' with your private keys (one per line)[/yellow]")
    with open(PRIVATE_KEYS_FILE, "w") as f:
        f.write("# Add your private keys here, one per line\n")
    exit()

def check_identity(wallet_address, account_name):
    project_id = "f84f8b1354cd3805ef4253caaadbe45f"
    url = f"https://rpc.walletconnect.org/v1/identity/{wallet_address}?projectId={project_id}"
    
    for retry in range(MAX_RETRIES):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                resolved_at = data.get("resolvedAt")
                console.print(Panel.fit(
                    f"[bold green]✅ Identity Verified[/bold green]\n⏱ Resolved At: {resolved_at}",
                    title=f"🪪 WalletConnect - {account_name}"))
                return True
            else:
                console.print(f"[bold yellow]⚠️ Identity request failed for {account_name}: {response.status_code}. Retry {retry+1}/{MAX_RETRIES}[/bold yellow]")
                time.sleep(2)
        except Exception as e:
            console.print(f"[bold yellow]⚠️ Error checking identity for {account_name}: {str(e)}. Retry {retry+1}/{MAX_RETRIES}[/bold yellow]")
            time.sleep(2)
    
    console.print(f"[bold red]❌ Identity verification failed for {account_name} after {MAX_RETRIES} attempts[/bold red]")
    return False

def get_wallet_address_from_pk(private_key):
    account = Account.from_key(private_key)
    return account.address
    
def get_dashboard():
    url = "https://testnet.r2.money/v1/public/dashboard"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("data", {})
        price = data.get("price", {})
        console.print(Panel.fit(
            f"[bold cyan]💰 R2 Faucet Info[/bold cyan]\n"
            f"• R2/USD: ${price.get('r2usd')}\n"
            f"• R2/ETH: {price.get('r2eth')} ETH\n"
            f"• Users: {data.get('users')}\n"
            f"• Total Distributed: {data.get('distributed')}",
            title="📊 Dashboard"))
    else:
        console.print(f"[bold red]❌ Failed to get dashboard info: {response.status_code}[/bold red]")

def checksumAddr(addr): return web3.to_checksum_address(addr)
def getNonce(sender): return int(web3.eth.get_transaction_count(sender))
def getgasPrice(): return int(web3.eth.gas_price * Decimal(1.1))

tokenabi = json.loads('[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"_decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

def show_status(title, sender, target, status, account_name, tx=None):
    table = Table(title=f"{title} - {account_name}", box=box.ROUNDED)
    table.add_column("From", justify="center")
    table.add_column("To", justify="center")
    table.add_column("Status", justify="center")
    if tx:
        table.add_column("TX-ID", justify="center")

    row = [sender[-6:], target[-6:], status]
    if tx:
        row.append(tx)
    table.add_row(*row)
    console.print(table)

def approveTokens(tokenaddr, targetaddr, sender, senderkey, account_name):
    for retry in range(MAX_RETRIES):
        try:
            token_contract = web3.eth.contract(address=tokenaddr, abi=tokenabi)
            approve_tx = token_contract.functions.approve(targetaddr, 2**256 - 1).build_transaction({
                'chainId': chainId,
                'from': sender,
                'gasPrice': getgasPrice(),
                'gas': token_contract.functions.approve(targetaddr, 2**256 - 1).estimate_gas({
                    'from': sender,
                    'gasPrice': getgasPrice(),
                    'nonce': getNonce(sender)
                }),
                'nonce': getNonce(sender)
            })

            tx_hash = web3.eth.send_raw_transaction(web3.eth.account.sign_transaction(approve_tx, senderkey).rawTransaction)
            console.print(f"🔄 [yellow]Approving from {sender[-6:]} to {targetaddr[-6:]} ({account_name})...[/yellow]")
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt.status == 1:
                show_status("✅ Approve Success", sender, targetaddr, "[green]Success[/green]", account_name, web3.to_hex(tx_hash))
                return True
            else:
                console.print(f"[yellow]Transaction reverted for {account_name}. Retry {retry+1}/{MAX_RETRIES}[/yellow]")
        except Exception as e:
            console.print(f"[yellow]Approve attempt {retry+1}/{MAX_RETRIES} failed for {account_name}: {str(e)}[/yellow]")
            time.sleep(2)
    
    show_status("❌ Approve Error", sender, targetaddr, f"[red]Failed after {MAX_RETRIES} attempts[/red]", account_name)
    return False

def apprvCheck(tokenaddr, sender, targetaddr):
    token_contract = web3.eth.contract(address=tokenaddr, abi=tokenabi)
    return int(token_contract.functions.allowance(sender, targetaddr).call())

def tx_process(title, sender, target, tx_hash, totalamount, account_name):
    console.print(f"⏳ [cyan]{title} {totalamount} RUSD for {account_name}...[/cyan]")
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if receipt.status == 1:
        show_status(f"✅ {title} Success", sender, target, "[green]Success[/green]", account_name, web3.to_hex(tx_hash))
        return True
    else:
        show_status(f"❌ {title} Failed", sender, target, "[red]Transaction Reverted[/red]", account_name, web3.to_hex(tx_hash))
        return False

def buyRUSD(addrtarget, sender, senderkey, amount, account_name):
    for retry in range(MAX_RETRIES):
        try:
            totalamount = int(amount) / 10**6
            funcbuy = bytes.fromhex('095e7a95')
            enc = encode(['address', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256'], [sender, amount, 0, 0, 0, 0, 0])
            data = web3.to_hex(funcbuy + enc)
            tx = {
                'chainId': chainId,
                'from': sender,
                'to': addrtarget,
                'data': data,
                'gasPrice': getgasPrice(),
                'gas': web3.eth.estimate_gas({'from': sender, 'to': addrtarget, 'data': data}),
                'nonce': getNonce(sender)
            }
            tx_hash = web3.eth.send_raw_transaction(web3.eth.account.sign_transaction(tx, senderkey).rawTransaction)
            success = tx_process("Buy", sender, addrtarget, tx_hash, totalamount, account_name)
            if success:
                return True
            console.print(f"[yellow]Buy attempt {retry+1}/{MAX_RETRIES} failed for {account_name}[/yellow]")
            time.sleep(2)
        except Exception as e:
            console.print(f"[yellow]Buy attempt {retry+1}/{MAX_RETRIES} failed for {account_name}: {str(e)}[/yellow]")
            time.sleep(2)
    
    show_status("❌ Buy Error", sender, addrtarget, f"[red]Failed after {MAX_RETRIES} attempts[/red]", account_name)
    return False

def stakesRUSD(addrtarget, sender, senderkey, amount, account_name):
    for retry in range(MAX_RETRIES):
        try:
            totalamount = int(amount) / 10**6
            data = web3.to_hex(bytes.fromhex('1a5f0f00') + encode(['uint256'] * 10, [amount] + [0]*9))
            tx = {
                'chainId': chainId,
                'from': sender,
                'to': addrtarget,
                'data': data,
                'gasPrice': getgasPrice(),
                'gas': web3.eth.estimate_gas({'from': sender, 'to': addrtarget, 'data': data}),
                'nonce': getNonce(sender)
            }
            tx_hash = web3.eth.send_raw_transaction(web3.eth.account.sign_transaction(tx, senderkey).rawTransaction)
            success = tx_process("Stake", sender, addrtarget, tx_hash, totalamount, account_name)
            if success:
                return True
            console.print(f"[yellow]Stake attempt {retry+1}/{MAX_RETRIES} failed for {account_name}[/yellow]")
            time.sleep(2)
        except Exception as e:
            console.print(f"[yellow]Stake attempt {retry+1}/{MAX_RETRIES} failed for {account_name}: {str(e)}[/yellow]")
            time.sleep(2)
    
    show_status("❌ Stake Error", sender, addrtarget, f"[red]Failed after {MAX_RETRIES} attempts[/red]", account_name)
    return False

def addLiquidity(addrtarget, sender, senderkey, amount, account_name):
    for retry in range(MAX_RETRIES):
        try:
            totalamount = int(amount) / 10**6
            data = web3.to_hex(
                bytes.fromhex('2e1a7d4d') + encode(
                    ['address', 'address', 'uint256', 'uint256', 'uint256', 'address', 'uint256'],
                    [web3.to_checksum_address('0x20c54C5F742F123Abb49a982BFe0af47edb38756'),
                     web3.to_checksum_address('0xBD6b25c4132F09369C354beE0f7be777D7d434fa'),
                     amount, 0, 0, sender, int(time.time()) + 1000]
                )
            )
            tx = {
                'chainId': chainId,
                'from': sender,
                'to': addrtarget,
                'data': data,
                'gasPrice': getgasPrice(),
                'gas': web3.eth.estimate_gas({'from': sender, 'to': addrtarget, 'data': data}),
                'nonce': getNonce(sender)
            }
            tx_hash = web3.eth.send_raw_transaction(web3.eth.account.sign_transaction(tx, senderkey).rawTransaction)
            success = tx_process("Add Liquidity", sender, addrtarget, tx_hash, totalamount, account_name)
            if success:
                return True
            console.print(f"[yellow]Liquidity attempt {retry+1}/{MAX_RETRIES} failed for {account_name}[/yellow]")
            time.sleep(2)
        except Exception as e:
            console.print(f"[yellow]Liquidity attempt {retry+1}/{MAX_RETRIES} failed for {account_name}: {str(e)}[/yellow]")
            time.sleep(2)
    
    show_status("❌ Liquidity Error", sender, addrtarget, f"[red]Failed after {MAX_RETRIES} attempts[/red]", account_name)
    return False

def load_private_keys():
    private_keys = []
    
    try:
        with open(PRIVATE_KEYS_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    private_keys.append(line)
    except Exception as e:
        console.print(f"[bold red]❌ Error reading private keys file: {str(e)}[/bold red]")
        exit()
    
    if not private_keys:
        console.print(f"[bold yellow]⚠️ No private keys found in '{PRIVATE_KEYS_FILE}'[/bold yellow]")
        console.print(f"[yellow]Please add your private keys to '{PRIVATE_KEYS_FILE}', one per line[/yellow]")
        exit()
    
    return private_keys

def run_account_tasks(private_key, amount, account_index, processes_count):
    account_name = f"Account-{account_index}"
    try:
        account = web3.eth.account.from_key(private_key)
        wallet_address = account.address
        
        console.print(Panel.fit(
            f"[bold green]Processing Account {account_index}[/bold green]\n"
            f"Address: {wallet_address}",
            title="👤 Account Info"))

        if not check_identity(wallet_address, account_name):
            return False

        USDC = web3.to_checksum_address('0xef84994eF411c4981328fFcE5Fda41cD3803faE4')
        rUSD = web3.to_checksum_address('0x20c54C5F742F123Abb49a982BFe0af47edb38756')
        sRUSD = web3.to_checksum_address('0xBD6b25c4132F09369C354beE0f7be777D7d434fa')
        liquidity = web3.to_checksum_address('0xF64a77f6e57d9fEeFd2E8fEDbd0032798dAC21Fa')

        completed_processes = 0

        while completed_processes < processes_count:
            process_num = completed_processes + 1
            console.print(Panel.fit(
                f"[bold cyan]Starting Process {process_num}/{processes_count} for {account_name}[/bold cyan]",
                title="🔄 Process"))

            if apprvCheck(USDC, wallet_address, rUSD) < amount:
                if not approveTokens(USDC, rUSD, wallet_address, private_key, account_name):
                    return False
            if not buyRUSD(rUSD, wallet_address, private_key, amount, account_name):
                return False
            time.sleep(5)
  
            if apprvCheck(rUSD, wallet_address, sRUSD) < amount:
                if not approveTokens(rUSD, sRUSD, wallet_address, private_key, account_name):
                    return False
            if not stakesRUSD(sRUSD, wallet_address, private_key, amount, account_name):
                return False
            time.sleep(5)

            if apprvCheck(rUSD, wallet_address, liquidity) < amount:
                if not approveTokens(rUSD, liquidity, wallet_address, private_key, account_name):
                    return False
            if apprvCheck(sRUSD, wallet_address, liquidity) < amount:
                if not approveTokens(sRUSD, liquidity, wallet_address, private_key, account_name):
                    return False
            if not addLiquidity(liquidity, wallet_address, private_key, amount, account_name):
                return False
            
            completed_processes += 1
            console.print(f"[bold green]✅ Process {process_num}/{processes_count} completed for {account_name}[/bold green]")
        
        console.print(f"[bold green]✅ Completed all {completed_processes} processes for {account_name}[/bold green]")
        return True
    
    except Exception as e:
        console.print(f"[bold red]❌ Error processing {account_name}: {str(e)}[/bold red]")
        return False

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

def main_loop():
    console.print(Panel.fit(
        f"[bold cyan]R2 Testnet Automated Multi-Account Process Bot[/bold cyan]\n"
        f"Using private keys from file: '{PRIVATE_KEYS_FILE}'",
        title="ℹ️ Information"))

    try:
        amount = int(input("Enter amount to use (default: 1000000, which is 1 RUSD): ") or TRANSACTION_AMOUNT)
    except ValueError:
        amount = TRANSACTION_AMOUNT
        console.print(f"[yellow]Invalid input. Using default amount: {amount/10**6} RUSD[/yellow]")
    
    try:
        processes_per_account = int(input(f"Enter number of processes to run for each account (default: {DEFAULT_PROCESSES_COUNT}): ") or DEFAULT_PROCESSES_COUNT)
        if processes_per_account < 1:
            processes_per_account = DEFAULT_PROCESSES_COUNT
            console.print(f"[yellow]Invalid input. Using default: {DEFAULT_PROCESSES_COUNT} process(es).[/yellow]")
    except ValueError:
        processes_per_account = DEFAULT_PROCESSES_COUNT
        console.print(f"[yellow]Invalid input. Using default: {DEFAULT_PROCESSES_COUNT} process(es).[/yellow]")
    
    try:
        delay_between_accounts = int(input(f"Enter delay between accounts in seconds (default: {DELAY_BETWEEN_ACCOUNTS}): ") or DELAY_BETWEEN_ACCOUNTS)
        if delay_between_accounts < 0:
            delay_between_accounts = DELAY_BETWEEN_ACCOUNTS
            console.print(f"[yellow]Invalid input. Using default: {DELAY_BETWEEN_ACCOUNTS} seconds.[/yellow]")
    except ValueError:
        delay_between_accounts = DELAY_BETWEEN_ACCOUNTS
        console.print(f"[yellow]Invalid input. Using default: {DELAY_BETWEEN_ACCOUNTS} seconds.[/yellow]")

    private_keys = load_private_keys()
    console.print(f"[green]Found {len(private_keys)} accounts to process[/green]")
    console.print("[cyan]Wallet addresses:[/cyan]")
    wallet_table = Table(title="Account List", box=box.ROUNDED)
    wallet_table.add_column("Index", justify="center")
    wallet_table.add_column("Address", justify="left")
    
    for idx, private_key in enumerate(private_keys):
        try:
            address = get_wallet_address_from_pk(private_key)
            wallet_table.add_row(f"{idx+1}", address)
        except Exception as e:
            wallet_table.add_row(f"{idx+1}", f"[red]Invalid key: {str(e)}[/red]")
    
    console.print(wallet_table)
    confirmation = input("Start processing all accounts automatically? (y/n): ").strip().lower()
    if confirmation != 'y':
        console.print("[yellow]Process aborted.[/yellow]")
        return
    get_dashboard()
    successful_accounts = 0
    failed_accounts = 0
    
    for idx, private_key in enumerate(private_keys):
        account_idx = idx + 1
        start_time = time.time()
        
        console.print(Panel.fit(
            f"[bold cyan]Processing Account {account_idx}/{len(private_keys)}[/bold cyan]",
            title="🔄 Progress"))        
        success = run_account_tasks(private_key, amount, account_idx, processes_per_account)
        
        if success:
            successful_accounts += 1
            console.print(f"[bold green]✅ Account-{account_idx} completed successfully![/bold green]")
        else:
            failed_accounts += 1
            console.print(f"[bold red]❌ Account-{account_idx} encountered errors![/bold red]")
        
        if idx < len(private_keys) - 1:
            elapsed_time = time.time() - start_time
            remaining_delay = max(0, delay_between_accounts - int(elapsed_time))
            
            if remaining_delay > 0:
                console.print(f"[cyan]Waiting {remaining_delay} seconds before processing next account...[/cyan]")
                time.sleep(remaining_delay)
    
    console.print(Panel.fit(
        f"[bold green]✅ Process completed![/bold green]\n"
        f"Total accounts: {len(private_keys)}\n"
        f"Successful: {successful_accounts}\n"
        f"Failed: {failed_accounts}",
        title="📊 Summary"))

if __name__ == "__main__":
    main_loop()
