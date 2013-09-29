#/bin/bash
#this script is used as pre-commit hook for git
#to install do ln -s ../../pre-commit.sh .git/hooks/pre-commit


#increase version number
OLDVER=$(python version.py)

NEWVER=$(expr $OLDVER + 1)
echo "Increasing version number to $NEWVER"

sed -i "1s/.*/VERSION=$NEWVER/" version.py 

#insert version number in new sql files for 
#use in the automatic updater
for FILE in $(git diff --cached --name-status | egrep "^A.*sql/.*\.sql" | cut -f2); do sed -i "1i #V$NEWVER" $FILE; done

git add version.py
