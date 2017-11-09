#!/bin/bash

NEW_SETUP=0
JERHZ_DIR="/var/jerhz"
JERHZ_EFS_DIR="$JERHZ_DIR/efs"

#===============================================================================
#    ARGUMENTS PARSING
#===============================================================================
printf ">>> Validating arguments ...\n"

if [[ $# > 0 ]]; then

    while [[ "$1" != "" ]]; do

        case "$1" in
            "-new" )
            NEW_SETUP=1
            printf "Argument <%s>,Value <%s>\n" "new" $NEW_SETUP
        esac
        
        shift
    
    done

fi

printf "<<< Done.\n\n"

printf ">>> Setting up python ...\n"

printf "> Installing pycrypto ... "
python3 -m pip install pycrypto
if [[ $? != 0 ]]; then
    printf "[ERROR] An error occurred during installation.\n"
    exit 1
fi
printf "done.\n"

printf "<<< Done.\n\n"
