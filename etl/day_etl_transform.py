#-*- coding: utf-8 -*-
'''
Created on 2015年9月10日

@author: jyb
'''
import petl as etl
from petl import fromcsv
import datetime
import csv
import types
import sys
from data2postgresql import load
import yaml
Config=yaml.load(file("config.yml"))
from etl_transform import ETL_Transform

def etl_by_hour(day,hour,version):
    d = datetime.datetime.strptime(day,"%Y%m%d")
    yearmonth = datetime.datetime.strftime(d,"%Y%m")
    yearmonthday = datetime.datetime.strftime(d,"%Y%m%d")
    if version == 'old':
        supply_filePath = Config["old_version"]["supply_csv_file_path"]+"{0}/{1}.{2}.product.supply.csv".format(yearmonth,yearmonthday,hour)
        demand_filePath = Config["old_version"]["demand_csv_file_path"]+"{0}/{1}.{2}.product.demand.csv".format(yearmonth,yearmonthday,hour)
        supply_head=Config["old_version"]["supply"]["raw_header"]
        demand_head=Config["old_version"]["demand"]["raw_header"]
        agg_head=Config["old_version"]["supply"]["agg_hour_header"]
    else:
        supply_filePath = Config["supply_csv_file_path"]+"{0}/{1}.{2}.product.supply.csv".format(yearmonth,yearmonthday,hour)
        demand_filePath = Config["demand_csv_file_path"]+"{0}/{1}.{2}.product.demand.csv".format(yearmonth,yearmonthday,hour)
        supply_head=Config["supply"]["raw_header"]
        demand_head=Config["demand"]["raw_header"]
        agg_head=Config["supply"]["agg_hour_header"]
    print supply_filePath
    etls = ETL_Transform(
                        supply_header=supply_head,
                        demand_header=demand_head,
                        aggre_header=agg_head,
                        supply_csv_filePath=supply_filePath,
                        demand_csv_filePath=demand_filePath,
                        batch_read_size=Config["petl"]["batch_read_size"],
                        pdate=day,
                        hour=hour)
    etls.transform()
    
def load_to_pg(day,version):
        load('day',day,Config["db_table"]["Ad_Facts_By_Day"]["table_name"],version,'')
        load('day',day,Config["db_table"]["Hit_Facts_By_Day"]["table_name"],version,'')
        load('day',day,Config["db_table"]["Reqs_Facts_By_Day"]["table_name"],version,'')
def day_etl_agg_hour(day,version):
    tmp_ad_facts_result_table=[]
    tmp_hit_facts_result_table=[]
    tmp_reqs_facts_result_table=[]
    d=datetime.datetime.strptime(day,"%Y%m%d")
    yearmonth=datetime.datetime.strftime(d,"%Y%m")
    pdate_=datetime.datetime.strftime(d,"%Y_%m_%d")
    if version == 'old':
        hour_facts_file_path=Config["old_version"]["day_hour_facts_file_path"]
        day_facts_file_path=Config["old_version"]["day_facts_file_path"]
    else:
        hour_facts_file_path=Config["hour_facts_file_path"]
        day_facts_file_path=Config["day_facts_file_path"]
    #合并24小时
    for hour in range(24):
        str_hour=''
        if hour < 10:
            str_hour='0'+str(hour)
        else:
            str_hour=str(hour)
            
        print hour_facts_file_path+"{0}/{1}_{2}_ad_facts_by_hour.csv".format(yearmonth,pdate_,str_hour)
        hour_ad_facts_table = etl.fromcsv(hour_facts_file_path+"{0}/{1}_{2}_ad_facts_by_hour.csv".format(yearmonth,pdate_,str_hour),"utf-8")
        header=hour_ad_facts_table.list()[0]
        if tmp_ad_facts_result_table:
            tmp_ad_facts_result_table = etl.merge(tmp_ad_facts_result_table,hour_ad_facts_table,key=header)
        else:
            tmp_ad_facts_result_table=hour_ad_facts_table
        
        hour_hit_facts_table = etl.fromcsv(hour_facts_file_path+"{0}/{1}_{2}_hit_facts_by_hour.csv".format(yearmonth,pdate_,str_hour),"utf-8")
        header=hour_hit_facts_table.list()[0]
        if tmp_hit_facts_result_table:
            tmp_hit_facts_result_table = etl.merge(tmp_hit_facts_result_table,hour_hit_facts_table,key=header)
        else:
            tmp_hit_facts_result_table=hour_hit_facts_table
        
        hour_reqs_facts_table = etl.fromcsv(hour_facts_file_path+"{0}/{1}_{2}_reqs_facts_by_hour.csv".format(yearmonth,pdate_,str_hour),"utf-8")
        header=hour_reqs_facts_table.list()[0]
        if tmp_reqs_facts_result_table:
            tmp_reqs_facts_result_table = etl.merge(tmp_reqs_facts_result_table,hour_reqs_facts_table,key=header)
        else:
            tmp_reqs_facts_result_table=hour_reqs_facts_table
    #聚合24小时数据
    day_hit_facts_table=aggre_hit_facts(tmp_hit_facts_result_table,version)
    day_reqs_facts_table=aggre_reqs_facts(tmp_reqs_facts_result_table,version)
    day_ad_facts_table=aggre_ad_facts(tmp_ad_facts_result_table,version)
    
    etl.tocsv(day_hit_facts_table, day_facts_file_path+"{0}/{1}_hit_facts_by_day.csv".format(yearmonth,pdate_), encoding="utf-8",write_header=True)
    etl.tocsv(day_reqs_facts_table, day_facts_file_path+"{0}/{1}_reqs_facts_by_day.csv".format(yearmonth,pdate_), encoding="utf-8",write_header=True)
    etl.tocsv(day_ad_facts_table, day_facts_file_path+"{0}/{1}_ad_facts_by_day.csv".format(yearmonth,pdate_), encoding="utf-8",write_header=True)        
    
def aggre_hit_facts(table,version):
    if version == 'old':
        agg_header=Config["old_version"]["supply"]["agg_day_header"][:]
    else:
        agg_header=Config["supply"]["agg_day_header"][:]
    agg_header.append("date_id")
    table=etl.convert(table,'total',int)
    agg_table_ = etl.aggregate(table,tuple(agg_header),sum,'total')
    ren_table = etl.rename(agg_table_,'value','total')
    return ren_table
def aggre_reqs_facts(table,version):
    if version == 'old':
        agg_header=Config["old_version"]["supply"]["reqs_day_header"][:]
    else:
        agg_header=Config["supply"]["reqs_day_header"][:]
    agg_header.append("date_id")
    table=etl.convert(table,'total',int)
    agg_table_ = etl.aggregate(table,tuple(agg_header),sum,'total')
    ren_table = etl.rename(agg_table_,'value','total')
    return ren_table
def aggre_ad_facts(table,version):
    if version == 'old':
        agg_header=Config["old_version"]["supply"]["agg_day_header"][:]
    else:
        agg_header=Config["supply"]["agg_day_header"][:]
    agg_header.append("date_id")
    ad_header=agg_header[:]
    ad_header.append("impressions_start_total")
    ad_header.append("impressions_finish_total")
    ad_header.append("click")
    table=etl.convert(table,('impressions_start_total','impressions_finish_total','click'),int)
    agg_table_ = etl.rowreduce(table,key=tuple(agg_header),reducer=sum_ad_facts_reducer,header=ad_header)
    return agg_table_
def sum_ad_facts_reducer(key,rows):
    sum_imps_start=0
    sum_imps_end=0
    sum_click=0
    for row in rows:
        sum_imps_start +=row['impressions_start_total']
        sum_imps_end +=row['impressions_finish_total']
        sum_click +=row['click']
    result=list(key)
    result.append(sum_imps_start)
    result.append(sum_imps_end)
    result.append(sum_click)
    return result
def day_etl(day,type_t,version):
    if type_t == "reload":
        for hour in range(24):
            str_hour=''
            if hour < 10:
                str_hour='0'+str(hour)
            else:
                str_hour=str(hour)
            etl_by_hour(day, str_hour,version)
    elif type_t == 'merge':
        pass
    try:
        day_etl_agg_hour(day,version)
        load_to_pg(day,version)
    except Exception,e:
        print "ERROR:day_etl_transform",day,e
if __name__ == "__main__":
    day=sys.argv[1]
    type_t=sys.argv[2] #reload merge
    version=sys.argv[3] #old new
    day_etl(day, type_t, version)