# Quick Reference Card

## 📁 Project Structure
```
midi-harmonizer-web-app/
├── backend/          → Python Flask API
├── frontend/         → React application
├── README.md         → Main documentation
├── SETUP.md          → Setup instructions
└── .gitignore        → Git ignore rules
```

## 🚀 Quick Start Commands

### First Time Setup
```bash
# Navigate to project
cd "C:\MIDI harmonizer web app"

# Setup backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Setup frontend (in new terminal)
cd frontend
npm install
```

### Daily Development

**Start Backend:**
```bash
cd backend
venv\Scripts\activate
python app.py
# Running on http://localhost:5000
```

**Start Frontend:**
```bash
cd frontend
npm start
# Opens http://localhost:3000
```

## 🔧 Git Commands

### Initial Push to GitHub
```bash
# Create repo on GitHub first, then:
git remote add origin https://github.com/chinmayjpatel/midi-harmonizer-web-app.git
git branch -M main
git push -u origin main
```

### Regular Workflow
```bash
# Check status
git status

# Add changes
git add .
# or add specific files:
git add backend/app.py

# Commit
git commit -m "Description of changes"

# Push to GitHub
git push

# Pull latest
git pull
```

### Branching
```bash
# Create new feature branch
git checkout -b feature/harmony-styles

# Switch branches
git checkout main

# List branches
git branch

# Push branch to GitHub
git push -u origin feature/harmony-styles

# Merge branch (from main)
git merge feature/harmony-styles

# Delete branch
git branch -d feature/harmony-styles
```

## 🐛 Debugging

### Check if services are running
```bash
# Check backend
curl http://localhost:5000/api/health

# Check frontend
# Open http://localhost:3000 in browser
```

### Common Issues

**Virtual environment not activated:**
```bash
cd backend
venv\Scripts\activate
# You should see (venv) in prompt
```

**Port already in use:**
```bash
# Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Dependencies out of date:**
```bash
# Backend
pip install -r requirements.txt --upgrade

# Frontend
npm update
```

## 📦 Package Management

### Python (Backend)
```bash
# Install new package
pip install package-name

# Save to requirements
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

### Node (Frontend)
```bash
# Install new package
npm install package-name

# Install dev dependency
npm install --save-dev package-name

# Update packages
npm update
```

## 🧪 Testing

### Backend Tests (future)
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 Project Stats

### View Git History
```bash
git log --oneline
git log --graph --oneline --all
```

### View File Changes
```bash
git diff
git diff filename.py
```

### View Contributors
```bash
git shortlog -sn
```

## 🌐 Useful URLs

- **Frontend Dev**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health
- **GitHub Repo**: https://github.com/chinmayjpatel/midi-harmonizer-web-app

## 🎯 Development Checklist

- [ ] Backend running ✓
- [ ] Frontend running ✓
- [ ] Can upload MIDI file ✓
- [ ] Harmonization works ✓
- [ ] Can download result ✓
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Code committed
- [ ] Changes pushed to GitHub

## 💡 Pro Tips

1. **Commit Often**: Small, frequent commits are better than large ones
2. **Descriptive Messages**: Write clear commit messages
3. **Pull Before Push**: Always `git pull` before `git push`
4. **Feature Branches**: Use branches for new features
5. **Test Before Commit**: Make sure code works before committing
6. **Keep README Updated**: Document new features

## 🆘 Need Help?

- Check SETUP.md for detailed instructions
- Check README.md for project overview
- GitHub Issues: Report bugs or request features
- Stack Overflow: For technical questions

---
Made with ❤️ by Trixx
