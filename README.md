# Raspberry Pi 5 Bitcoin Miner Dashboard

A desktop GUI application for Bitcoin mining on Raspberry Pi 5 with real-time monitoring, alerts, and autostart capability.

## Features

- **Real-time Dashboard** with PyQt5 GUI
- **Miner Statistics**: Hashrate, shares, uptime
- **Bitcoin Network Data**: Difficulty, block height, network hashrate
- **Profitability Calculator**: BTC price, estimated earnings, power costs
- **System Monitoring**: CPU temperature, memory, load
- **Temperature Alerts**: Notifications when CPU gets too hot
- **Autostart**: Launch on boot

## Installation

1. Clone or copy this directory to your Raspberry Pi 5
2. Run the installation script:
```bash
chmod +x install.sh
./install.sh
```

3. Configure your mining pool in `miner_dashboard.py` (line 195-201):
```python
self.miner_process = subprocess.Popen([
    'cpuminer',
    '-a', 'sha256d',
    '-o', 'stratum+tcp://your-pool.com:3333',
    '-u', 'your_wallet_address',
    '-p', 'x'
])
```

4. Setup autostart (optional):
```bash
chmod +x setup_autostart.sh
./setup_autostart.sh
```

## Usage

Run the dashboard:
```bash
python3 miner_dashboard.py
```

## Mining Pool Configuration

You'll need to sign up with a mining pool. Popular options:
- Slush Pool (slushpool.com)
- F2Pool (f2pool.com)
- AntPool (antpool.com)

Get your wallet address and pool connection details, then update the miner configuration.

## Important Notes

⚠️ **Reality Check**: Bitcoin mining on a Raspberry Pi is NOT profitable. The hashrate is extremely low compared to ASIC miners, and you'll spend more on electricity than you'll earn. This is primarily an educational project.

- Raspberry Pi 5 hashrate: ~100-200 KH/s
- Modern ASIC miners: 100+ TH/s (1,000,000x faster)
- Network difficulty is optimized for ASICs

## Power Consumption

- Raspberry Pi 5: ~5W during mining
- Estimated daily cost: $0.01-0.02 (at $0.12/kWh)
- Estimated daily earnings: $0.0000001 (essentially zero)

## Customization

Edit `miner_dashboard.py` to customize:
- Update intervals (line 113, 119)
- Power cost per kWh (line 186)
- Alert thresholds (line 157)
- Mining algorithm (line 196)

## Troubleshooting

If the dashboard doesn't start:
```bash
# Check Python version
python3 --version

# Install PyQt5 manually
sudo apt-get install python3-pyqt5

# Check if cpuminer is installed
which cpuminer
```

## License

MIT License - Educational purposes only
