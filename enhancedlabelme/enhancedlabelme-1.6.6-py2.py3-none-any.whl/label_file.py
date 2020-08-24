# -*- coding: utf-8 -*-

import base64
import io
import json
import os
import os.path as osp
import codecs
import shutil
import time

import PIL.Image

from enhancedlabelme import __version__
from enhancedlabelme.logger import logger
from enhancedlabelme import PY2
from enhancedlabelme import QT4
from enhancedlabelme import utils
from datetime import datetime


PIL.Image.MAX_IMAGE_PIXELS = None


class LabelFileError(Exception):
    pass


class LabelFile(object):
    suffix = '.json'
    BLOCKSIZE = 1048576

    def __init__(self, filename=None, loadTime=str(datetime.now())):
        self.shapes = []
        self.imagePath = None
        self.imageData = None
        self.loadTime = loadTime
        if filename is not None:
            self.load(filename)
        self.filename = filename

    @staticmethod
    def load_image_file(self, filename, time):
        try:
            image_pil = PIL.Image.open(filename)
        except IOError:
            logger.error('Failed opening image file: {}'.format(filename))
            return

        # apply orientation to image according to exif
        image_pil = utils.apply_exif_orientation(image_pil)

        with io.BytesIO() as f:
            ext = osp.splitext(filename)[1].lower()
            if PY2 and QT4:
                format = 'PNG'
            elif ext in ['.jpg', '.jpeg', '.JPG', '.JPEG']:
                format = 'JPEG'
            else:
                format = 'PNG'
            image_pil.save(f, format=format)
            f.seek(0)
            return f.read()

    def load(self, filename):
        BLOCKSIZE = 1048576
        keys = [
            'version',
            'imageData',
            'imagePath',
            'shapes',  # polygonal annotations
            'flags',   # image level flags
            'imageHeight',
            'imageWidth',
            'loadTime',
            'saveTime'
        ]
        try:
            with open(filename, 'rb' if PY2 else 'r', encoding='utf-8') as f:
                data = json.load(f)
            version = data.get('version')
            if version is None:
                logger.warn(
                    'Loading JSON file ({}) of unknown version'
                    .format(filename)
                )
            elif version != '4.1.1':
                logger.warn(
                    'This JSON file ({}) may be incompatible with '
                    'current labelme. version in file: {}, '
                    'current version: {}'.format(
                        filename, version, '4.1.1'
                    )
                )

            # if data['imageData'] is not None:
            #    imageData = base64.b64decode(data['imageData'])
            #    if PY2 and QT4:
            #        imageData = utils.img_data_to_png_data(imageData)
            # else:
            #     #relative path from label file to relative path from cwd
            imagePath = osp.join(osp.dirname(filename), data['imagePath'])
            imageData = self.load_image_file(self, imagePath, str(datetime.now()))
            
            flags = data.get('flags') or {}
            imagePath = data['imagePath']
            self._check_image_height_and_width(
                base64.b64encode(imageData).decode('utf-8'),
                data.get('imageHeight'),
                data.get('imageWidth'),
            )
            shapes = [
                dict(
                    label=s['label'],
                    points=s['points'],
                    shape_type=s.get('shape_type', 'polygon'),
                    flags=s.get('flags', {}),
                    group_id=s.get('group_id')
                )
                for s in data['shapes']
            ]
        except Exception as e:
            with codecs.open(filename, "r", "euckr") as sourceFile:
                    with codecs.open('temp.json', "w", "utf-8") as targetFile:
                        while True:
                            contents = sourceFile.read(BLOCKSIZE)
                            if not contents:
                                break
                            targetFile.write(contents)
                        targetFile.close()
                    sourceFile.close()
                    os.remove(filename)
                    shutil.move('temp.json', filename)
            with open(filename, 'rb' if PY2 else 'r', encoding='utf-8') as f:
                data = json.load(f)
            version = data.get('version')
            if version is None:
                logger.warn(
                    'Loading JSON file ({}) of unknown version'
                    .format(filename)
                )
            elif version != '4.1.1':
                logger.warn(
                    'This JSON file ({}) may be incompatible with '
                    'current labelme. version in file: {}, '
                    'current version: {}'.format(
                        filename, version, '4.1.1'
                    )
                )
            imagePath = osp.join(osp.dirname(filename), data['imagePath'])
            imageData = self.load_image_file(self, imagePath, str(datetime.now()))
            
            flags = data.get('flags') or {}
            imagePath = data['imagePath']
            self._check_image_height_and_width(
                base64.b64encode(imageData).decode('utf-8'),
                data.get('imageHeight'),
                data.get('imageWidth'),
            )
            shapes = [
                dict(
                    label=s['label'],
                    points=s['points'],
                    shape_type=s.get('shape_type', 'polygon'),
                    flags=s.get('flags', {}),
                    group_id=s.get('group_id')
                )
                for s in data['shapes']
            ]


        otherData = {}
        for key, value in data.items():
            if key not in keys:
                otherData[key] = value

        # Only replace data after everything is loaded.
        self.flags = flags
        self.shapes = shapes
        self.imagePath = imagePath
        self.imageData = imageData
        self.filename = filename
        self.otherData = otherData

    @staticmethod
    def _check_image_height_and_width(imageData, imageHeight, imageWidth):
        img_arr = utils.img_b64_to_arr(imageData)
        if imageHeight is not None and img_arr.shape[0] != imageHeight:
            logger.error(
                'imageHeight does not match with imageData or imagePath, '
                'so getting imageHeight from actual image.'
            )
            imageHeight = img_arr.shape[0]
        if imageWidth is not None and img_arr.shape[1] != imageWidth:
            logger.error(
                'imageWidth does not match with imageData or imagePath, '
                'so getting imageWidth from actual image.'
            )
            imageWidth = img_arr.shape[1]
        return imageHeight, imageWidth

    def save(
        self,
        filename,
        shapes,
        imagePath,
        imageHeight,
        imageWidth,
        imageData=None,
        otherData=None,
        flags=None,
        loadTime=None,
        saveTime=None
    ):
        if imageData is not None:
            imageData = base64.b64encode(imageData).decode('utf-8')
            imageHeight, imageWidth = self._check_image_height_and_width(
                imageData, imageHeight, imageWidth
            )
        if otherData is None:
            otherData = {}
        if flags is None:
            flags = {}
        
        saveTime = str(datetime.now())
        data = dict(
            version='4.1.1',
            flags=flags,
            shapes=shapes,
            imagePath=imagePath,
            imageData=imageData,
            imageHeight=imageHeight,
            imageWidth=imageWidth,
            loadTime=self.loadTime,
            saveTime=saveTime
        )
        for key, value in otherData.items():
            """ assert key not in data """
            data[key] = value
        try:
            with open(filename, 'wb' if PY2 else 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self.filename = filename
        except Exception as e:
            raise LabelFileError(e)

    @staticmethod
    def is_label_file(filename):
        return osp.splitext(filename)[1].lower() == LabelFile.suffix
