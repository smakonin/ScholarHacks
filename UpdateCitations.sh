
head /Users/stephen/SourceCode/smakonin.github.io/scholar.js

#cd /home/pi/ScholarHacks/
cd /Users/stephen/SourceCode/ScholarHacks

cd ../smakonin.github.io/
git pull
cd ../ScholarHacks/
./GenerateCitationJSON.py
cd ../smakonin.github.io/

python3 ./SourceCode/PySitemap/main.py --url="http://makonin.com/"


git add .
git status
git commit -m 'upd citation json'
git push
#git push > /dev/null
head scholar.js
cd ../ScholarHacks/
