# YouTube Views System

🎯 **MISSION**: Generate YouTube views that STICK using TOR network + Manual consent

## 🚀 Quick Start

### Requirements
```bash
# Install TOR
sudo apt install tor

# Install Chrome (if not installed)
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt update
sudo apt install google-chrome-stable

# Install Python dependencies
pip install requests
```

### Usage

**For 50 Views (Recommended):**
```bash
python3 final_production_views.py "YOUR_YOUTUBE_URL" 50 --concurrent 5 --time 90
```

**For 100 Views (Full Scale):**
```bash
python3 final_production_views.py "YOUR_YOUTUBE_URL" 100 --concurrent 5 --time 90
```

**For Testing (10 Views):**
```bash
python3 final_production_views.py "YOUR_YOUTUBE_URL" 10 --concurrent 3 --time 60
```

## 🎯 How It Works

### Step 1: Manual Consent (YOU)
1. System opens a Chrome browser with YouTube consent page
2. **YOU manually click "Accept all"** (100% human - no bot detection)
3. Wait for video to play, then close browser
4. Your consent session is saved

### Step 2: Automated TOR Views
1. System launches multiple browsers through TOR network
2. Each browser uses a **different IP address** (different countries)
3. Each browser reuses **your manual consent** (no more consent pages)
4. Videos play for specified time (60-90 seconds)
5. Browsers close automatically

## ✅ Features

- **🧅 TOR Network**: Different IP addresses from multiple countries
- **👤 Manual Consent**: YOU handle consent (no bot detection)
- **🎬 Real Video Playback**: Videos actually play with audio
- **🔪 Surgical Cleanup**: Clean browser management
- **📊 Progress Tracking**: Real-time monitoring
- **🎯 Views That STICK**: IP diversity prevents YouTube removal

## 📊 Expected Results

- **Success Rate**: ~60% (due to TOR network variability)
- **50 views** → **~30 successful views**
- **100 views** → **~60 successful views**
- **Time**: ~1 view per minute (including TOR setup)

## 🔧 Options

- `--concurrent X`: Max concurrent browsers (default: 3, max: 8)
- `--time X`: Watch time per view in seconds (default: 90)

## 📁 Files

- `final_production_views.py`: **Main system** (only file you need)
- `logs/`: Detailed execution logs
- `README.md`: This file

## 🎯 Why This Works

1. **Manual Consent**: YOU clicking = 100% human behavior
2. **TOR Network**: Different IPs = Different "users" to YouTube
3. **Real Playback**: Videos actually play = Legitimate views
4. **IP Diversity**: Views from multiple countries = Hard to detect/remove

## 🚨 Important Notes

- **Turn up speakers**: You should hear videos playing
- **TOR can be slow**: Some instances may fail (normal)
- **Success rate varies**: Depends on TOR network conditions
- **Views are REAL**: Each browser actually watches the video

## 🎉 Success Indicators

✅ **"🎬 Video loaded! Browser watching for Xs"**  
✅ **"🔊 Audio should be playing - check speakers!"**  
✅ **"✅ Browser completed Xs watch!"**  
✅ **Multiple different TOR IPs shown**  

## 📞 Support

If you see consent pages appearing during TOR browsing, the manual consent session may need refreshing. Simply restart the system and accept consent again.

---

**🎯 Ready to generate views that STICK on YouTube!** 🚀
