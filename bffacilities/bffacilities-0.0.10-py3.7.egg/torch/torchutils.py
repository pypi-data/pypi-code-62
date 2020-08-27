"""
TODO reformat this file and imageutil, labelme utils
"""


import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt
import os.path as osp
from .labelmeutils import encodeImage

import torch

class PlotHelper():
    """Helper used to plot serveral images into one figure
    """
    def __init__(self, vmin = 0, vmax = 255):
        self.vmin = vmin
        self.vmax = vmax
        
    def checkzeros(self, imglist, imgstart = 0):
        channels = len(imglist)
        zero = []
        for i in range(channels):
            imgploti = imglist[i]
            # print(imgploti)
            if np.count_nonzero(imgploti) == 0:
                zero.append(i + imgstart)

        if len(zero) > 0:
            print(f"Following (total: {len(zero)}) are all zeros: ", zero)

        self.zero = zero
        return len(zero)

    def _plot(self, imglist, rows=2, cols=2, dpi=60, imgstart=0, names=None, cmap='gray'):
        """
        imglist(list(np.ndarray)):
        """

        fig = plt.figure(figsize=(18, 16), dpi= dpi, facecolor='w', edgecolor='w', clear=True)
        imgstart = imgstart * (rows * cols)
        channels = len(imglist)
        # channels = imglist.shape[0]
        if imgstart + rows * cols > channels:
            print(f"Index Invalid: {imgstart} - {rows * cols}")
            # imgstart = 0

            # names = [f"{i}" for i in range(rows * cols)]
        for idx in range(imgstart, imgstart + rows * cols): #imglist.shape[0]):
            if idx >= channels: break

            a = fig.add_subplot(rows, cols, idx - imgstart +1)
            # Turn off tick labels
            a.set_yticklabels([])
            a.set_xticklabels([])
            if names is not None:
                a.set_xlabel(names[idx])
            # plt.axis('off')
            imgploti = imglist[idx]
            imgploti = plt.imshow(imgploti, cmap=cmap) # * 255, , vmin=0, vmax=255)


    def plotImgList(self, imglist, checkzeros=True, names=None, **kwargs):
        """
        Arguments:
            imglist (np.ndarray | list | torch.Tensor)
        """
        imgtype = type(imglist)
        if imgtype == np.ndarray:
            shape = imglist.shape
            ndim = imglist.ndim 
            if ndim == 2:
                imglist = [imglist]
            elif ndim == 3:
                imglist = [img for img in imglist]
            else:
                raise ValueError(f"Unsupported ndarray shapeP: {shape} {ndim}")
        elif imgtype == list:
            pass
        elif imgtype == torch.Tensor:
            assert len(imglist.shape) == 4  ## B C H W
            imglist = imglist[0,:,:,:].cpu()
            print("Plot on converted Tensor: ", imglist.shape)
            ims = [imglist[i].cpu().numpy() for i in range(len(imglist))]
        else:
            raise ValueError(f"Unsupported type: {imgtype}")
        # print(imglist)
        if names is not None:
            assert len(names) >= len(imglist)
        if checkzeros:
            self.checkzeros(imglist, kwargs.get("imgstart", 0))

        self._plot(imglist, names=names, **kwargs)
        
    def plotTensor(self, imtensor, cmap='gray', **kwargs):
        """Tensor
        """
        tlen = len(imtensor.shape)
        if tlen == 3:
        # assert imtensor.shape[0] == 3
            im = imtensor.permute(1, 2, 0).mul(256).byte().cpu().numpy()
            self.plotArray(im, cmap, **kwargs)
        elif tlen == 4:
            ## channel may not be 3
            # print(imtensor.shape)
            for imt in imtensor:
                merged = np.zeros((imt.shape[-2], imt.shape[-1]))
                for im in imt:
                    im = im.cpu().numpy()
                    self.plotArray(im, cmap, **kwargs)
                    # merged = np.where(im > 0, im, merged)
                # self.plotArray(merged, cmap, **kwargs)

    def plotArray(self, im, cmap='gray', figsize=(12, 8), **kwargs):
        # print(im.shape)
        fig = plt.figure(figsize=figsize, dpi= 100, facecolor='w', edgecolor='w', clear=True)
        plt.imshow(im, cmap=cmap)
        plt.show()

    def plotHeatmap(self, imarr, cmap='gray', **kwargs):
        # for batch in imarr:
        hms = imarr[0]
        for hm in hms:
            self.plotArray(hm)

    def drawPoints(self, points, size=None, img=None, bright=2.5, cmap='gray', **kwargs):
        """
            points (list(np.ndarray))
            size (tuple(height, width))
        """
        # assert len(size) == 3
        assert size is not None or img is not None

        if img is None:
            img = np.zeros(size, dtype=np.float)
        else:
            img = img.copy()
        # print(img.shape)
        for po in points:
            x, y = po[:2]
            x, y = int(x), int(y)
            img[x, y] = bright
        self.plotArray(img, cmap=cmap, **kwargs)
        

from PIL import Image, ImageDraw
import imgviz
import types
import json
import shutil as sh

class MaskContourSaver():
    """
    Used to save mask contour predicted by ai. 
    @Note it depends on certain model and datasets, and outpus only mask, 
        use PredictionViewer instead, which provides keypoint label output
    @See torchutils.PredictionViewer

    Arguments:
        labels (function , list) it maps the idx of predicted results into Readable texts

        root(str): root dir contains images, should be different from dst_dir
    """

    def __init__(self, labels=None, root = None, img_suffix=".jpg", debug=False, **kwargs):
        self.debug = debug
        self.root = root
        # self.imgs = sorted([file for file in os.listdir(root) if file.endswith(img_suffix)])
        self.img_suffix = img_suffix

        if type(labels) is list:
            self._captions = labels
        else:
            label = []
            assert isinstance(labels, types.FunctionType)
            try:
                for i in range(1000):
                    label.append(labels(i))
            except: pass
            self._captions = label
        if self.root is not None:
            print("Root: ", self.root)
        print("Get captions: ", self._captions)


    def _save(self, im, dst_dir, imname, shapes, imsize):
        """
        im(np.ndarray | PIL.Image.Image)
        imname(str): image name without suffix, such as `1.jpg` will get `1`
        shapes(list(dict)):
        """
        imfilename = f"{imname}{self.img_suffix}"
        ## @See Also encodeImage
        # imageData = LabelFile.load_image_file(imgloc)
        # imageData = base64.b64encode(imageData).decode("utf-8")
        imageData = encodeImage(im, self.img_suffix)

        data = {"version": "4.5.5",
            "flags": {}, "shapes":shapes, "imagePath": imfilename, 
            "imageHeight": imsize[1],
            "imageWidth": imsize[0],
            "imageData": imageData
        }
        if self.root is not None:
            try:
                imgloc = osp.join(self.root, imfilename)
                sh.copy(imgloc, osp.join(dst_dir, imfilename))
            except Exception as e:
                print(e)
        jsonloc = osp.join(dst_dir, imname+".json")
        with open(jsonloc, "w") as f:
            f.write(json.dumps(data, indent=True))
    
    def _getPrediction(self, idx):
        """
        @Returns 
            True prediction is valid
        """
        img, _ = dataset[idx]
        imsize = img.shape[-2], img.shape[-1]
        img = img.to(device)
        predictions = self.model([img])
        prediction = predictions[0]  ## batch size is one

        self.boxes = prediction["boxes"]
        self.labels = prediction["labels"].cpu().numpy()
        self.masks = prediction['masks'].mul(255).byte().cpu().numpy()
        
        self.maskcount = masks.shape[0] if maskperimage <= 0 else maskperimage
        
    def save(self, dst_dir, dataset, imgnames, drange=None,\
            maskperimage=-1, skipUnmask=True,\
            contourDis = 8, contourGap=4, contourArea=None, contourThresh=None, contourSaveMax=False, \
            device=torch.device('cpu'), **kwargs):
        """
        Before invoking this method, model should be in `eval` mode, `with torch.no_grad()` is 
        necessary.

        Arguments:
            dataset(torch.utils.Dataset): 
                dataset should return tuple (img, target)
                Generally property: 
                1. imgs, which provide the names of images, it should be passed as parameter `imgnames`
                2. root, root_dir indicates where the data is from, it should be passed to constructor
                3. Labels, which could be used to repreter label index

            imgnames(list):
            
            drange(range):

            maskperimage(int): if -1, then no mask limit for each image

            contourThresh(tuple): [threshold, maxval, imtype]
            contourArea(int): if none, contour area will not be accounted for. Otherwise any contour whose are is less than `contourArea` will be filtered
            contourGap(int): 
            contourSaveMax(bool): Not Implemented Yet
        """
        assert dst_dir != self.root
        # device = torch.device(device)
        # assert device == self.model.device
        os.makedirs(dst_dir, exist_ok=True)
        
        if drange == None:
            drange = range(0, len(dataset))
        
        assert drange[-1] <= len(dataset)

        if contourThresh is None:
            contourThresh = [127, 255, 0]
        
        assert len(contourThresh) == 3
        print("Start prediction on: ", drange, "...")
        self.contour_areas = []
        self.skipped_idxes = []
        for idx in drange:
            self._getPrediction(idx)
            if self.maskcount == 0:
                continue

            found_contours = []
            contour_areas = []
            for c in range(self.maskcount):
                maskdata = self.masks[c, 0]
                label_name = self._captions[self.labels[c]]

                ret, thresh = cv.threshold(maskdata, contourThresh[0], contourThresh[1], contourThresh[2])
                contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

                if len(contours) == 0:
                    continue
                # reshape as a list, the first contour will be used
                contour = contours[0]
                actualarea = cv.contourArea(contour)

                if contourArea is not None and actualarea < contourArea:
                    # print("ContourArea is too small: ", actualarea)
                    continue
                
                if self.debug:
                    print("Actual contour area: ", actualarea)
                contour = contour.reshape(-1, 2)
                contour = cv.convexHull(contour)
                ## disable contourGap using hull instead
                if len(contour) > contourGap * 5:
                    contour = contour[0::contourGap]
                if len(contour) < 2:
                    continue
                found_contours.append(contour)
                contour_areas.append(actualarea)

            if len(contour_areas) > 0:
                self.contour_areas.append(contour_areas)
            shapes = []
            for contour in found_contours:
                shapes.append({"label": label_name, 
                    "points": contour.tolist(),       
                    "group_id": None,
                    "shape_type": "polygon",
                    "flags": {}
                })
            if len(shapes) == 0 and skipUnmask:
                self.skipped_idxes.append(idx)
                continue
            print(f"Idx: {idx}: mask will be saved: {len(shapes)}")

            imfilename = imgnames[idx]
            imname = imfilename[:imfilename.rfind(self.img_suffix)]
            self._save(osp.join(self.root, imfilename), dst_dir, imname, shapes, imsize)
            print("==============================")
            # if self.debug:
            #     break
        
    @staticmethod
    def saveContour(prediction, dataset, idx, saveLoc, labelList = None,\
        gap=4, size=(512, 512), img_suffix=".jpg"):
        """
        Deprecated, Use Saver instead
        Save Contour By AI prediction and CV contours

        Arguments:
            dataset(torch.utils.Dataset)
            idx(int)
            saveLoc(str)
            labels(list)
        """
        os.makedirs(saveLoc, exist_ok=True)
        boxes = prediction["boxes"]
        labels = prediction["labels"]
        masks = prediction['masks']
        i = 1
        count = masks.shape[0]
        label = labels.cpu().numpy()
        shapes = []
        if labelList is None:
            labelList = dataset.Labels
        print(f"{idx} Masks: {count}")

        imname = dataset.imgs[idx]
        imfilename = imname[:imname.rfind(img_suffix)]
        for c in range(count):
            mask = masks[c, 0]
            label_name = labelList[label[c]]
            imdata = mask.mul(255).byte().cpu().numpy()
            # im = Image.fromarray(imdata)
            # display(im)
            ret, thresh = cv.threshold(imdata, 127, 255, 0)
            contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            if len(contours) == 0:
                continue
            # reshape as a list
            contour = contours[0].reshape(-1, 2)
            if len(contour) > gap * 5:
                contour = contour[0::gap]
            if len(contour) < 2:
                continue
            shapes.append({"label": label_name, "points": contour.tolist(),       
                "group_id": None,
                "shape_type": "polygon",
                "flags": {}
            })
        imageData = LabelFile.load_image_file(osp.join(dataset.root, imname))
        imageData = base64.b64encode(imageData).decode("utf-8")
        data = {"version": "4.5.5",
            "flags": {}, "shapes":shapes, "imagePath": imname, 
            "imageHeight": size[1],
            "imageWidth": size[0],
            "imageData": imageData
        }
        with open(osp(saveLoc, imfilename+".json"), "w") as f:
            f.write(json.dumps(data, indent=True))

    @staticmethod
    def mergeLabelIntoImages(labeldir, imagedir):
        labels = os.listdir(labeldir)
        for label in labels:
            if not label.endswith(".json"):
                raise ValueError("Labels should be json file")
            path = osp.join(imagedir, label)
            if osp.exists(path):
                print("Removing: ", path)
                os.remove(path)
            sh.move(osp.join(labeldir, label), imagedir)

        sh.rmtree(labeldir)
import math
class PredictionViewer(MaskContourSaver):
    """
    1. Display model's prediction 
    2. Save prediction as labeled json files or visualized images

    Arugments:
    """

    def __init__(self, labels=None, img_suffix=".jpg", debug=False, kpcaptions=None, **kwargs):
        super().__init__(labels=labels, img_suffix=img_suffix, debug=debug, **kwargs)
        self.kpcaptions = kpcaptions
        if kpcaptions is not None:
            print("KP captions:", kpcaptions)

    @staticmethod
    def mask_to_box(mask):
        assert type(mask) is np.ndarray
        pos = np.where(mask)
        xmin = np.min(pos[1])
        xmax = np.max(pos[1])
        ymin = np.min(pos[0])
        ymax = np.max(pos[0])
        return [xmin, ymin, xmax, ymax]

    def setPrediction(self, predictions, mask3channels=True, \
        score_threshold=0.5, hint=True):
        """Note, if predictions is a tensor contains multiple predictions, the first one will be used
            and others will be droped.
            score_threshold is deprecated, if you want to filter that is not clearly identified,
            use `box_thresh` for rpn.
        """

        self.score_threshold = score_threshold

        if type(predictions) == list:
            if len(predictions) == 0:
                raise ValueError("No Prediction found")
            prediction = predictions[0]
        else:
            prediction = predictions

        self.boxes =  prediction["boxes"].cpu().numpy()
        self.labels = prediction["labels"].cpu().numpy()
        self.scores = prediction["scores"].cpu().numpy()

        # proposals = []
        # for i, score in enumerate(self.scores):
        #     # print("Score", i, score)
        #     if score > self.score_threshold:
        #         proposals.append(i)
        # self.boxes = np.take(self.boxes, proposals, axis=0)
        # print(self.boxes)

        if "masks" in prediction:
            masks = prediction['masks']
            masks = masks.permute(0, 2, 3, 1)#.squeeze(0)
            ## N H W C
            # if mask3channels:
            #     if masks.shape[1] == 1:
            #         masks = masks.repeat(1, 1, 1, 3)
            #     # now masks showld be N H W C
            # else:
            #     masks = masks.squeeze(3)
                # now masks showld be N H W
            # maskimg = []
            # for mask in masks:
                # maskim.append(mask.mul(128).byte().cpu().numpy())
                # maskimg.append(Image.fromarray(mask.mul(128).byte().cpu().numpy()))
            # self.masks = maskimg
            self.masks = masks.mul(255).byte().cpu().numpy()
            # print(self.masks.shape)
        else:
            self.masks = None
        if "keypoints" in prediction:
            keypoints = prediction["keypoints"]
            self.keypoints = keypoints.cpu().numpy()
            self.keypoints_scores = prediction["keypoints_scores"].cpu().numpy()
            # N 2
        else:
            self.keypoints = None

        # print(self.masks.shape, self.keypoints.shape)

        if hint:
            m = self.masks.shape if self.masks is not None else 0
            k = self.keypoints.shape if self.keypoints is not None else 0
            print("Found masks", m, " Keypoints: ", k)

    def convertImg(self, imarr):
        """
        Argument:
            imarr (np.ndarray) # ndim == 3 (H, W, C) channels == 3
        Return:
            np.ndarray (H, W, C)
        """
        imtype = type(imarr)
        # print(imtype)
        if imtype == np.ndarray:
            pass
        elif isinstance(imarr, torch.Tensor):
            assert len(imarr.shape) == 3
            imarr = imarr.permute(1, 2, 0)
            if imarr.shape[-1] == 1:
                imarr = imarr.repeat(1, 1 ,3)
            imarr = imarr.mul(255).byte().cpu().numpy()
        elif isinstance(imarr, (Image.Image, )):
            # im = Image.fromarray(imarr, mode="RGB")
            im = imarr
            imarr=np.asarray(imarr)
            if imarr.ndim != 3:
                imarr = np.asarray([imarr])
                imarr = np.repeat(imarr, 3, axis=0)
                imarr = imarr.swapaxes(0, 1)
                imarr = imarr.swapaxes(1, 2)
        else:
            raise ValueError("Unsupported Type", imtype)
        
        assert imarr.ndim == 3 and imarr.shape[-1] == 3
        # print("Show: ", imarr.shape)

        return imarr

    def showMask(self, imarr, box_swap_xy=True,
        # mask
        mask_threshold=30, mask_alpha=0.25, box_only=False):
        """
        @return np.ndarray
        """
        imarr = self.convertImg(imarr)

        captions = self.caption_with_score

        # print(self.boxes, captions)
        colormap = imgviz.label.label_colormap()
        if self.masks is None or box_only:
            # data = imgviz.data.arc2017()
            # bboxes = self.boxes
            if box_swap_xy:
                bboxes = []
                for box in self.boxes:
                    bboxes.append((box[1], box[0], box[3], box[2]))
            else:
                bboxes = self.boxes
            viz = imgviz.instances2rgb(imarr, bboxes=bboxes, \
                labels=self.labels, captions=captions, \
                colormap=colormap, alpha=mask_alpha, \
                font_size=12, line_width=1)
        else:
            masks = self.masks > mask_threshold
            # mask didnot need all 3 channels
            masks = masks[:, :, :, 0]
                # masks = np.squeeze(masks, axis=3)
            viz = imgviz.instances2rgb(imarr, masks=masks, \
                labels=self.labels, captions=captions, \
                colormap=colormap, alpha=mask_alpha, \
                font_size=12, line_width=1)
        return viz

    def showKeypoint(self, im, radius=5, kp_fill=None, **kwargs):
        """
        Arugments:
            im(PIL.Image.Image)
        """
        if self.keypoints is None:
            return None

        assert isinstance(im, Image.Image)
        colormap = imgviz.label.label_colormap()
        num_color = 256
        imdraw = ImageDraw.Draw(im)
        keypoints = self.keypoints[:,:,:2]
        i = 1
        for kps in keypoints:
            # print(k, fill)
            for k in kps:
                fill = tuple(x for x in colormap[num_color-i-1]) if kp_fill is None else kp_fill
                # print(fill, k)
                imdraw.rectangle([k[0] - radius, k[1] - radius, k[0]+radius, k[1]+radius], fill=fill)
                i+=1
        return im

    @property
    def caption_with_score(self):
        return [f"{self._captions[i]}: {score:.2f}" for i, score in zip(self.labels, self.scores)] #if score > self.score_threshold

    def show(self, imarr, box_swap_xy=True,
        # mask
        mask_threshold=30, mask_alpha=0.25,
        # keypoint
        radius=5, kp_fill=(128, 200, 128), **kwargs
        ):
        """Draw masks and keypoints(if exists) on the image

        @Note setPrediciton must be called before this method invoked
        
        Arguments:
            imarr (np.ndarray) # ndim == 3 (H, W, C) channels == 3
            box_swap_xy(bool), the imgviz tool xy axis seems different from the screen axis,
                so it will be swapped if necessary.

        Return:
            im (Image.Image)
        """
        imarr = self.convertImg(imarr)
        # swap x, y
        viz = self.showMask(imarr, box_swap_xy, mask_threshold=mask_threshold, mask_alpha=mask_alpha)
        im = Image.fromarray(viz)
        im = self.showKeypoint(im, radius=radius, kp_fill=kp_fill)
        return im

    def displayWrongHint(self, predictions, idx=None, showWrongHintOnly=True, expected_box_num=2):    
        self.setPrediction(predictions, hint=False)
        box_num = len(self.boxes)
        if box_num != expected_box_num:
            print(f"{idx} Wrong predicted box: ", box_num)
        elif not showWrongHintOnly:
            print("Predicted box: ", box_num)

    Save_Success = 0
    Save_SkippedNoMask = 1
    Save_NoMaskPredicted = 2

    def _maskToContour(self, found_contours, contourGap, contourThresh, contourArea):
        if self.masks is None:
            return

        maskNum = self.masks.shape[0] # 

        for ci in range(maskNum):
            label_name = self._captions[self.labels[ci]]
            maskdata = self.masks[ci]
            ret, thresh = cv.threshold(maskdata, contourThresh[0], contourThresh[1], contourThresh[2])
            # thresh = cv.adaptiveThreshold(maskdata, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)
            # if self.debug:
            # display(Image.fromarray(thresh))
            contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            # print("fondContours", maskdata.shape, label_name, len(contours))
            if len(contours) == 0:
                continue
            # reshape as a list, the first contour will be used
            newcontours = []
            for contour in contours:
                actualarea = cv.contourArea(contour)

                if contourArea is not None and actualarea < contourArea:
                    # print(f"[{label_name}] ContourArea is too small: ", actualarea)
                    continue

                contour = contour.reshape(-1, 2) # two-d array is needed for labelme
                # print("Contour ", len(contour))
                conlen = len(contour)
                if conlen < 2:
                    continue
                ncontour = []
                i = 0
                x1 = contour[i]
                ncontour.append(x1)
                i += 1
                while i < conlen - 1: 
                    x2 = contour[i]
                    dis = (x1[0] - x2[0]) ** 2 + (x1[1] - x2[1]) ** 2
                    # print(dis)
                    dis = math.sqrt(dis)
                    if dis >= contourGap or contourGap <= 0:
                        x1 = x2
                        ncontour.append(x1)
                    i += 1
                contour = np.asarray(ncontour)

                # if len(contour) > contourGap * 4:
                #     contour = contour[0::contourGap]
                newcontours.append((contour, actualarea))
            # sort by area size
            newcontours = sorted(newcontours, key=lambda x: len(x[0]), reverse=True)
            # print("Contour: ", [ len(c) for c, a in newcontours])
            found_contours[label_name] = newcontours

    def saveMask(self, im, dst_dir, imname, \
        maskperimage=-1, contourGap=6, contourArea=None, contourThresh=None,\
        skipUnmask=True, radius = 5, withoutMask=False, \
        style="labelme", **kwargs):
        """@Note setPrediciton must be called before this method invoked
        save mask / keypoints

        Arguments:
            im(torch.Tensor): image object processed by Dataset/Model, 
                it should be the same with the original image no matter how it is processed (preprocess & postprocess).
                **Note, if the Dataset/Model didnot reveal the image, you'd better pass a original Image object**
            imname(str): image pure name withou suffix
            style(str): only support `labelme` currently
            maskperimage(int): if -1, then no mask limit for each image, otherwize each class will only get certain masks
        """
        os.makedirs(osp.join(dst_dir, "Annotation"), exist_ok=True)
        im = self.convertImg(im)
        
        if contourThresh is None:
            contourThresh = [127, 255, 0]

        # print(found_contours)
        shapes = []
        ## add mask type as polygon
        if not withoutMask:
            found_contours = { c: None for c in self._captions }
            ## TODO contour will change orders
            self._maskToContour(found_contours, contourGap, contourThresh, contourArea)
            for label_name, contours in found_contours.items():
                mc = 0
                if contours is None:
                    continue
                for contour, areasize in contours:
                    if maskperimage > 0 and mc >= maskperimage:
                        break
                    mc += 1
                    shapes.append({"label": label_name, 
                        "points": contour.tolist(),       
                        "group_id": None,
                        "shape_type": "polygon",
                        "flags": {}
                    })
        if self.keypoints is not None:
            ## TODO how to map keypoints to label better?
            kpNum = self.keypoints.shape[0]
            mc = 0
            for ci in range(kpNum):
                kps = self.keypoints[ci]
                if maskperimage > 0 and mc >= maskperimage:
                    break

                label_name = self._captions[self.labels[ci]]
                for i, kp in enumerate(kps):
                    if self.kpcaptions is None:
                        ln = f"{label_name}-{i}"
                    else:
                        ln = self.kpcaptions[i]
                    # print(ln, kp)
                    shapes.append({"label": ln, 
                        "points": [ [ float(kp[0]), float(kp[1]) ] ],
                        "group_id": None,
                        "shape_type": "point",
                        "flags": {}
                    })
        if len(shapes) == 0 and skipUnmask:
            return PredictionViewer.Save_SkippedNoMask
        # print(f"mask will be saved: {len(shapes)}")

        if imname.endswith(self.img_suffix):
            imname = imname[:imname.rfind(self.img_suffix)]
        # imname should withoud suffix
        self._save(im, osp.join(dst_dir, "Annotation"), imname, \
            shapes, im.shape)
        return PredictionViewer.Save_Success

    def saveViz(self, im, dst_dir, imname, mask_threshold = 127, radius=3, **kwargs):
        """
        Arguments:
            process_func (function):
        """
        if imname.endswith(self.img_suffix):
            imfilename = imname # full name
            imname = imname[:imname.rfind(self.img_suffix)]
        else:
            imfilename = f"{imname}{self.img_suffix}"

        ## save visualized image
        os.makedirs(osp.join(dst_dir, "viz"), exist_ok=True)
        annIm = self.show(im, mask_threshold=mask_threshold, radius=radius)
        annIm.save(osp.join(dst_dir, "viz", imfilename))



from collections import defaultdict, deque
import datetime
import pickle
import time
from tqdm import tqdm

import torch.distributed as dist

class ImagePreprocessor(object):

    def __init__(self, debug=False):
        self.debug = debug

    def setImage(self, img, dst=None):
        """ Convert other format into numpy.ndarray

        Arguments:
            img(str| np.ndarray | PIL.Image.Image | torch.Tensor)
            dst(str): directory that will be used to store processed images
        """
        self.dst = dst
        imtype = type(img)
        if imtype == str:
            self._img = np.asarray(Image.open(img))
        elif imtype == np.ndarray:
            self._img = img
        elif isinstance(img, Image.Image):
            self._img = np.asarray(img)
        elif isinstance(img, torch.Tensor):
            if img.ndim == 3:
                img = img.permute(1, 2, 0)
            ## TODO check img max val ?
            self._img = img.mul(255).byte().cpu().numpy()
        else:
            raise ValueError(f"Type Not Supported: {imtype}")
        
        assert self._img.dtype == np.uint8

        if self.debug:
            print(self._img.shape, self._img.dtype)

    def rotate(self, angle, center=None, scale=1.0, boarderValue=(0,0,0)):
        """
        Note: some problems may not be solved currently
        """
        img = self._img
        h, w = img.shape[:2]
        if center is None:
            center = (w // 2, h // 2)
        M = cv.getRotationMatrix2D(center, angle, scale)
        rotated = cv.warpAffine(img, M, (w, h), borderValue=boarderValue)
        return rotated

    def getRoiByConnected(self, thresh, areaSize):
        '''
        Arguments:
            thresh (np.ndarray): preprocessed thresh image
            areaSize(int): any components whose size is less than `areaSize` 
                will be filtered, if None, no components will be filtered
        '''
        img = self._img
        num_labels, labels, stats, centers = cv.connectedComponentsWithStats(thresh, connectivity=8, ltype=cv.CV_32S)
        image = None
        if self.debug:
            image = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
            # image = np.asarray(image, dtype=np.float32)
            print(image.shape, image.ndim,image.dtype)
            # print(num_labels)
        roi_list = []
        ## TODO figure out why it starts from 1
        for t in range(1, num_labels, 1):
            x, y, w, h, area = stats[t]
            if areaSize is not None and area < areaSize:
                continue
            # save roi coordinate and width and height
            roi_list.append((x, y, w, h))
            if self.debug:
                cx, cy = centers[t]
                # 标出中心位置
                cv.circle(image, (np.int32(cx), np.int32(cy)), 2, (0, 255, 0), 2, 8, 0)
                # 画出外接矩形
                cv.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2, 8, 0)
                showImage(image, name="debug components", size=(w, h))
                break

        return num_labels, labels, roi_list, image

    CROP_RETAIN_WH = 0
    CROP_MIN_WH = 1
    CROP_MAX_WH = 2
    def cropByComponents(self, roi = None, \
        thresh=127, maxval=255, 
        dst_size=100000, xoff=0, yoff=0,
        crop_policy=CROP_MIN_WH, areaSize = 24000
        ):
        """
        Arguments:
            dst_size(int): final size of the image if specified
            xoff(int): offset for x
            yoff(int): offset for y

            roi (list(int)): x , y, w, h
                if roi is None: processor will try to find the first area 
                that is connected and it's size is greater than areaSize
            dst(str): image file saved location
            crop_policy(int): if 0,  width and height will be retained, 
                if greater than 0, final width and height will be the same,
                if 1, the width and height will be the smallest one
                if 2, biggest one
        """
        # im = cv.imdecode(np.fromfile(f"{src}", dtype=np.uint8), imread_type) # gray
        im = self._img
        if self._img.ndim == 3 and self._img.shape[-1] != 1:
            gray = cv.cvtColor(im, cv.COLOR_RGB2GRAY)
        else:
            gray = im

        ret, th1 = cv.threshold(gray, thresh, maxval, cv.THRESH_BINARY | cv.THRESH_OTSU )

        # contours, hierarchy = cv.findContours(im, 1, 2)
        # cnt = contours[0]
        # area = cv.contourArea(cnt)
        if roi is None:
            num_labels, labels, roi_list, image = self.getRoiByConnected(th1, areaSize=areaSize)
            x, y, w, h = roi_list[0]
        else:
            x, y, w, h = roi
        # rois.append(roi_list[0])
        if crop_policy == ImagePreprocessor.CROP_MIN_WH:
            mwh = min(w, h, dst_size)
            w = h = mwh
        elif crop_policy == ImagePreprocessor.CROP_MAX_WH:
            mwh = max(w, h, dst_size)
            w = h = mwh
        else:
            raise ValueError("Policy not supported!")
        x += xoff
        y += yoff
        cimage = im[ y:y+h, x:x+w ]

        if self.debug:
            print("ROI: ", x, y, " WH: ", w, h)
            showImage(cimage)

        self.crop_img = cimage
        self.crop_roi = [x, y, w, h] # roi_list[0]
        # return roi_list[0]

    def saveImage(self, img, dst, imsuffix=".jpg"):
        retval, buf = cv.imencode(imsuffix, cimage)
        buf.tofile(dst)

    def findEdge(self, im = None, thresh=127, maxval=255, \
            canny_thresh1=120, canny_thresh2=200, edge_weight= 0.6):
        ''' This is a test function and may change sometimes
        Arguments:
            im(np.ndarray): 
        '''
        # gray = cv.imdecode(np.fromfile(impath, dtype=np.uint8), 0)
        # gray = np.copy(self._img)
        if im is None:
            im = self._img

        if im.ndim == 3 and im.shape[-1] != 1:
            gray = cv.cvtColor(im, cv.COLOR_RGB2GRAY)
        else:
            gray = np.copy(im)
        # gray = cv.GaussianBlur(gray, (3, 3), 1)
        cimg = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)
        circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT,1, 100,
                                    param1=50,param2=30,minRadius=30,maxRadius=84)
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

        # ret, th1 = cv.threshold(gray, thresh, maxval, cv.THRESH_BINARY | cv.THRESH_OTSU )
        th1 = cv.adaptiveThreshold(gray, maxval, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 15, 0 )
        # ret, th1 = cv.threshold(th1, thresh, maxval, cv.THRESH_BINARY | cv.THRESH_OTSU )

        # 开闭运算去除噪点
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))
        th1 = cv.morphologyEx(th1, cv.MORPH_OPEN, kernel)
        th1 = cv.morphologyEx(th1, cv.MORPH_CLOSE, kernel)

        edge = cv.Canny(th1, canny_thresh1, canny_thresh2)
 
        # if self.debug:
        #     dst = cv.addWeighted(gray, (1-edge_weight), edge, edge_weight, 0)
        #     plt.figure(figsize=(10, 8 ), dpi=100)
        #     plt.imshow(dst, cmap='gray')
        #     plt.show()

        return edge, th1, cimg

    # show the colorful components
    def colorImg(self, thresh, num_labels, labels):
        '''
        thresh: 填充后的二值图
        num_labels: 连通组件的个数
        labels: 连通组件的输出标记图像，背景index=0
        '''
        # make the colors
        colors = []
        for i in range(num_labels):
            b = np.random.randint(0, 256)
            g = np.random.randint(0, 256)
            r = np.random.randint(0, 256)
            colors.append((b, g, r))
        colors[0] = (0, 0, 0)

        # draw the image
        h, w = thresh.shape
        image = np.zeros((h, w, 3), dtype=np.uint8)
        for row in range(h):
            for col in range(w):
                image[row, col] = (colors[labels[row, col]])

        return image

class CvImageReader(dict):
    """
    """
    def __init__(self, root, rootId, img_type=0, img_suffix=".png", **kwargs):
        super().__init__()
        self.root = root
        self.rootId = rootId
        self.img_suffix = img_suffix
        self.imgs = list(sorted([img for img in sorted(os.listdir(osp.join(root, rootId))) if img.endswith(self.img_suffix)]))
        self.img_type = img_type
        print("Dataset: ", len(self.imgs))

    def plt_hist(self, idxes, prange=None, density=False, stacked=False):
        """
        Arguments:
            idxes(list(int) | int)
            prange(list): plt range (two elements)
        """
        if prange is None:
            prange = [0, 256]

        if type(idxes) == list:
            imgs = []
            paths = []
            for idx in tqdm(idxes):
                img, path = self[idx]
                # img.append(img.ravel())
                # p = path[path.rfind("\\")+1:]
                # paths.append(p)
                plt.hist(img.ravel(), 256, prange, stacked=stacked, density=density)
            # print(paths, len(imgs))
            # imgs = np.asarray(imgs)
            plt.show()
        elif type(idxes) == int:
            img, path = self[idxes]
            plt.hist(img.ravel(), 256, prange, density=density)
            if not stacked:
                plt.xlabel(path)
        else:
            print("Not Supported!")

    def __getitem__(self, idx):
        if self.rootId is not None:
            path = osp.join(self.root, self.rootId, self.imgs[idx])
        else:
            path = osp.join(self.root, self.imgs[idx])
        return cv.imread(path, self.img_type), path

    def __len__(self):
        return len(self.imgs)

def saveROIOnly(src, dst = None, imread_type = 0):
    """ imread_type: IMREAD_GRAY 0 gray , IMREAD_COLOR
    """
    # src = config.DataDir / "train_raw"
    im = cv.imdecode(np.fromfile(f"{src}", dtype=np.uint8), imread_type) 
    # ret, th1 = cv.threshold(im, 127, 255, cv.THRESH_BINARY)
    th2 = cv.adaptiveThreshold(im,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY, 25, 2)
    # kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7,7))
    # morphed = cv.morphologyEx(th2, cv.MORPH_CLOSE, kernel)
    # plt.imshow(morphed, 'gray')
    cnts = cv.findContours(th2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
    cnt = sorted(cnts, key=cv.contourArea)[-1]
    ## (4) Crop and save it
    x,y,w,h = cv.boundingRect(cnt)
    print(x, y, w, h)
    plt.imshow(im[y:y+h, x:x+w], 'gray')
    plt.xticks([]), plt.yticks([])
    
    plt.show()

def resizeKeepRatio(img, size, ori_size = None):
    """ori_size: None, size should be tuple
        tuple, width of size will be used (height will be ignored), keep ratio
        @retrun resized image
    """
    if ori_size is not None:
        h = ori_size[1] / ori_size[0] * size[0]
        size = (size[0], int(h))
    return cv.resize(img, size)

def showImage(img, name = "default", size = (1024, 1024), ori_size = None, skip_wait=False):
    if size is not None:
        img = resizeKeepRatio(img, size, ori_size)
    cv.imshow(name, img)
    if not skip_wait:
        cv.waitKey(0)


def warmup_lr_scheduler(optimizer, warmup_iters, warmup_factor):

    def f(x):
        if x >= warmup_iters:
            return 1
        alpha = float(x) / warmup_iters
        return warmup_factor * (1 - alpha) + alpha

    return torch.optim.lr_scheduler.LambdaLR(optimizer, f)

class F1ScoreCalcor():
    """Binary Label F1-score calculator
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self.TP = 0
        self.FP = 0
        self.FN = 0

    def compare(self, preds, targets):
        """
        Arguments:
            preds(Tensor): (n x 1)
            targets(Tensor): (n x 1)
        """
        self.TP += np.sum(preds & (targets == 1))
        self.FP += np.sum(preds & (targets == 0))
        self.FN += np.sum(~preds & (targets == 1))

    def export(self, printit=True):
        TP = self.TP
        FP = self.FP
        FN = self.FN
        precision = TP / (TP+FP)
        recall = TP / (TP + FN)
        f1score = 2 * precision * recall / (precision + recall)
        if printit:
            print(f"TP {self.TP}, FP {self.FP}, FN {self.FN}, Precision: {precision:.6f}, Recall: {recall}, F1-score: {f1score}")
        return precision, recall, f1score

class PearsonCorrelation(torch.nn.Module):


    def forward(self,tensor_1,tensor_2):
        x = tensor_1
        y = tensor_2

        vx = x - torch.mean(x)
        vy = y - torch.mean(y)

        cost = torch.sum(vx * vy) / (torch.sqrt(torch.sum(vx ** 2)) * torch.sqrt(torch.sum(vy ** 2)))
        return cost

class PearsonClassfication():
    """
    Arguments:
        base (torch.Tensor)
        converter( Callable ): which is used to convert imgs into torch.Tensor if not None
    """
    def __init__(self, base, converter=None):
        self.pc = PearsonCorrelation()
        self.converter = converter
        if not isinstance(base, torch.Tensor) and self.converter is not None:
            base = self.converter(base)
        self.base = base
        assert isinstance(self.base, torch.Tensor)

    def compare(self, imglists, thresh, names = None):
        """
        Arguments:
            imglists(list(torch.Tensor) Iterable) it could be a list which contains torch.Tensor instances,
                or it could be just torch.utils.data.Dataset which is iterable for getting images,
                if elemetns in list is not instance of torch.Tensor and converter is not None,
                then it will be converted first
            names(list(str) | None)
        """
        similar = []
        unsimilar = []
        corr = []
        self.pc.eval()
        print("Length of list to be checked: ", len(imglists))
        with torch.no_grad():
            for idx, img in enumerate(imglists):
                if type(img) is tuple:
                    img = img[0]
                if not isinstance(img, torch.Tensor) and self.converter is not None:
                    img = self.converter(img)
                assert isinstance(img, torch.Tensor)

                c = self.pc(self.base, img)
                corr.append(c)
                name = names[idx] if names is not None else ""
                if c > thresh:
                    similar.append((img, name))
                else:
                    unsimilar.append((img, name))
        return similar, unsimilar, corr


def getSGDOptimizer(model, lr=0.005, weight_decay=0.00002, step_size=6):
    params = [p for p in model.parameters() if p.requires_grad]
    for name, param in model.named_parameters():
         if param.requires_grad:
            print(name)

    optimizer = torch.optim.SGD(params, lr=lr,
                                momentum=0.9, weight_decay=weight_decay)
    # and a learning rate scheduler
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer,
                                                step_size=step_size,
                                                gamma=0.2)
    return optimizer, lr_scheduler