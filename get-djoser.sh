python_version=$(ls $VIRTUAL_ENV/lib | grep python)
site_packages=$VIRTUAL_ENV/lib/$python_version/site-packages/

echo "You are using virtualenv $(basename $VIRTUAL_ENV) ($VIRTUAL_ENV)"
read -p "Add djoser from https://github.com/mjuopperi/djoser/releases/0.3.2? [y/n]" -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
  if command -v curl >/dev/null 2>&1
  then
    echo "Getting djoser 0.3.2..."
    curl -L -o $site_packages/djoser.tar.gz https://github.com/mjuopperi/djoser/releases/download/0.3.2/0.3.2.tar.gz
    tar xvf $site_packages/djoser.tar.gz -C $site_packages
    rm $site_packages/djoser.tar.gz
    echo "Done."
  else
    echo "curl is not installed."
  fi
fi
