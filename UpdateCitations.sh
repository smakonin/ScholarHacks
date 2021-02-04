
head ~/SourceCode/smakonin.github.io/scholar.js

#cd /home/pi/ScholarHacks/
cd ~/SourceCode/ScholarHacks

echo "*** INGESTING GOOGLE SCHOLAR DATA:"
cd ../smakonin.github.io/
git pull
cd ../ScholarHacks/
./GenerateCitationJSON.py
cd ../smakonin.github.io/

echo "*** UPDATE WITH NEW CV:"
cp -v ~/Documents/Job\ Docs/SMakonin_CV.pdf ./doc/

#echo "*** BUILD NEW SITEMAP:"
#python3 ~/SourceCode/PySitemap/main.py --url="http://makonin.com/"

echo "*** PUSH WEBSITE UPDATES:"
git add .
git status
git commit -m 'upd citation json'
git push
#git push > /dev/null

head scholar.js
cd ../ScholarHacks/
