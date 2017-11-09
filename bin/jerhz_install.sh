#!/bin/bash

NEW_SETUP=0

JERHZ_TMP_DIR="/tmp/jerhz"
JERHZ_DIR="/var/jerhz"
JERHZ_EFS_DIR="$JERHZ_DIR/efs"
JERHZ_USERS_DIR="$JERHZ_EFS_DIR/users"
JERHZ_ZEPPELIN_DIR="$JERHZ_EFS_DIR/zeppelin"
JERHZ_ZEPPELIN_NB_DIR="$JERHZ_ZEPPELIN_DIR/notebook"
JERHZ_EFS_HOST="fs-7a5c1733.efs.us-east-1.amazonaws.com"

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

printf ">>> Setting up jerhz ...\n"

mkdir -p $JERHZ_DIR
mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 $JERHZ_EFS_HOST:/ $JERHZ_DIR

if [[ $NEW_SETUP = 1 ]]; then
    printf "> Setting up new install ..."
    rm -rf "$JERHZ_DIR/*"
    mkdir -p "$JERHZ_EFS_DIR"
    mkdir -p "$JERHZ_USERS_DIR"
    mkdir -p "$JERHZ_ZEPPELIN_DIR"
    chown zeppelin:zeppelin "$JERHZ_ZEPPELIN_DIR"
    mkdir -p "$JERHZ_ZEPPELIN_NB_DIR"
    chown zeppelin:zeppelin "$JERHZ_ZEPPELIN_NB_DIR"
    printf "done.\n"
fi

printf "<<< Done.\n\n"

mkdir -p "$JERHZ_TMP_DIR"
cd "$JERHZ_TMP_DIR"

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
aws s3 cp "$S3_REPO/mysql/$MYSQL_JAVA_CONNECTOR_PKG" .
printf "done.\n"

printf "> Setup mysql java connector ..."
mv "$MYSQL_JAVA_CONNECTOR_PKG" "/usr/lib/zeppelin/lib/"
printf "done.\n"

printf "> Downloading mysql python connector ... "
aws s3 cp "$S3_REPO/mysql/$MYSQL_PYTHON_CONNECTOR_PKG" .
printf "done.\n"

printf "> Setup mysql python connector ..."
tar -xzf "$MYSQL_PYTHON_CONNECTOR_PKG"
cd "$MYSQL_PYTHON_CONNECTOR"
python3 setup.py install
printf "done.\n"

cd "$JERHZ_TMP_DIR"

printf "<<< Done.\n\n"

printf ">>> Setting up zeppelin ...\n"

stop zeppelin

printf "> Setting up shiro"

aws s3 cp "$S3_REPO/zeppelin/zeppelin-site.xml" .
mv "zeppelin-site.xml" "/usr/lib/zeppelin/conf/"

aws s3 cp "$S3_REPO/zeppelin/shiro.ini" .
mv "shiro.ini" "/usr/lib/zeppelin/conf/"

aws s3 cp "$S3_REPO/zeppelin/zeppelin-env.sh" .
mv "zeppelin-env.sh" "/usr/lib/zeppelin/conf/"

rm -rf "/var/lib/zeppelin/notebook"
ln -s "$JERHZ_ZEPPELIN_NB_DIR" "/var/lib/zeppelin/notebook"

printf "done.\n"

start zeppelin

printf "<<< Done.\n\n"
