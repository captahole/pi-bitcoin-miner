# How to Publish to GitHub

## Step 1: Create a New Repository on GitHub

1. Go to https://github.com and log in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the details:
   - **Repository name**: `pi-bitcoin-miner`
   - **Description**: "Bitcoin mining dashboard for Raspberry Pi 5 with GUI, alerts, and autostart"
   - **Visibility**: Public (or Private if you prefer)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

## Step 2: Push Your Code to GitHub

After creating the repository, GitHub will show you commands. Use these in your terminal:

### On Windows (in the pi-bitcoin-miner folder):

```bash
git remote add origin https://github.com/YOUR_USERNAME/pi-bitcoin-miner.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### If you get authentication errors:

You may need to use a Personal Access Token instead of your password:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with "repo" permissions
3. Use the token as your password when pushing

Or use SSH (recommended):
```bash
git remote add origin git@github.com:YOUR_USERNAME/pi-bitcoin-miner.git
git branch -M main
git push -u origin main
```

## Step 3: Verify Upload

Go to `https://github.com/YOUR_USERNAME/pi-bitcoin-miner` and verify all files are there.

## Step 4: Clone on Raspberry Pi

Now on your Raspberry Pi, open a terminal and run:

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/pi-bitcoin-miner.git
cd pi-bitcoin-miner
chmod +x install.sh setup_autostart.sh
./install.sh
```

That's it! Follow the RASPBERRY_PI_SETUP.md file for complete setup instructions.

---

## Quick Command Summary

### On Windows (publish):
```bash
cd pi-bitcoin-miner
git remote add origin https://github.com/YOUR_USERNAME/pi-bitcoin-miner.git
git branch -M main
git push -u origin main
```

### On Raspberry Pi (clone):
```bash
cd ~
git clone https://github.com/YOUR_USERNAME/pi-bitcoin-miner.git
cd pi-bitcoin-miner
chmod +x install.sh
./install.sh
python3 miner_dashboard.py
```

---

## Updating the Repository Later

If you make changes and want to push updates:

```bash
cd pi-bitcoin-miner
git add .
git commit -m "Description of your changes"
git push
```

On your Raspberry Pi, to get updates:

```bash
cd ~/pi-bitcoin-miner
git pull
```
