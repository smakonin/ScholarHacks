echo "*** SYNC WITH GITHUB:"
cd ~/SourceCode/smakonin.github.io/
git pull

echo "*** BUILD NEW SITEMAP:"
cd ~/SourceCode/ScholarHacks/
python3 PySitemap/main.py --url="http://makonin.com/"
mv -v sitemap.xml ~/SourceCode/smakonin.github.io/

echo "*** PUSH WEBSITE UPDATES:"
cd ~/SourceCode/smakonin.github.io/
git add .
git status
git commit -m 'upd sitemap json'
git push

cd ~
