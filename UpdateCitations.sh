cd ../smakonin.github.io
git pull
cd ../ScholarHacks
./GenerateCitationJSON.py
cd ../smakonin.github.io
git add .
git commit -m 'upd citation json' --quiet
git push > /dev/null --quiet
cd ../ScholarHacks
