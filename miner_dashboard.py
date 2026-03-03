#!/usr/bin/env python3
import sys
import json
import subprocess
import time
import requests
import psutil
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QGroupBox, QPushButton, QMessageBox)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

class MinerDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.start_time = datetime.now()
        self.shares_accepted = 0
        self.shares_rejected = 0
        self.total_shares = 0
        self.hashrate = 0
        self.miner_process = None
        
        self.initUI()
        self.start_monitoring()
        
    def initUI(self):
        self.setWindowTitle('Raspberry Pi Bitcoin Miner Dashboard')
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel('Bitcoin Mining Dashboard')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Miner Section
        miner_group = self.create_miner_section()
        main_layout.addWidget(miner_group)
        
        # Bitcoin Network Section
        network_group = self.create_network_section()
        main_layout.addWidget(network_group)
        
        # Profit Section
        profit_group = self.create_profit_section()
        main_layout.addWidget(profit_group)
        
        # System Section
        system_group = self.create_system_section()
        main_layout.addWidget(system_group)
        
        # Control Buttons
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton('Start Mining')
        self.start_btn.clicked.connect(self.toggle_mining)
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        button_layout.addWidget(self.start_btn)
        main_layout.addLayout(button_layout)
        
    def create_miner_section(self):
        group = QGroupBox('Miner Status')
        layout = QVBoxLayout()
        
        self.hashrate_label = QLabel('Hashrate: 0 H/s')
        self.shares_label = QLabel('Shares Submitted: 0')
        self.accepted_label = QLabel('Accepted: 0 | Rejected: 0')
        self.uptime_label = QLabel('Uptime: 00:00:00')
        
        for label in [self.hashrate_label, self.shares_label, 
                     self.accepted_label, self.uptime_label]:
            label.setFont(QFont('Arial', 11))
            layout.addWidget(label)
            
        group.setLayout(layout)
        return group
        
    def create_network_section(self):
        group = QGroupBox('Bitcoin Network')
        layout = QVBoxLayout()
        
        self.difficulty_label = QLabel('Difficulty: Loading...')
        self.block_height_label = QLabel('Block Height: Loading...')
        self.network_hashrate_label = QLabel('Network Hashrate: Loading...')
        
        for label in [self.difficulty_label, self.block_height_label, 
                     self.network_hashrate_label]:
            label.setFont(QFont('Arial', 11))
            layout.addWidget(label)
            
        group.setLayout(layout)
        return group
        
    def create_profit_section(self):
        group = QGroupBox('Profitability')
        layout = QVBoxLayout()
        
        self.btc_price_label = QLabel('BTC Price: $0.00')
        self.earnings_label = QLabel('Est. Daily Earnings: $0.00')
        self.power_cost_label = QLabel('Est. Daily Power Cost: $0.00')
        
        for label in [self.btc_price_label, self.earnings_label, 
                     self.power_cost_label]:
            label.setFont(QFont('Arial', 11))
            layout.addWidget(label)
            
        group.setLayout(layout)
        return group
        
    def create_system_section(self):
        group = QGroupBox('System Status')
        layout = QVBoxLayout()
        
        self.cpu_temp_label = QLabel('CPU Temp: 0°C')
        self.memory_label = QLabel('Memory: 0%')
        self.load_label = QLabel('CPU Load: 0%')
        
        for label in [self.cpu_temp_label, self.memory_label, self.load_label]:
            label.setFont(QFont('Arial', 11))
            layout.addWidget(label)
            
        group.setLayout(layout)
        return group
        
    def start_monitoring(self):
        # Update timer - every 2 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(2000)
        
        # Network data timer - every 30 seconds
        self.network_timer = QTimer()
        self.network_timer.timeout.connect(self.update_network_data)
        self.network_timer.start(30000)
        self.update_network_data()
        
    def update_dashboard(self):
        # Update uptime
        uptime = datetime.now() - self.start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        self.uptime_label.setText(f'Uptime: {hours:02d}:{minutes:02d}:{seconds:02d}')
        
        # Update system stats
        self.update_system_stats()
        
        # Simulate mining stats (replace with actual miner API calls)
        if self.miner_process:
            self.hashrate = 100000 + (time.time() % 10000)  # Simulated
            self.hashrate_label.setText(f'Hashrate: {self.hashrate/1000:.2f} KH/s')
            
    def update_system_stats(self):
        # CPU Temperature
        try:
            temp = psutil.sensors_temperatures()
            if 'cpu_thermal' in temp:
                cpu_temp = temp['cpu_thermal'][0].current
                self.cpu_temp_label.setText(f'CPU Temp: {cpu_temp:.1f}°C')
                
                # Alert if temperature too high
                if cpu_temp > 75:
                    self.show_alert('High Temperature', 
                                  f'CPU temperature is {cpu_temp:.1f}°C!')
        except:
            self.cpu_temp_label.setText('CPU Temp: N/A')
            
        # Memory usage
        memory = psutil.virtual_memory()
        self.memory_label.setText(f'Memory: {memory.percent:.1f}%')
        
        # CPU load
        cpu_load = psutil.cpu_percent(interval=0.1)
        self.load_label.setText(f'CPU Load: {cpu_load:.1f}%')
        
    def update_network_data(self):
        try:
            # Get Bitcoin price
            response = requests.get('https://api.coindesk.com/v1/bpi/currentprice/BTC.json', 
                                  timeout=5)
            data = response.json()
            btc_price = float(data['bpi']['USD']['rate'].replace(',', ''))
            self.btc_price_label.setText(f'BTC Price: ${btc_price:,.2f}')
            
            # Get blockchain info
            response = requests.get('https://blockchain.info/q/getdifficulty', timeout=5)
            difficulty = float(response.text)
            self.difficulty_label.setText(f'Difficulty: {difficulty:,.0f}')
            
            response = requests.get('https://blockchain.info/q/getblockcount', timeout=5)
            block_height = int(response.text)
            self.block_height_label.setText(f'Block Height: {block_height:,}')
            
            # Calculate network hashrate (approximate)
            network_hashrate = difficulty * 2**32 / 600 / 1e12  # TH/s
            self.network_hashrate_label.setText(f'Network Hashrate: {network_hashrate:.2f} TH/s')
            
            # Calculate profitability
            self.calculate_profitability(btc_price, difficulty)
            
        except Exception as e:
            print(f"Error fetching network data: {e}")
            
    def calculate_profitability(self, btc_price, difficulty):
        # Raspberry Pi 5 power consumption ~5W for mining
        power_watts = 5
        power_cost_kwh = 0.12  # $0.12 per kWh (adjust for your location)
        
        daily_power_cost = (power_watts / 1000) * 24 * power_cost_kwh
        self.power_cost_label.setText(f'Est. Daily Power Cost: ${daily_power_cost:.4f}')
        
        # Calculate estimated earnings (very rough estimate)
        if self.hashrate > 0:
            blocks_per_day = 144
            block_reward = 3.125  # Current BTC block reward
            daily_btc = (self.hashrate / (difficulty * 2**32 / 600)) * blocks_per_day * block_reward
            daily_usd = daily_btc * btc_price
            self.earnings_label.setText(f'Est. Daily Earnings: ${daily_usd:.8f}')
            
            # Alert if unprofitable
            if daily_usd < daily_power_cost:
                net = daily_usd - daily_power_cost
                self.earnings_label.setText(
                    f'Est. Daily Earnings: ${daily_usd:.8f} (Net: ${net:.4f})')
        
    def toggle_mining(self):
        if self.miner_process is None:
            self.start_mining()
        else:
            self.stop_mining()
            
    def start_mining(self):
        # Start cpuminer-multi (you'll need to install this)
        # This is a placeholder - configure with your pool details
        try:
            # Example: self.miner_process = subprocess.Popen([
            #     'cpuminer',
            #     '-a', 'sha256d',
            #     '-o', 'stratum+tcp://pool.example.com:3333',
            #     '-u', 'your_wallet_address',
            #     '-p', 'x'
            # ])
            self.miner_process = True  # Simulated for now
            self.start_btn.setText('Stop Mining')
            self.start_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px;")
            self.show_alert('Mining Started', 'Bitcoin mining has started!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to start miner: {e}')
            
    def stop_mining(self):
        if self.miner_process:
            # if isinstance(self.miner_process, subprocess.Popen):
            #     self.miner_process.terminate()
            self.miner_process = None
            self.start_btn.setText('Start Mining')
            self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
            self.hashrate = 0
            self.hashrate_label.setText('Hashrate: 0 H/s')
            
    def show_alert(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()
        
    def closeEvent(self, event):
        self.stop_mining()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = MinerDashboard()
    dashboard.show()
    sys.exit(app.exec_())
