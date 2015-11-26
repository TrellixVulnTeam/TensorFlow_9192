# encoding:utf-8
import sys
import os
import time
from datetime import datetime
from datetime import timedelta

if 'amble' not in sys.modules and __name__ == '__main__':
    import pythonpathsetter
from etl.app import AdMonitorRunner
from etl.conf.settings import LOGGER, Config
from etl.util import path_chk_or_create
from etl.util.inventory_datautil import merge_file
from etl.logic1.ad_calculate_inventory import AdInventoryTranform
from etl.logic1.ad_transform_pandas import buddha_bless_me

from etl.report.reporter import DataReader
from etl.report.reporter import Reportor

METRICS = ["display", "display_poss"]
M_Dir = "{prefix}{sep}{year}{sep}{month}{sep}{day}{sep}{hour}"
H_Dir = "{prefix}{sep}{year}{sep}{month}{sep}{day}"
D_Dir = "{prefix}{sep}{year}{sep}{month}"
M_Logic1_Filename = "result_{metric}_ad_{minute:02d}.csv"
H_Logic1_Filename = "result_{metric}_ad_{hour:02d}.csv"
D_Logic1_Filename = "result_{metric}_ad_{day:02d}.csv"

data_prefix = Config["data_prefix"]
data_output_prefix = os.path.join(data_prefix, "inventory")

class InventoryAdMonitorRunner(AdMonitorRunner):

    def concat_output_path(self, path, num, minute):
        output_paths = {}
        for metric in METRICS:
            filename = "logic{num}_{metric}_ad_{minute:02d}.csv".format(
                    num=num,
                    metric=metric,
                    minute=minute)

            tmp_path = os.path.join(path, filename)
            output_paths.update({ metric: tmp_path})

        return output_paths
    def _job_ready_by_hour(self, now):
        '''计算当前小时'''
        paths = {}

        ad_src_path = "{prefix}{sep}{year}{sep}{month}{sep}{day}".format(
                prefix=data_prefix,
                year=now.year,
                month=now.month,
                day=now.day,
                sep=os.sep
            )
        path_chk_or_create(ad_src_path)
        ad_src_filename = "src_ad_{hour:02d}.csv".format(hour=now.hour)


        paths.update({
            'ad_src_path': ad_src_path,
            'ad_src_filename': ad_src_filename
            })

        ad_output_path = "{prefix}{sep}{year}{sep}{month}{sep}{day}".format(
                prefix=data_output_prefix,
                year=now.year,
                month=now.month,
                day=now.day,
                sep=os.sep
            )
        # ## logic1 path
        output_paths = self.concat_output_path(ad_output_path, 1, now.hour)

        paths.update({
            'logic1_output_paths': output_paths
            })

        result_dir = "{prefix}{sep}{year}{sep}{month}{sep}{day}".format(
                prefix=data_output_prefix,
                year=now.year,
                month=now.month,
                day=now.day,
                sep=os.sep
            )
        path_chk_or_create(result_dir)
        result_filename = H_Logic1_Filename.format(metric="inventory",hour=now.hour)
        paths.update({
            'result_filepath': os.path.join(result_dir, result_filename)
        })

        return paths

    def _job_ready_by_day(self, now):
        output_path = D_Dir.format(prefix=data_output_prefix,
                                year=now.year,
                                sep=os.sep,
                                month=now.month)

        src_path = H_Dir.format(prefix=data_output_prefix,
                                year=now.year,
                                sep=os.sep,
                                month=now.month,
                                day=now.day)

        paths = {}
        logic1_src_paths = {}
        logic1_output_paths = {}

        paths1 = []
        output_filename1 = D_Logic1_Filename.format(metric="inventory", day=now.day)

        for i in xrange(0, 24, Config["d_delay"]):
            filename1 = H_Logic1_Filename.format(hour=i, metric="inventory")
            paths1.append(os.path.join(src_path, filename1))

        logic1_src_paths.update({"inventory": paths1})

        logic1_output_paths.update({"inventory": os.path.join(output_path, output_filename1)})

        paths.update({
            'logic1_src_paths': logic1_src_paths,
            'logic1_output_paths': logic1_output_paths
            })
        return paths


    def run(self, now, mode='h'):
        """
        mode in minute, hour, day
        """

        LOGGER.info("begin running etl job")

        assert type(now) == datetime
        assert mode in ['h', 'd']

        if mode == 'h':
            paths = self._job_ready_by_hour(now)

            LOGGER.info("Job hour paths: \r\n \
                    ad_src_path: %s \r\n \
                    ad_src_filename: %s \r\n \
                    logic1_output_paths: %s \r\n \
                    result_filepath: %s \r\n ",
                        paths['ad_src_path'],
                        paths['ad_src_filename'],
                        paths['logic1_output_paths'],
                        paths['result_filepath'])

            # ad_src_path = os.path.join(paths["ad_src_path"], paths["ad_src_filename"])

            start = time.clock()
            # logic1 code
            result_filepath = paths["result_filepath"]
            ait = AdInventoryTranform(result_filepath)
            ait.calculate(
                    paths['ad_src_path'],
                    paths['ad_src_filename'],
                    paths['logic1_output_paths'])
            end = time.clock()
            logic1_sptime = '%0.2f' % (end - start)
            LOGGER.info("logic1 calc spent: %s s" , logic1_sptime)
            '''
            # 读取计算结果
            d_reader = DataReader().hour_data(None, \
                                    paths['logic1_output_paths'])
            # 报告结果
            filesize = getfilesize(ad_src_path)
            params = {
                      "type":"hour",
                      "filename":paths["ad_src_filename"],
                      "filesize":filesize,
                      "logic1_sptime":logic1_sptime,
                      "start_time":now.strftime("%Y-%m-%d %H")}
            Reportor(params, d_reader).report_text()
            '''

        elif mode == 'd':
            paths = self._job_ready_by_day(now)

            LOGGER.info("Job hour paths: \r\n \
                    logic1_src_paths: %s \r\n \
                    logic1_output_path: %s \r\n \
                    " % (paths['logic1_src_paths'],
                        paths['logic1_output_paths']))

            start = time.clock()
            # logic1 code
            merge_file(paths['logic1_src_paths'], paths['logic1_output_paths'])
            end = time.clock()
            #sptime = '%0.2f' % (end - start)
            LOGGER.info("merge file spend: %f s" % (end - start))
            '''
            # 读取计算结果
            d_reader = DataReader().hour_data(None, \
                                    paths['logic1_output_paths'])

            params = {
                      "type":"day",
                      "fileinfo0":None,
                      "fileinfo1":getfilesinfo(paths['logic1_output_paths']),
                      "sptime":sptime,
                      "start_time":now.strftime("%Y-%m-%d")}
            # 报告结果
            Reportor(params, d_reader).report_text()
            '''

def getfilesize(filepath):
    psize = os.path.getsize(filepath)
    filesize = '%0.3f' % (psize / 1024.0 / 1024.0)
    return str(filesize) + "MB"

def getfilesinfo(filepaths):
    info = {}
    for key, filepath in filepaths.iteritems():
        filesize = getfilesize(filepath)
        filename = os.path.split(filepath)[1]
        info[key] = (filesize, filename)
    return info

def run_cli(arguments):
    try:
        run_type = arguments[1]
        args = arguments[2:]
        now = datetime.now()
        if run_type == 'admonitor':
            if 'h' == args[0]:
                now = now - timedelta(hours=1)
            elif 'd' == args[0]:
                now = now - timedelta(days=1)
            AdMonitorRunner().run(now, args[0])
        elif run_type == 'inventory':
            if 'h' == args[0]:
                now = now - timedelta(hours=1)
            elif 'd' == args[0]:
                now = now - timedelta(days=1)
            InventoryAdMonitorRunner().run(now, args[0])
        else:
            LOGGER.error("app run_type [{0}] is wrong".format(run_type))
            sys.exit(-1)
    except Exception, e:
        import traceback
        print traceback.format_exc()
        LOGGER.error("run app error,error message:" + str(e))
        sys.exit(-1)


if __name__ == '__main__':
    '''
    args: python app.py ad_monitor m|h|d
    '''
    buddha_bless_me()
    run_cli(sys.argv)

