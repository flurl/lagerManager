#!/bin/bash
#this file is used as commit-msg hook for git
#to install do ln -s ../../commit-msg.sh .git/hooks/commit-msg


#append version to commit msg
VERSION=$(python version.py)
echo "V#$VERSION" >> $1
