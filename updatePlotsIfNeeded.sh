dir=$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )
datadir=$dir/covid-19-data

cd $datadir
git remote update
if git status -uno | grep behind > /dev/null; then
    git merge
    cd $dir
    ./plotstatecounties.py --no-show
    ./plotstatecounties.py --no-show --deaths
    git add plots/
    git commit -m "Automatic: Update plots $(date)"
fi
