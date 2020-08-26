# -*- coding:utf-8 -*-

"""
define some constants for global control
"""

PROCESSED_MF4_FILES = []

DB_FILES = []

MASTER_TABLE_NAMES = ['groups', 'channels', 'group_channel',
                      'timestamp', 'group_ts',
                      'data_no_resample', 'channel_data_no_resample',
                      'data_after_resample', 'channel_data_after_resample']

VEH_STATIC_TABLE_NAMES = ['veh_static']

OBJLIST_TABLE_NAMES = ['radar_loc', 'tracker', 'radar_tracker', 'attribute', 'tracker_attr']

CHECKED_TABLE_NAMES = []

RADAR = [(0, 'RM'), (1, 'RS')]

TRACKER_ATTR = ('posX_Left_m',
                'posX_m',
                'posX_Right_m',
                'posY_Left_m',
                'posY_m',
                'posY_Right_m',
                'velX_mps',
                'velY_mps',
                'velX_rel_mps',
                'velY_rel_mps',
                'accX_mpss',
                'accY_mpss',
                'accX_rel_mpss',
                'accY_rel_mpss',
                'yaw_rate_degps',
                'stdPosX',
                'stdPosY',
                'stdPosX_Left',
                'stdPosY_Left',
                'stdPosX_Right',
                'stdPosY_Right',
                'stdVelX',
                'stdVelY',
                'stdAccX',
                'stdAccY',
                'boxCenterPosX',
                'boxCenterPosY',
                'boxLength',
                'boxWidth',
                'fusionWeight',
                'objQuality.bits.bIsValid',
                'objQuality.bits.bIsActive',
                'objQuality.bits.bIsFused',
                'objQuality.bits.bIsPossibleMirror',
                'objQuality.bits.bIsConfirmedByRSPTracker',
                'objQuality.bits.bIsInsideFreespace',
                'objQuality.bits.bIsOutsideStationaryCloud',
                'objQuality.bits.bDoesNotMatchEgoYawRate_Direction',
                'objQuality.bits.bDoesNotMatchEgoYawRate_XYSpeed',
                'objQuality.bits.bAssoicatedWithGoodDet',
                'objQuality.bits.bIsGoodQuality',
                'objQuality.u_value',
                'observationHist',
                'lifetime',
                'stationaryCounter',
                'heading',
                'globalID',
                'objID',
                'objMtnClass',
                'objTypClass',
                'objProbExist',
                'objConfidence')
