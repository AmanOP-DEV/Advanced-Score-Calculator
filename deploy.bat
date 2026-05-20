@echo off
title JEE Advanced 2026 Calculator - Deployer
color 0b
echo =============================================================
echo    🚀 JEE ADVANCED 2026 SCORE CALCULATOR - GITHUB DEPLOYER
echo =============================================================
echo.
echo This utility will initialize a Git repository in this folder
echo and deploy it to a new public GitHub Repository of your choice.
echo.
echo -------------------------------------------------------------
echo STEP 1: Create a new GitHub Repository
echo -------------------------------------------------------------
echo 1. Open your browser and go to: https://github.com/new
echo 2. Set Repository Name to: jee-advanced-calculator
echo 3. Make sure the repository is PUBLIC (so Pages can host it).
echo 4. Keep "Add a README", ".gitignore", and "License" UNCHECKED.
echo 5. Click "Create repository".
echo.
echo -------------------------------------------------------------
echo STEP 2: Input your Repository URL
echo -------------------------------------------------------------
set /p REPO_URL="Paste the HTTPS repository URL (e.g., https://github.com/yourusername/jee-advanced-calculator.git): "
if "%REPO_URL%"=="" (
    echo [ERROR] Repository URL cannot be empty! Exiting.
    pause
    exit
)
echo.
echo -------------------------------------------------------------
echo STEP 3: Initializing Git and Staging Files...
echo -------------------------------------------------------------
git init
git add .
git commit -m "Initial release of JEE Advanced 2026 Calculator with response sheet parser and coaching keys"
git branch -M main
git remote add origin %REPO_URL%
echo.
echo -------------------------------------------------------------
echo STEP 4: Pushing files to GitHub...
echo -------------------------------------------------------------
git push -u origin main
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [WARNING] Direct push failed. This usually happens if you're not logged into git in this shell.
    echo Try running: git push -u origin main manually or via VS Code git integration.
) else (
    echo [SUCCESS] Files successfully pushed to GitHub!
)
echo.
echo -------------------------------------------------------------
echo STEP 5: Enable GitHub Pages (Free Hosting)
echo -------------------------------------------------------------
echo 1. Go to your repository settings page on GitHub.
echo 2. Click "Pages" on the left sidebar.
echo 3. Under "Build and deployment", set Source to "Deploy from a branch".
echo 4. Select "main" as your branch, keep folder as "/ (root)", and click "Save".
echo 5. Your premium calculator will be LIVE and available to everyone in 60 seconds!
echo.
echo Press any key to exit...
pause > nul
