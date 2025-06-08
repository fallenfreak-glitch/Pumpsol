import asyncio
import aiohttp
import datetime

PUMPFUN_API_URL = "https://pump.fun/api/tokens?sort=created&limit=100"
SOLANA_RPC = "https://api.mainnet-beta.solana.com"
HELIUS_API_KEY = "YOUR_HELIUS_API_KEY"

OUTPUT_FILE = "launches.txt"
SEEN_MINTS = set()

async def is_fresh_wallet(session, wallet_address):
    url = f"https://api.helius.xyz/v0/addresses/{wallet_address}/transactions?limit=1&api-key={HELIUS_API_KEY}"
    async with session.get(url) as resp:
        data = await resp.json()
        return len(data) == 0

async def is_lp_initialized(session, mint_address):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenLargestAccounts",
        "params": [mint_address]
    }
    async with session.post(SOLANA_RPC, json=payload) as resp:
        try:
            data = await resp.json()
            accounts = data.get("result", {}).get("value", [])
            return any(float(acc.get("amount", "0")) > 0 for acc in accounts)
        except Exception:
            return False

async def is_on_birdeye(session, mint_address):
    url = f"https://public-api.birdeye.so/public/token/{mint_address}"
    headers = {"x-chain": "solana"}
    try:
        async with session.get(url, headers=headers) as resp:
            return resp.status == 200
    except Exception:
        return False

async def monitor_pumpfun():
    print("[+] Pump.fun Tracker Started (500ms loop)")
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(PUMPFUN_API_URL) as resp:
                    tokens = await resp.json()

                for token in tokens:
                    mint = token.get("mint")
                    owner = token.get("creator")
                    symbol = token.get("symbol", "???")
                    name = token.get("name", "")
                    liquidity = token.get("liquidity", 0)

                    if mint in SEEN_MINTS or liquidity < 160:
                        continue  # Skip if seen or LP not yet initialized

                    SEEN_MINTS.add(mint)

                    # Fresh wallet check
                    is_fresh = await is_fresh_wallet(session, owner)
                    freshness = "f" if is_fresh else "o"

                    # LP check
                    has_lp = await is_lp_initialized(session, mint)
                    lp_status = "✅" if has_lp else "❌"

                    # Birdeye presence
                    birdeye_found = await is_on_birdeye(session, mint)
                    birdeye_status = "✅" if birdeye_found else "❌"

                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    output = (
                        f"DetectedAt: {now} | ${symbol} | {mint} | Wallet: {owner} "
                        f"| Fresh: {freshness} | Liquidity: ${liquidity:.2f} | LP: {lp_status} | Birdeye: {birdeye_status}"
                    )

                    print(output)
                    with open(OUTPUT_FILE, "a") as f:
                        f.write(output + "\n")

                await asyncio.sleep(0.5)  # 500ms loop
            except Exception as e:
                print(f"[!] Error: {e}")
                await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(monitor_pumpfun())
