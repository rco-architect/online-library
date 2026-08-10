@echo off
echo ===================================================
echo   Pushing Local SQL Schema to Cloudflare D1...
echo ===================================================

npx wrangler d1 execute my-library-db --remote --file=./schema.sql

echo.
echo ===================================================
echo   Verifying Live Remote Database Content:
echo ===================================================

npx wrangler d1 execute my-library-db --remote --command="SELECT * FROM books;"

pause