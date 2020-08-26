# -*- coding:utf-8 -*-

"""
SQLite don't support function: REGEXP. So must use python to do regexp.
"""

import os
from pathlib import Path
import sqlite3
import re
import threading
import numpy as np
import time
import sys
from io import StringIO

import mdfreader

from .. import constant
from ..exception import OpenMdfError, OpenDbError


def transformCoordinate():
    """
    transform the coordinate from the channels in table: RADAR_TRACKER_TABLE_NAMES[2].
    """
    if len(constant.DB_FILES) != 0:
        db_pth = constant.DB_FILES[0]
        try:
            conn = sqlite3.connect(db_pth)
        except Exception:
            print('Error in fun: data_process->transformCoordinate, connect db_pth error')
            return False
        else:
            curs = conn.cursor()

            # get the veh-static data
            str1 = 'SELECT Value FROM'
            str2 = constant.VEH_STATIC_TABLE_NAMES[0]
            str3 = 'ORDER BY no'
            sql = ' '.join((str1, str2, str3))
            curs.execute(sql)
            result = curs.fetchall()
            veh_length = result[0][0]
            # veh_width = result[1][0]
            rm_pos_x = result[2][0]
            rm_pos_y = result[3][0]
            rs_pos_x = result[4][0]
            rs_pos_y = result[5][0]

            # get the ch which need to transform coordinate
            str1 = 'SELECT no, Channel_Name FROM'
            str2 = constant.MASTER_TABLE_NAMES[1]
            str3 = 'ORDER BY no'
            sql = ' '.join((str1, str2, str3))
            curs.execute(sql)
            result = curs.fetchall()

            coord_transform_dir = {'posY_m': {}}

            def getDatanoFromChno(ch_no_tuple):
                str1 = 'SELECT data_no FROM channel_data_no_resample WHERE ch_no IN'
                str2 = f'{ch_no_tuple}'
                sql = ' '.join((str1, str2))
                curs.execute(sql)
                data_no_result = curs.fetchall()
                data_no_tuple = tuple([i[0] for i in data_no_result])
                return data_no_tuple

            sql = 'SELECT ch_no FROM tracker_attr WHERE Attr_ID <3'
            curs.execute(sql)
            result = curs.fetchall()
            ch_no_tuple = tuple([i[0] for i in result])
            coord_transform_dir['posX_m'] = getDatanoFromChno(ch_no_tuple)

            sql = """SELECT ch_no 
                    FROM tracker_attr AS tat, radar_tracker as rt 
                    WHERE
                    Radar_ID = 0 AND rt.tracker_no=tat.tracker_no AND Attr_ID IN (3, 4, 5)"""
            curs.execute(sql)
            result = curs.fetchall()
            ch_no_tuple = tuple([i[0] for i in result])
            coord_transform_dir['posY_m']['RM'] = getDatanoFromChno(ch_no_tuple)

            sql = """SELECT ch_no 
                    FROM tracker_attr AS tat, radar_tracker as rt 
                    WHERE
                    Radar_ID = 1 AND rt.tracker_no=tat.tracker_no AND Attr_ID IN (3, 4, 5)"""
            curs.execute(sql)
            result = curs.fetchall()
            ch_no_tuple = tuple([i[0] for i in result])
            coord_transform_dir['posY_m']['RS'] = getDatanoFromChno(ch_no_tuple)

            tmp_list = [coord_transform_dir['posX_m'],
                        coord_transform_dir['posY_m']['RM'],
                        coord_transform_dir['posY_m']['RS']]

            posX_value = veh_length + rm_pos_x
            posY_rm = rm_pos_y
            posY_rs = rs_pos_y
            transformed_value = [posX_value, posY_rm, posY_rs]

            str1 = 'UPDATE data_no_resample AS a'
            str2 = 'SET Value_after_CoordTransform = Value_after_CoordTransform + ?'
            str3 = 'WHERE a.no = ?'
            sql = ' '.join((str1, str2, str3))
            for i, tmp_tuple in zip(transformed_value, tmp_list):
                temp_list = []
                for j in tmp_tuple:
                    temp_list.append((i, j))
                try:
                    curs.executemany(sql, temp_list)
                except:
                    print('error in data_process->transformCoordinate: update value to list')
                    conn.rollback()
                else:
                    conn.commit()

            conn.close()
            return True
    else:
        print('Error in data_process->transformCoordinate, no db-pth')
        return False


def createVehStaticTable():
    db_pth = constant.DB_FILES[0]
    try:
        conn = sqlite3.connect(db_pth)
    except Exception:
        print('open db in fun: data_process->organizeData Error')
        return False
    else:
        curs = conn.cursor()

        # get all the channels
        str1 = 'SELECT no, Channel_Name FROM'
        str2 = constant.MASTER_TABLE_NAMES[1]
        str3 = 'ORDER BY no'
        sql = ' '.join((str1, str2, str3))
        curs.execute(sql)
        result = curs.fetchall()

        re_result = ([], [], [], [], [], [])
        prog0 = re.compile('\.VehStaticRM\.vehLength_m')
        prog1 = re.compile('\.VehStaticRM\.vehWidth_m')
        prog2 = re.compile('\.VehStaticRM\.sengeo\.xpos')
        prog3 = re.compile('\.VehStaticRM\.sengeo\.ypos')
        prog4 = re.compile('\.VehStaticRS\.sengeo\.xpos')
        prog5 = re.compile('\.VehStaticRS\.sengeo\.ypos')
        prog = (prog0, prog1, prog2, prog3, prog4, prog5)

        def getVehStaticInfo(count_):
            conn = sqlite3.connect(db_pth)
            curs = conn.cursor()
            for row in result:
                ch_no, ch_name = row
                m = re.search(prog[count_], ch_name)
                if m is not None:
                    sql = """ SELECT Value FROM
                            data_no_resample AS a, channel_data_no_resample AS b
                            WHERE 
                            ch_no = ? AND a.no = b.data_no AND a.TimeStamp_ID = 0
                        """
                    curs.execute(sql, (ch_no,))
                    output = curs.fetchall()
                    output = output[0][0]
                    re_result[count_].append(output)

        thread_list = []
        for count in range(len(prog)):
            t = threading.Thread(target=getVehStaticInfo, args=(count,))
            thread_list.append(t)

        for t in thread_list:
            t.start()

        for t in thread_list:
            t.join()

        for index, data in enumerate(re_result):
            # true means null-list
            if len(data) == 0:
                # veh_length
                if index == 0:
                    re_result[index].append(5.032)
                # veh_width
                elif index == 1:
                    re_result[index].append(1.875)
                # rm-pos-x
                elif index == 2:
                    re_result[index].append(-0.3)
                # rm-pos-y
                elif index == 3:
                    re_result[index].append(0.7)
                # rs-pos-x
                elif index == 4:
                    re_result[index].append(-0.3)
                # rs-pos-x
                elif index == 5:
                    re_result[index].append(-0.7)
                else:
                    print('Error in set veh-static-value')

        veh_static = []
        re_name = ['Length', 'Width', 'RM_X_pos', 'RM_Y_pos', 'RS_X_pos', 'RS_Y_pos']
        for i, info in enumerate(zip(re_name, re_result)):
            name, data = info
            veh_static.append((i, name, data[0]))

        # store in table
        str1 = 'CREATE TABLE'
        str2 = constant.VEH_STATIC_TABLE_NAMES[0]
        str3 = """(
                        no INT(4) PRIMARY KEY,
                        Name VARCHAR(32),
                        Value DOUBLE
                    )"""
        sql = ' '.join((str1, str2, str3))
        curs.execute(sql)

        str1 = 'INSERT INTO'
        str2 = constant.VEH_STATIC_TABLE_NAMES[0]
        str3 = 'VALUES (?,?,?)'
        sql = ' '.join((str1, str2, str3))
        try:
            curs.executemany(sql, veh_static)
        except Exception:
            print('insert value to table: veh_static error')
            conn.rollback()
            conn.close()
            return False
        else:
            conn.commit()
            conn.close()
            return True


def organizeData():
    if len(constant.PROCESSED_MF4_FILES) != 0:
        file_pth = constant.PROCESSED_MF4_FILES[0]
        try:
            mdf = mdfreader.Mdf(file_pth)
        except OpenMdfError as X:
            print(X)
        else:
            db_pth = constant.DB_FILES[0]
            try:
                conn = sqlite3.connect(db_pth)
            except Exception:
                print('open db in fun: data_process->organizeData Error')
                return False
            else:
                curs = conn.cursor()

                # get all the channels
                str1 = 'SELECT no, Channel_Name FROM'
                str2 = constant.MASTER_TABLE_NAMES[1]
                str3 = 'ORDER BY no'
                sql = ' '.join((str1, str2, str3))
                curs.execute(sql)
                result = curs.fetchall()

                data_no_resample_list = []
                ch_data_no_resample_list = []
                data_no_count = 0
                for row in result:
                    ch_no, ch_name = row

                    info = mdf.get_channel(ch_name)
                    ch_data = info['data']
                    ch_data = ch_data.astype(np.float64)
                    ch_unit = info['unit']

                    ts_len = len(ch_data)
                    ts_id = list(range(ts_len))
                    data_no = [i + data_no_count for i in ts_id]

                    for no, ts, value in zip(data_no, ts_id, ch_data):
                        data_no_resample_list.append((no, ts, value, value, ch_unit))
                        ch_data_no_resample_list.append((ch_no, no))

                    data_no_count += ts_len

                #################################################  data_no_resample
                str1 = 'CREATE TABLE'
                str2 = constant.MASTER_TABLE_NAMES[5]
                str3 = """(
                            no INT PRIMARY KEY,
                            TimeStamp_ID INT NOT NULL,
                            Value DOUBLE,
                            Value_after_CoordTransform DOUBLE,
                            Unit VARCHAR(16)
                        )"""
                sql = ' '.join((str1, str2, str3))
                curs.execute(sql)

                str1 = 'INSERT INTO'
                str2 = constant.MASTER_TABLE_NAMES[5]
                str3 = 'VALUES (?,?,?,?,?)'
                sql = ' '.join((str1, str2, str3))
                try:
                    curs.executemany(sql, data_no_resample_list)
                except Exception:
                    conn.rollback()
                else:
                    conn.commit()

                #################################################  channel-data_no_resample
                str1 = 'CREATE TABLE'
                str2 = constant.MASTER_TABLE_NAMES[6]
                str3 = """(
                            ch_no INT,
                            data_no INT
                        )"""
                sql = ' '.join((str1, str2, str3))
                curs.execute(sql)

                str1 = 'INSERT INTO'
                str2 = constant.MASTER_TABLE_NAMES[6]
                str3 = 'VALUES (?,?)'
                sql = ' '.join((str1, str2, str3))
                try:
                    curs.executemany(sql, ch_data_no_resample_list)
                except Exception:
                    conn.rollback()
                else:
                    conn.commit()

                # data-after-resample not define yet
                # data_after_sample_list = []
                #                #################################################  data_after_resample
                #                str2 = constant.MASTER_TABLE_NAMES[7]
                #                str3 = """(
                #                                            data_no INT PRIMARY KEY,
                #                                            TimeStamp_ID INT NOT NULL,
                #                                            Value DOUBLE,
                #                                            Value_after_CoordTransform DOUBLE,
                #                                            Unit VARCHAR(16)
                #                                        )"""
                #                sql = ' '.join((str1, str2, str3))
                #                curs.execute(sql)
                #
                #                #################################################  channel-data_no_resample
                #                str2 = constant.MASTER_TABLE_NAMES[8]
                #                str3 = """(
                #                                            ch_no INT,
                #                                            data_no INT
                #                                        )"""
                #                sql = ' '.join((str1, str2, str3))
                #                curs.execute(sql)

                # get the vehicle static data
                status = createVehStaticTable()

                if status:
                    # begin to transform coordinate
                    transformCoordinate()

                conn.close()
                return True
    else:
        print('Error in fun:data_process->organizeData, no MF4-file path')
        return False


def extractObjlist():
    if len(constant.DB_FILES) != 0:
        db_pth = constant.DB_FILES[0]
        try:
            conn = sqlite3.connect(db_pth)
        except Exception:
            print('Error in fun: data_process->extractObjlist, connect db_pth error')
            return False
        else:
            curs = conn.cursor()

            # get the veh-static data
            str1 = 'SELECT no, Channel_Name FROM'
            str2 = constant.MASTER_TABLE_NAMES[1]
            sql = ' '.join((str1, str2))
            curs.execute(sql)
            result = curs.fetchall()

            radar_list = constant.RADAR
            tracker_list = []
            rm_tracker_set = set()
            rs_tracker_set = set()
            radar_tracker_list = []

            ATTR_TUPLE = constant.TRACKER_ATTR
            attr_list = []
            for i, attr in enumerate(ATTR_TUPLE):
                attr_list.append((i, attr))

            tracker_attr_list = []

            tracker_no_count = 0
            for row in result:
                ch_no, ch_name = row
                info = ch_name.split('.')
                if len(info) >=5 :
                    filter_obj = info[1][:7]

                    if filter_obj == 'ObjList':
                        filter_radar = info[1][-2:]
                        if info[2] == 'track':
                            filter_tracker_id = int(info[3][1:-1])
                            tracker_no = tracker_no_count
                            if filter_radar == 'RM':
                                if filter_tracker_id in rm_tracker_set:
                                    pass
                                else:
                                    rm_tracker_set.add(filter_tracker_id)
                                    radar_tracker_list.append((0, tracker_no))
                                    tracker_list.append((tracker_no, filter_tracker_id))
                                    tracker_no_count += 1
                            elif filter_radar == 'RS':
                                if filter_tracker_id in rs_tracker_set:
                                    pass
                                else:
                                    rs_tracker_set.add(filter_tracker_id)
                                    radar_tracker_list.append((1, tracker_no))
                                    tracker_list.append((tracker_no, filter_tracker_id))
                                    tracker_no_count += 1

                            tracker_no = tracker_no_count - 1
                            filter_attr = '.'.join(info[4:])
                            if filter_attr in ATTR_TUPLE:
                                attr_id = ATTR_TUPLE.index(filter_attr)
                                tracker_attr_list.append((tracker_no, attr_id, ch_no))

            ############################################ radar
            str1 = 'CREATE TABLE'
            str2 = constant.OBJLIST_TABLE_NAMES[0]
            str3 = """(
                        Radar_ID INT(4) PRIMARY KEY,
                        Radar_Name VARCHAR(8)
                    )"""
            sql = ' '.join((str1, str2, str3))
            curs.executescript(sql)

            str1 = 'INSERT INTO'
            str2 = constant.OBJLIST_TABLE_NAMES[0]
            str3 = 'VALUES (?,?)'
            sql = ' '.join((str1, str2, str3))
            try:
                curs.executemany(sql, radar_list)
            except Exception:
                conn.rollback()
            else:
                conn.commit()

            ############################################ tracker
            str1 = 'CREATE TABLE'
            str2 = constant.OBJLIST_TABLE_NAMES[1]
            str3 = """(
                        no INT(4) PRIMARY KEY,
                        Tracker_ID VARCHAR(8)
                    )"""
            sql = ' '.join((str1, str2, str3))
            curs.executescript(sql)

            str1 = 'INSERT INTO'
            str2 = constant.OBJLIST_TABLE_NAMES[1]
            str3 = 'VALUES (?,?)'
            sql = ' '.join((str1, str2, str3))
            try:
                curs.executemany(sql, tracker_list)
            except Exception:
                conn.rollback()
            else:
                conn.commit()

            ############################################ radar-tracker
            str1 = 'CREATE TABLE'
            str2 = constant.OBJLIST_TABLE_NAMES[2]
            str3 = """(
                        Radar_ID INT(4),
                        tracker_no INT(4)
                    )"""
            sql = ' '.join((str1, str2, str3))
            curs.executescript(sql)

            str1 = 'INSERT INTO'
            str2 = constant.OBJLIST_TABLE_NAMES[2]
            str3 = 'VALUES (?,?)'
            sql = ' '.join((str1, str2, str3))
            try:
                curs.executemany(sql, radar_tracker_list)
            except Exception:
                conn.rollback()
            else:
                conn.commit()

            ############################################ attr
            str1 = 'CREATE TABLE'
            str2 = constant.OBJLIST_TABLE_NAMES[3]
            str3 = """(
                        no INT,
                        Attribute_Name VARCHAR(128)
                    )"""
            sql = ' '.join((str1, str2, str3))
            curs.executescript(sql)

            str1 = 'INSERT INTO'
            str2 = constant.OBJLIST_TABLE_NAMES[3]
            str3 = 'VALUES (?,?)'
            sql = ' '.join((str1, str2, str3))
            try:
                curs.executemany(sql, attr_list)
            except Exception:
                conn.rollback()
            else:
                conn.commit()

            ############################################ tracker-attr
            str1 = 'CREATE TABLE'
            str2 = constant.OBJLIST_TABLE_NAMES[4]
            str3 = """(
                        tracker_no INT,
                        Attr_ID INT,
                        ch_no INT
                    )"""
            sql = ' '.join((str1, str2, str3))
            curs.executescript(sql)

            str1 = 'INSERT INTO'
            str2 = constant.OBJLIST_TABLE_NAMES[4]
            str3 = 'VALUES (?,?,?)'
            sql = ' '.join((str1, str2, str3))
            try:
                curs.executemany(sql, tracker_attr_list)
            except Exception:
                conn.rollback()
            else:
                conn.commit()

            curs.close()
            conn.close()
    else:
        print('Error in data_process->extractObjlist: no db-pth')


def parseMf4File(file_pth=None):
    """
    The main function to parse the input file_path
    :param file_pth: [srt] the MF4-file path
    :return parse_status: the parse state
    """

    # create db-store-path
    file_name = file_pth.stem
    current_parent_pth = Path(os.path.dirname(os.path.abspath(__file__)))
    db_pth = current_parent_pth.joinpath(f'{file_name}.db')

    # judge this file's database whether exists
    db_status = db_pth.exists()

    if not db_status:
        # create SQLite connect, cursor
        try:
            mdf = mdfreader.Mdf(file_pth)
        except OpenMdfError as X:
            print(X)
        else:
            # create memory db, after write to file
            conn = sqlite3.connect(":memory:")
            curs = conn.cursor()

            group_list = []
            channel_list = []
            group_channel_list = []
            ts_list = []
            group_ts_list = []

            

            channel_no_count = 0
            for group, channels in mdf.masterChannelList.items():
                info = mdf.get_channel(group)
                g_id = info['id'][0][0]
                g_name = info['id'][2][0]
                g_source = info['id'][2][1]
                g_path = info['id'][2][2]
                g_master_ch_name = info['master']
                g_master_ch_type = info['masterType']
                group_list.append((g_id, g_name, g_source, g_path, g_master_ch_name, g_master_ch_type))

                ts_no = g_id
                group_ts_list.append((g_id, ts_no))

                sample_period = 0
                sample_length = 0
                if 't_5_5' in channels:
                    ts_data = mdf.get_channel_data('t_5_5')
                    sample_length = len(ts_data)
                    ts_period = (ts_data[1] - ts_data[0]) * 1000
                    sample_period = int(round(ts_period))
                sample_unit = 'ms'
                ts_list.append((ts_no, sample_period, sample_unit, sample_length))

                for ch_no, channel in enumerate(channels):
                    ch_no += channel_no_count
                    info = mdf.get_channel(channel)
                    ch_id = info['id'][0][2]
                    ch_name = info['id'][1][0]
                    ch_source = info['id'][1][1]
                    ch_path = info['id'][1][2]
                    ch_unit = info['unit']
                    channel_list.append((ch_no, ch_id, ch_name, ch_unit, ch_source, ch_path))
                    group_channel_list.append((g_id, ch_no))
                channel_no_count += len(channels)




            #################################################  channel
            str1 = 'CREATE TABLE'
            str2 = constant.MASTER_TABLE_NAMES[1]
            str3 = """(
                        no INT PRIMARY KEY,
                        Channel_ID INT NOT NULL,
                        Channel_Name VARCHAR(128),
                        Ch_Data_Unit VARCHAR(16),
                        Channel_Source VARCHAR(32),
                        Channel_Path VARCHAR(32)
                    )"""
            sql = ' '.join((str1, str2, str3))
            curs.executescript(sql)

            str1 = 'INSERT INTO'
            str2 = constant.MASTER_TABLE_NAMES[1]
            str3 = 'VALUES (?,?,?,?,?,?)'
            sql = ' '.join((str1, str2, str3))
            try:
                curs.executemany(sql, channel_list)
            except Exception:
                conn.rollback()
                print('inserting data into db file failed~~~')
            #################################################  group
            str1 = 'CREATE TABLE'
            str2 = constant.MASTER_TABLE_NAMES[0]
            str3 = """(
                        Group_ID INT(8) PRIMARY KEY,
                        Group_Name VARCHAR(32), 
                        Group_Source VARCHAR(32),
                        Group_Path VARCHAR(32),
                        Master_Channel_Name VARCHAR(32), 
                        Master_Channel_Type VARCHAR(32)
                    )"""
            sql = ' '.join((str1, str2, str3))
            curs.executescript(sql)

            str1 = 'INSERT INTO'
            str2 = constant.MASTER_TABLE_NAMES[0]
            str3 = 'VALUES (?,?,?,?,?,?)'
            sql = ' '.join((str1, str2, str3))
            try:
                curs.executemany(sql, group_list)
            except Exception:
                conn.rollback()
                print('inserting data into db file failed~~~')
            #################################################  group-channel

            str1 = 'CREATE TABLE'
            str2 = constant.MASTER_TABLE_NAMES[2]
            str3 = """(
                        Group_ID INT(4) NOT NULL,
                        ch_no INT
                    )"""
            sql = ' '.join((str1, str2, str3))
            curs.executescript(sql)

            str1 = 'INSERT INTO'
            str2 = constant.MASTER_TABLE_NAMES[2]
            str3 = 'VALUES (?,?)'
            sql = ' '.join((str1, str2, str3))
            try:
                curs.executemany(sql, group_channel_list)
            except Exception:
                conn.rollback()
                print('inserting data into db file failed~~~')

            #################################################  timestamp

            str1 = 'CREATE TABLE'
            str2 = constant.MASTER_TABLE_NAMES[3]
            str3 = """(
                        no INT(4) PRIMARY KEY,
                        Sample_Period INT,
                        Sample_Unit VARCHAR(8),
                        Sample_Length INT
                    )"""
            sql = ' '.join((str1, str2, str3))
            curs.executescript(sql)

            str1 = 'INSERT INTO'
            str2 = constant.MASTER_TABLE_NAMES[3]
            str3 = 'VALUES (?,?,?,?)'
            sql = ' '.join((str1, str2, str3))
            try:
                curs.executemany(sql, ts_list)
            except Exception:
                conn.rollback()
                print('inserting data into db file failed~~~')

            #################################################  group_ts

            str1 = 'CREATE TABLE'
            str2 = constant.MASTER_TABLE_NAMES[4]
            str3 = """(
                        Group_ID INT(4),
                        ts_no INT(4)
                    )"""
            sql = ' '.join((str1, str2, str3))
            curs.executescript(sql)

            str1 = 'INSERT INTO'
            str2 = constant.MASTER_TABLE_NAMES[4]
            str3 = 'VALUES (?,?)'
            sql = ' '.join((str1, str2, str3))
            try:
                curs.executemany(sql, group_ts_list)
            except Exception:
                conn.rollback()
                print('inserting data into db file failed~~~')

            # generate mem-db script
            str_buffer = StringIO()
            # con.iterdump() dump all sqls
            for line in conn.iterdump():
                str_buffer.write('%s\n' % line)

            curs.close()
            conn.close()

            conn_file = sqlite3.connect(db_pth)
            curs_file = conn_file.cursor()
            curs_file.executescript(str_buffer.getvalue())
            curs_file.close()
            conn_file.close()

            constant.PROCESSED_MF4_FILES.append(str(file_pth))
            constant.DB_FILES.append(str(db_pth))

            # the fist means ok, the second means the data not processed
            return True, False

    else:
        constant.PROCESSED_MF4_FILES.append(str(file_pth))
        constant.DB_FILES.append(str(db_pth))
        print('db-file exist already,h')
        return True, True


def create_select_table(db_pth, checked_channel):
    try:
        conn = sqlite3.connect(db_pth)
        curs = conn.cursor()
    except Exception:
        print('create selected-ch-view error in btn-num-clicked')
        return False
    select_ch_info = []
    for ch in checked_channel:
        g_id, ch_id = ch

        sql = 'SELECT Group_ID, ch_no, Channel_ID, Channel_Name, Ch_Data_Unit ' \
              'FROM channels AS a, group_channel AS b ' \
              'WHERE a.no=b.ch_no AND Group_ID=? AND Channel_ID=?'
        curs.execute(sql, (g_id+1, ch_id))
        row = curs.fetchall()[0]
        select_ch_info.append(row)

    sql = """CREATE TABLE IF NOT EXISTS checked_ch_info(
            Group_ID INT(4) NOT NULL,
            ch_no INT NOT NULL,
            Channel_ID INT(4) NOT NULL,
            Channel_Name VARCHAR(128),
            Ch_Data_Unit VARCHAR(16)
        )"""
    curs.execute(sql)

    # clear all values in table
    curs.execute('DELETE FROM checked_ch_info')
    conn.commit()

    try:
        curs.executemany('INSERT INTO checked_ch_info VALUES (?,?,?,?,?)', select_ch_info)
        conn.commit()
    except Exception:
        conn.rollback()

    conn.close()
