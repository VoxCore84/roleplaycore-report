@echo off
echo Refreshing content from local sources...
python "%~dp0refresh_content.py"
echo.
echo Building site...
python "%~dp0build_site.py"
echo.
echo Committing and pushing...
cd /d "%~dp0"
git add docs/
git commit -m "Site rebuild %date%"
git push
echo.
echo Done. Site will deploy in ~30 seconds.
pause
