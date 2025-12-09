# Setup Instructions for Windows

## Step 1: Copy Project to Your Directory

I've created the entire project structure here. You need to copy it to your Windows directory.

### Option A: Using Windows Explorer (Easiest)
1. Open File Explorer
2. Navigate to: `\\wsl$\Ubuntu\home\claude\midi-harmonizer-web-app`
3. Copy the entire `midi-harmonizer-web-app` folder
4. Paste it to `C:\MIDI harmonizer web app`

### Option B: Using Command Line
Open PowerShell and run:
```powershell
# From WSL/Linux side, if you have access:
cp -r /home/claude/midi-harmonizer-web-app/* "/mnt/c/MIDI harmonizer web app/"

# OR from Windows PowerShell:
wsl cp -r /home/claude/midi-harmonizer-web-app/* "/mnt/c/MIDI harmonizer web app/"
```

## Step 2: Navigate to Your Project Directory

Open Command Prompt or PowerShell:
```cmd
cd "C:\MIDI harmonizer web app"
```

## Step 3: Create GitHub Repository

### Using GitHub CLI (if installed):
```bash
gh repo create midi-harmonizer-web-app --public --source=. --remote=origin --push
```

### Using Git Commands (manual):
```bash
# The repo is already initialized with a commit!
# Just add your GitHub remote and push

# Add your GitHub remote (replace YOUR_USERNAME if different)
git remote add origin https://github.com/chinmayjpatel/midi-harmonizer-web-app.git

# Push to GitHub
git push -u origin master
```

### Using GitHub Web Interface:
1. Go to https://github.com/new
2. Repository name: `midi-harmonizer-web-app`
3. Make it Public
4. **DO NOT** initialize with README (we already have one)
5. Click "Create repository"
6. Then run these commands:
```bash
git remote add origin https://github.com/chinmayjpatel/midi-harmonizer-web-app.git
git branch -M main
git push -u origin main
```

## Step 4: Set Up the Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Step 5: Set Up the Frontend

```bash
cd ..\frontend
npm install
```

## Step 6: Run the Application

### Terminal 1 - Backend:
```bash
cd backend
venv\Scripts\activate
python app.py
```

### Terminal 2 - Frontend:
```bash
cd frontend
npm start
```

## Verification

✅ Backend should be running on: http://localhost:5000
✅ Frontend should open automatically at: http://localhost:3000

## Next Steps

1. Test the application with a sample MIDI file
2. Start developing additional features
3. Train the ML model with dataset
4. Add more harmonization styles

## Troubleshooting

**If you get "git not found":**
- Install Git from: https://git-scm.com/download/win

**If you get Python errors:**
- Make sure Python 3.9+ is installed
- Check: `python --version`

**If npm fails:**
- Install Node.js from: https://nodejs.org/

**Port already in use:**
```bash
# Backend (5000)
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Frontend (3000)
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F
```

## Git Workflow Going Forward

```bash
# Make changes to files
git add .
git commit -m "Descriptive message about changes"
git push

# Pull latest changes
git pull

# Create a new branch for features
git checkout -b feature/new-feature
git push -u origin feature/new-feature
```

Happy coding! 🚀
