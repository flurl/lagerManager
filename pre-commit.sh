#/bin/bash
#this script is used as pre-commit hook for git
#to install do ln -s ../../pre-commit.sh .git/hooks/pre-commit


#increase version number
OLDVER=$(python version.py)

NEWVER=$(expr $OLDVER + 1)
echo "Increasing version number to $NEWVER"

sed -i "1s/.*/VERSION=$NEWVER/" version.py 
