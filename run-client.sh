#!/bin/bash - 
#===============================================================================
#
#          FILE: run-client.sh
# 
#         USAGE: ./run-client.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 10/20/2024 14:09
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
javac -d classes LDAPInfo.java
java -cp classes LDAPInfo $1
echo Now try 'java -cp classes LDAPInfo "bob)(userPassword=a*"'
