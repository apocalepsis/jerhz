#!/bin/bash

NEW_SETUP=0

JERHZ_DIR="/opt/jerhz"
JERHZ_TMP_DIR="/tmp/jerhz"
JERHZ_SRC_DIR="$JERHZ_DIR/src"
JERHZ_EFS_DIR="$JERHZ_DIR/efs"
JERHZ_USERS_DIR="$JERHZ_EFS_DIR/users"
JERHZ_ZEPPELIN_DIR="$JERHZ_EFS_DIR/zeppelin"
JERHZ_ZEPPELIN_NB_DIR="$JERHZ_ZEPPELIN_DIR/notebook"
JERHZ_EFS_HOST="fs-267d516f.efs.us-east-1.amazonaws.com"

S3_JERHZ_REPO="s3://aws.jerhz.boi"
S3_3P_REPO="$S3_JERHZ_REPO/3p"

ZEPPELIN_DIR="/usr/lib/zeppelin"
ZEPPELIN_NB_DIR="/var/lib/zeppelin/notebook"

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

sudo mkdir -p "$JERHZ_DIR"

sudo mkdir -p "$JERHZ_EFS_DIR"
sudo mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 $JERHZ_EFS_HOST:/ $JERHZ_EFS_DIR

if [[ $NEW_SETUP = 1 ]]; then
    printf "> Setting up new install ... "
    sudo rm -rf $JERHZ_EFS_DIR/*
    sudo mkdir -p "$JERHZ_USERS_DIR"
    sudo mkdir -p "$JERHZ_ZEPPELIN_DIR"
    sudo mkdir -p "$JERHZ_ZEPPELIN_NB_DIR"
    printf "done.\n"
fi

printf "> Setting up zeppelin folder ... "
sudo chmod -R o+w "$JERHZ_ZEPPELIN_DIR"
printf "done.\n"

printf "> Setting up library ... \n"

sudo mkdir -p "$JERHZ_DIR/src"
sudo rm -rf $JERHZ_DIR/src/*
sudo aws s3 cp "$S3_JERHZ_REPO/src/" "$JERHZ_DIR/src/" --recursive
 
printf "done.\n"

printf "<<< Done.\n\n"

printf ">>> Setting up python ...\n"

printf "> Installing pycrypto ... "

sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install pycrypto

printf "done.\n"

printf "<<< Done.\n\n"

printf ">>> Setting up mysql ...\n"

printf "> Setting up mysql java connector ... "
sudo aws s3 cp "$S3_3P_REPO/mysql/$MYSQL_JAVA_CONNECTOR_PKG" "$ZEPPELIN_DIR/lib/"
printf "done.\n"

printf "> Setup mysql python connector ..."
sudo mkdir -p "$JERHZ_TMP_DIR"
cd "$JERHZ_TMP_DIR"
sudo aws s3 cp "$S3_3P_REPO/mysql/$MYSQL_PYTHON_CONNECTOR_PKG" .
sudo tar -xzf "$MYSQL_PYTHON_CONNECTOR_PKG"
cd "$MYSQL_PYTHON_CONNECTOR"
sudo python3 setup.py install
cd "$JERHZ_TMP_DIR"
sudo rm -rf "$MYSQL_PYTHON_CONNECTOR"
printf "done.\n"

printf "<<< Done.\n\n"

sudo mkdir -p "$JERHZ_TMP_DIR"
cd "$JERHZ_TMP_DIR"

printf ">>> Setting up zeppelin ...\n"

sudo stop zeppelin

printf "> Setting up configuration ... "

cd "$ZEPPELIN_DIR/conf/"

sudo aws s3 cp "$S3_3P_REPO/zeppelin/conf/zeppelin-site.xml" .
sudo chown zeppelin:zeppelin "zeppelin-site.xml"

sudo aws s3 cp "$S3_3P_REPO/zeppelin/conf/zeppelin-env.sh" .
sudo chown zeppelin:zeppelin "zeppelin-env.sh"

sudo aws s3 cp "$S3_3P_REPO/zeppelin/conf/interpreter.json" .
sudo chown zeppelin:zeppelin "interpreter.json"

sudo aws s3 cp "$S3_3P_REPO/zeppelin/conf/shiro.ini" .
sudo chown zeppelin:zeppelin "shiro.ini"

sudo rm -rf "/var/lib/zeppelin/notebook"
sudo ln -s "$JERHZ_ZEPPELIN_NB_DIR" "$ZEPPELIN_NB_DIR"
printf "done.\n"

printf "> Setting up JDBC Interpreter ... "

cd "$ZEPPELIN_DIR/bin"
sudo ./install-interpreter.sh --name jdbc
sudo aws s3 cp "$S3_3P_REPO/zeppelin/interpreter/jdbc/" "$ZEPPELIN_DIR/interpreter/jdbc/" --recursive

printf "done.\n"

sudo start zeppelin

printf "<<< Done.\n\n"

cd "$JERHZ_TMP_DIR"

printf "> Setting up users ... \n"

cd "$JERHZ_SRC_DIR"
sudo python3 jerhz-cli.py users sync

printf "<<< Done.\n\n"
