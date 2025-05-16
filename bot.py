import time
from datetime import datetime
import json
from decimal import Decimal
from web3 import Web3
from eth_abi import encode
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

# Global placeholders for Web3 and chainId
web3 = None
chainId = None

console = Console()
console.print(Panel.fit(
    "[bold cyan]🚀 R2 Testnet Auto\n[green]By ADFMIND TEAM[/green]\n[link=https://t.me/AirdropFamilyIDN]Join Telegram[/link]",
    title="🔥 Welcome",
    subtitle="Testnet Tools"))

# Load network config
with open("network_config.json") as f:
    network_config = json.load(f)

networks_to_run = list(network_config.items())

# Load ABI
with open("tokenabi.json") as f:
    tokenabi = json.load(f)

def getNonce(sender): return int(web3.eth.get_transaction_count(sender))
def getgasPrice(): return int(web3.eth.gas_price * Decimal(1.1))

def show_status(title, sender, target, status, tx=None, gas_fee=None):
    table = Table(title=title, box=box.ROUNDED)
    table.add_column("From", justify="center")
    table.add_column("To", justify="center")
    table.add_column("Status", justify="center")
    
    if tx:
        table.add_column("TX-ID", justify="center")
    if gas_fee is not None:
        table.add_column("Gas Fee (Native)", justify="center")

    row = [sender[-6:], target[-6:], status]
    if tx:
        row.append(tx)
    if gas_fee is not None:
        row.append(f"{gas_fee:.6f}")
        
    table.add_row(*row)
    console.print(table)

def apprvCheck(tokenaddr, sender, targetaddr):
    contract = web3.eth.contract(address=tokenaddr, abi=tokenabi)
    return contract.functions.allowance(sender, targetaddr).call()

def approveTokens(tokenaddr, targetaddr, sender, senderkey):
    try:
        token_contract = web3.eth.contract(address=tokenaddr, abi=tokenabi)
        approve_tx = token_contract.functions.approve(targetaddr, 2**256 - 1).build_transaction({
            'chainId': chainId,
            'from': sender,
            'gasPrice': getgasPrice(),
            'gas': token_contract.functions.approve(targetaddr, 2**256 - 1).estimate_gas({'from': sender}),
            'nonce': getNonce(sender)
        })
        tx_hash = web3.eth.send_raw_transaction(web3.eth.account.sign_transaction(approve_tx, senderkey).rawTransaction)
        console.print(f"🔄 [yellow]Approving from {sender[-6:]} to {targetaddr[-6:]}...[/yellow]")
        web3.eth.wait_for_transaction_receipt(tx_hash)
        show_status("✅ Approve Success", sender, targetaddr, "[green]Success[/green]", web3.to_hex(tx_hash))
    except Exception as e:
        show_status("❌ Approve Error", sender, targetaddr, f"[red]{str(e)}[/red]")

def tx_process(title, sender, target, tx_hash, totalamount):
    console.print(f"⏳ [cyan]{title} {totalamount} RUSD...[/cyan]")

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    gas_used = receipt.gasUsed
    tx_detail = web3.eth.get_transaction(tx_hash)
    gas_price = tx_detail.gasPrice
    fee_native = web3.from_wei(gas_used * gas_price, 'ether')

    show_status(f"✅ {title} Success", sender, target, "[green]Success[/green]", web3.to_hex(tx_hash), fee_native)

def buyRUSD(addrtarget, sender, senderkey, amount):
    try:
        totalamount = int(amount) / 10**6
        funcbuy = bytes.fromhex('095e7a95')
        enc = encode(['address', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256'],
                     [sender, amount, 0, 0, 0, 0, 0])
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
        tx_process("Buy", sender, addrtarget, tx_hash, totalamount)
    except Exception as e:
        show_status("❌ Buy Error", sender, addrtarget, f"[red]{str(e)}[/red]")

def stakesRUSD(addrtarget, sender, senderkey, amount):
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
        tx_process("Stake", sender, addrtarget, tx_hash, totalamount)
    except Exception as e:
        show_status("❌ Stake Error", sender, addrtarget, f"[red]{str(e)}[/red]")

def addLiquidity(addrtarget, sender, senderkey, amount):
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
        tx_process("Add Liquidity", sender, addrtarget, tx_hash, totalamount)
    except Exception as e:
        show_status("❌ Liquidity Error", sender, addrtarget, f"[red]{str(e)}[/red]")

def run_actions():
    amount = int(5 * 10**6)  # jumlah USDC per aksi
    repeat = 1  # jumlah pengulangan tiap aksi per wallet

    try:
        with open("pk.txt", "r") as f:
            keys = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        console.print("[red]❌ File pk.txt tidak ditemukan![/red]")
        return

    for index, privkey in enumerate(keys, 1):
        try:
            sender = web3.eth.account.from_key(privkey)
            sender_address = sender.address
            sender_key = privkey

            console.print(f"\n[bold green]🚀 Wallet #{index}: {sender_address}[/bold green]")

            USDC = web3.to_checksum_address('0xef84994eF411c4981328fFcE5Fda41cD3803faE4')
            rUSD = web3.to_checksum_address('0x20c54C5F742F123Abb49a982BFe0af47edb38756')
            sRUSD = web3.to_checksum_address('0xBD6b25c4132F09369C354beE0f7be777D7d434fa')
            liquidity = web3.to_checksum_address('0xF64a77f6e57d9fEeFd2E8fEDbd0032798dAC21Fa')

            # Approve hanya dilakukan sekali per token per kontrak tujuan
            if apprvCheck(USDC, sender_address, rUSD) < amount:
                approveTokens(USDC, rUSD, sender_address, sender_key)
            if apprvCheck(rUSD, sender_address, sRUSD) < amount:
                approveTokens(rUSD, sRUSD, sender_address, sender_key)
            if apprvCheck(rUSD, sender_address, liquidity) < amount:
                approveTokens(rUSD, liquidity, sender_address, sender_key)
            if apprvCheck(sRUSD, sender_address, liquidity) < amount:
                approveTokens(sRUSD, liquidity, sender_address, sender_key)

            for i in range(repeat):
                console.print(f"[blue]🔁 Loop {i+1}/{repeat} untuk {sender_address[-6:]}[/blue]")
                
                buyRUSD(rUSD, sender_address, sender_key, amount)
                time.sleep(10)

                stakesRUSD(sRUSD, sender_address, sender_key, amount)
                time.sleep(10)

                addLiquidity(liquidity, sender_address, sender_key, amount)
                time.sleep(15)

            console.print(f"[cyan]✅ Semua loop selesai untuk wallet #{index} ({sender_address[-6:]})[/cyan]")
            time.sleep(15)

        except Exception as e:
            console.print(f"[red]❌ Gagal memproses wallet #{index}: {e}[/red]")

def countdown(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        hrs, mins = divmod(mins, 60)
        timer = f"{hrs:02d}:{mins:02d}:{secs:02d}"
        tanggal = datetime.now().strftime("%d/%m/%Y")
        console.print(f"📅 {tanggal} ⏳ Menunggu sebelum ulang semua jaringan: {timer}", end="\r")
        time.sleep(1)
        seconds -= 1
    print()  # supaya pindah baris setelah countdown selesai

def main_loop():
    while True:
        for network_key, netconf in networks_to_run:
            try:
                web3_local = Web3(Web3.HTTPProvider(netconf["rpcUrl"]))
                if not web3_local.is_connected():
                    console.print(f"❌ [red]Gagal konek ke jaringan {netconf['name']}[/red]")
                    continue

                global web3, chainId
                web3 = web3_local
                chainId = netconf["chainId"]

                console.print(f"\n\n[bold cyan]🔗 Jaringan: {netconf['name']} (Chain ID: {chainId})[/bold cyan]")
                run_actions()
            except Exception as e:
                console.print(f"[red]❌ Error di jaringan {netconf['name']}: {e}[/red]")

        # Log countdown 12 jam
        countdown(43200)  # 12 jam = 43200 detik

if __name__ == "__main__":
    main_loop()
