# Raspberry Pi 5 Setup Instructions

## Step 1: Clone the Repository on Your Raspberry Pi

Open a terminal on your Raspberry Pi and run:

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/pi-bitcoin-miner.git
cd pi-bitcoin-miner
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 2: Make Scripts Executable

```bash
chmod +x install.sh
chmod +x setup_autostart.sh
```

## Step 3: Run Installation

```bash
./install.sh
```

This will install:
- Python dependencies (PyQt5, requests, psutil)
- cpuminer-multi (the actual mining software)
- All required system packages

Installation may take 10-15 minutes.

## Step 4: Configure Your Mining Pool

Before running the miner, you need to configure your mining pool settings.

1. Sign up with a mining pool (e.g., Slush Pool, F2Pool, AntPool)
2. Get your wallet address and pool connection details
3. Edit the configuration:

```bash
nano miner_dashboard.py
```

Find lines 195-201 and update with your pool details:

```python
self.miner_process = subprocess.Popen([
    'cpuminer',
    '-a', 'sha256d',
    '-o', 'stratum+tcp://your-pool.com:3333',  # Your pool URL
    '-u', 'your_wallet_address',                # Your BTC wallet
    '-p', 'x'                                   # Pool password (usually 'x')
])
```

Save with `Ctrl+X`, then `Y`, then `Enter`.

## Step 5: Run the Dashboard

```bash
python3 miner_dashboard.py
```

The GUI should launch showing the dashboard!

## Step 6: Setup Autostart (Optional)

To make the dashboard start automatically when your Pi boots:

```bash
./setup_autostart.sh
```

To disable autostart later:
```bash
rm ~/.config/autostart/bitcoin-miner.desktop
```

## Troubleshooting

### If PyQt5 doesn't install:
```bash
sudo apt-get install python3-pyqt5 python3-pyqt5.qtwidgets
```

### If cpuminer fails to compile:
```bash
sudo apt-get install build-essential libcurl4-openssl-dev libjansson-dev libssl-dev libgmp-dev
```

### Check if cpuminer installed correctly:
```bash
which cpuminer
cpuminer --version
```

### If the GUI doesn't start:
Make sure you're running on the Pi's desktop environment (not SSH without X11 forwarding).

### To run via SSH with display:
```bash
export DISPLAY=:0
python3 miner_dashboard.py
```

## Performance Tips

1. **Cooling**: Ensure your Pi 5 has adequate cooling (heatsink or fan)
2. **Power**: Use the official 27W USB-C power supply
3. **Overclocking**: You can overclock for slightly better hashrate (at your own risk)

## Monitoring

The dashboard updates every 2 seconds and shows:
- Your miner's hashrate and shares
- Bitcoin network statistics
- Real-time profitability calculations
- System temperature and resource usage

## Stopping the Miner

Click the "Stop Mining" button in the GUI, or close the window.

## Important Notes

⚠️ This is primarily educational. Bitcoin mining on a Raspberry Pi is not profitable due to the extremely low hashrate compared to ASIC miners. You'll earn essentially nothing while consuming electricity.

However, it's a great way to learn about:
- How Bitcoin mining works
- Blockchain technology
- System monitoring and optimization
- Python GUI development

Enjoy your mining experience! 🚀
