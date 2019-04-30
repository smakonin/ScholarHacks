
#cd /home/pi/ScholarHacks/
cd /Users/stephen/SourceCode/ScholarHacks

cd ../smakonin.github.io/
git pull
cd ../ScholarHacks/
./GenerateCitationJSON.py
cd ../smakonin.github.io/
git add .
git status
git commit -m 'upd citation json'
git push > /dev/null
cd ../ScholarHacks/
