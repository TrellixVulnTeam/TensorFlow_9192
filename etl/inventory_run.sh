#!/bin/bash
#yyyy-MM-DD:HH
$date=$1
echo "python inventory_app.py inventory h ${date}"
python inventory_app.py inventory h "${date}"
if [ $? -eq 255 ];then
    echo "ad inventory hour run error"
    sh send_mail.sh ${date} ad app hour run error
    exit
fi
if [ "${hour}" == "02" ];then
    python inventory_app.py inventory 'd'
    if [ $? -eq 255 ];then
        echo "ad inventory day run error"
        sh send_mail.sh ${date} ad app day run error
        exit
    fi
fi