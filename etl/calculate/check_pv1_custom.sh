#encoding=utf8
#!/bin/bash

year=$1
month=$2
day=$3
hour=$4

prefix2="data2"
prefix3="data3"
prefix4="data4"

dash00="00"
dash15="15"
dash30="30"
dash45="45"

f1="/home/dingzheng/.inventory_${prefix2}_${year}${month}${day}${hour}${dash00}"
f2="/home/dingzheng/.inventory_${prefix2}_${year}${month}${day}${hour}${dash15}"
f3="/home/dingzheng/.inventory_${prefix2}_${year}${month}${day}${hour}${dash30}"
f4="/home/dingzheng/.inventory_${prefix2}_${year}${month}${day}${hour}${dash45}"

f5="/home/dingzheng/.inventory_${prefix3}_${year}${month}${day}${hour}${dash00}"
f6="/home/dingzheng/.inventory_${prefix3}_${year}${month}${day}${hour}${dash15}"
f7="/home/dingzheng/.inventory_${prefix3}_${year}${month}${day}${hour}${dash30}"
f8="/home/dingzheng/.inventory_${prefix3}_${year}${month}${day}${hour}${dash45}"

f9="/home/dingzheng/.inventory_${prefix4}_${year}${month}${day}${hour}${dash00}"
f10="/home/dingzheng/.inventory_${prefix4}_${year}${month}${day}${hour}${dash15}"
f11="/home/dingzheng/.inventory_${prefix4}_${year}${month}${day}${hour}${dash30}"
f12="/home/dingzheng/.inventory_${prefix4}_${year}${month}${day}${hour}${dash45}"

if [ ! -f ${f1} ];then
    exit
fi
echo "find ${f1}"
if [ ! -f ${f2} ];then
    exit
fi
echo "find ${f2}"
if [ ! -f ${f3} ];then
    exit
fi
echo "find ${f3}"
if [ ! -f ${f4} ];then
    exit
fi
echo "find ${f4}"
if [ ! -f ${f5} ];then
    exit
fi
echo "find ${f5}"
if [ ! -f ${f6} ];then
    exit
fi
echo "find ${f6}"
if [ ! -f ${f7} ];then
    exit
fi
echo "find ${f7}"
if [ ! -f ${f8} ];then
    exit
fi
echo "find ${f8}"
if [ ! -f ${f9} ];then
    exit
fi
echo "find ${f9}"
if [ ! -f ${f10} ];then
    exit
fi
echo "find ${f10}"
if [ ! -f ${f11} ];then
    exit
fi
echo "find ${f11}"
if [ ! -f ${f12} ];then
    exit
fi
echo "find ${f12}"

cd /home/dingzheng/amble/etl/

r1="/data6/inventory/${year}/${month}/${day}/inventory_${prefix2}_${year}${month}${day}${hour}${dash00}.pv1"
r2="/data6/inventory/${year}/${month}/${day}/inventory_${prefix2}_${year}${month}${day}${hour}${dash15}.pv1"
r3="/data6/inventory/${year}/${month}/${day}/inventory_${prefix2}_${year}${month}${day}${hour}${dash30}.pv1"
r4="/data6/inventory/${year}/${month}/${day}/inventory_${prefix2}_${year}${month}${day}${hour}${dash45}.pv1"
r5="/data6/inventory/${year}/${month}/${day}/inventory_${prefix3}_${year}${month}${day}${hour}${dash00}.pv1"
r6="/data6/inventory/${year}/${month}/${day}/inventory_${prefix3}_${year}${month}${day}${hour}${dash15}.pv1"
r7="/data6/inventory/${year}/${month}/${day}/inventory_${prefix3}_${year}${month}${day}${hour}${dash30}.pv1"
r8="/data6/inventory/${year}/${month}/${day}/inventory_${prefix3}_${year}${month}${day}${hour}${dash45}.pv1"
r9="/data6/inventory/${year}/${month}/${day}/inventory_${prefix4}_${year}${month}${day}${hour}${dash00}.pv1"
r10="/data6/inventory/${year}/${month}/${day}/inventory_${prefix4}_${year}${month}${day}${hour}${dash15}.pv1"
r11="/data6/inventory/${year}/${month}/${day}/inventory_${prefix4}_${year}${month}${day}${hour}${dash30}.pv1"
r12="/data6/inventory/${year}/${month}/${day}/inventory_${prefix4}_${year}${month}${day}${hour}${dash45}.pv1"

python merge_crontab.py ${f1},${f2},${f3},${f4},${f5},${f6},${f7},${f8},${f9},${f10},${f11},${f12}  ${r1},${r2},${r3},${r4},${r5},${r6},${r7},${r8},${r9},${r10},${r11},${r12}  /data6/inventory/${year}/${month}/${day}/inventory_pv1_${hour}.csv

r1="/data6/inventory/${year}/${month}/${day}/inventory_${prefix2}_${year}${month}${day}${hour}${dash00}.display_sale"
r2="/data6/inventory/${year}/${month}/${day}/inventory_${prefix2}_${year}${month}${day}${hour}${dash15}.display_sale"
r3="/data6/inventory/${year}/${month}/${day}/inventory_${prefix2}_${year}${month}${day}${hour}${dash30}.display_sale"
r4="/data6/inventory/${year}/${month}/${day}/inventory_${prefix2}_${year}${month}${day}${hour}${dash45}.display_sale"
r5="/data6/inventory/${year}/${month}/${day}/inventory_${prefix3}_${year}${month}${day}${hour}${dash00}.display_sale"
r6="/data6/inventory/${year}/${month}/${day}/inventory_${prefix3}_${year}${month}${day}${hour}${dash15}.display_sale"
r7="/data6/inventory/${year}/${month}/${day}/inventory_${prefix3}_${year}${month}${day}${hour}${dash30}.display_sale"
r8="/data6/inventory/${year}/${month}/${day}/inventory_${prefix3}_${year}${month}${day}${hour}${dash45}.display_sale"
r9="/data6/inventory/${year}/${month}/${day}/inventory_${prefix4}_${year}${month}${day}${hour}${dash00}.display_sale"
r10="/data6/inventory/${year}/${month}/${day}/inventory_${prefix4}_${year}${month}${day}${hour}${dash15}.display_sale"
r11="/data6/inventory/${year}/${month}/${day}/inventory_${prefix4}_${year}${month}${day}${hour}${dash30}.display_sale"
r12="/data6/inventory/${year}/${month}/${day}/inventory_${prefix4}_${year}${month}${day}${hour}${dash45}.display_sale"

python merge_crontab.py ${f1},${f2},${f3},${f4},${f5},${f6},${f7},${f8},${f9},${f10},${f11},${f12}  ${r1},${r2},${r3},${r4},${r5},${r6},${r7},${r8},${r9},${r10},${r11},${r12}  /data6/inventory/${year}/${month}/${day}/inventory_display_sale_${hour}.csv
