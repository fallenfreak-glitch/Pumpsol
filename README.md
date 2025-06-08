sample output
2025-06-07 18:13:42 | $DOGE69 | 9xJVu6...pump | Wallet: F3aB...xyz | Fresh: f | Liquidity: $165.33 | LP: ✅ | Birdeye: ❌
2025-06-07 18:14:01 | $PEPE420 | 3sQ2u9...pump | Wallet: GcD8...abc | Fresh: o | Liquidity: $178.92 | LP: ✅ | Birdeye: ✅

what this bit do
| Feature                       | Description                                              |
| ----------------------------- | -------------------------------------------------------- |
| 🚀 **Real-time tracking**     | Polls Pump.fun API every 500ms                           |
| 🔍 **Fresh wallet detection** | Uses Helius to detect if token creator is a fresh wallet |
| 💧 **Liquidity check**        | Reads `liquidity` directly from Pump.fun API             |
| 🛢️ **LP status**             | Uses Solana RPC `getTokenLargestAccounts`                |
| 🪙 **Birdeye check**          | Optional: verifies if token is on Birdeye                |
| 📁 **Logs to file**           | Writes output to `launches.txt`                          |
| 🧠 **Skips duplicates**       | Tracks already-seen tokens in memory                     |
