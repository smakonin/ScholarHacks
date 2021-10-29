head ~/SourceCode/smakonin.github.io/scholar.js

echo "*** SYNC WITH GITHUB:"
cd ~/SourceCode/smakonin.github.io/
git pull

echo "*** INGESTING GOOGLE SCHOLAR DATA:"
cd ~/SourceCode/ScholarHacks/
./GenerateCitationJSON.py
mv -v scholar.js ~/SourceCode/smakonin.github.io/

echo "*** UPDATE WITH NEW CV:"
cd ~/SourceCode/ScholarHacks/
cp -v SMakonin_CV.pdf ~/SourceCode/smakonin.github.io/doc/

#echo "*** BUILD NEW SITEMAP:"
#cd ~/SourceCode/ScholarHacks/
#python3 PySitemap/main.py --url="http://makonin.com/"
#mv -v sitemap.xml ~/SourceCode/smakonin.github.io/

echo "*** PUSH WEBSITE UPDATES:"
cd ~/SourceCode/smakonin.github.io/
git add .
git status
git commit -m 'upd citation json'
git push
#git push > /dev/null

cd ~
head ~/SourceCode/smakonin.github.io/scholar.js
