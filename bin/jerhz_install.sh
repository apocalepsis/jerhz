#!/bin/bash

NEW_SETUP=0
JERHZ_DIR="/var/jerhz"
JERHZ_EFS_DIR="$JERHZ_DIR/efs"
S3_REPO="s3://aws.demos.jerhz"
MYSQL_JAVA_CONNECTOR="mysql-connector-java-5.1.44-bin"
MYSQL_JAVA_CONNECTOR_PKG="$MYSQL_JAVA_CONNECTOR.jar"
MYSQL_PYTHON_CONNECTOR="mysql-connector-python-2.1.7"
MYSQL_PYTHON_CONNECTOR_PKG="$MYSQL_PYTHON_CONNECTOR.tar.gz"

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

mkdir -p "/tmp"

printf ">>> Setting up python ...\n"

printf "> Installing pycrypto ... "
python3 -m pip install --upgrade pip
python3 -m pip install pycrypto
if [[ $? != 0 ]]; then
    printf "[ERROR] An error occurred during installation.\n"
    exit 1
fi
printf "done.\n"

printf "<<< Done.\n\n"

printf ">>> Setting up mysql ...\n"

printf "> Downloading mysql java connector ... "
aws s3 cp "$S3_REPO/mysql/$MYSQL_JAVA_CONNECTOR_PKG" "/tmp/"
printf "done.\n"

printf "> Setup mysql java connector ..."
mv "/tmp/$MYSQL_JAVA_CONNECTOR_PKG" "/usr/lib/zeppelin/lib/"
printf "done.\n"

printf "> Downloading mysql python connector ... "
aws s3 cp "$S3_REPO/mysql/$MYSQL_PYTHON_CONNECTOR_PKG" "/tmp/"
printf "done.\n"

printf "> Setup mysql python connector ..."
cd "/tmp"
tar -xzf "/tmp/$MYSQL_PYTHON_CONNECTOR_PKG"
cd "$MYSQL_PYTHON_CONNECTOR"
python3 setup.py install
printf "done.\n"

printf "<<< Done.\n\n"
