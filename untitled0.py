# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 19:38:25 2018

@author: shahi
"""

import cv2
import numpy as np

#read in either image
reg = cv2.imread('./reg2.jpg')
foil = cv2.imread('./foil2.jpg')
combo = cv2.imread('./foilVsNonFoil.jpg')
# convert the colour spaces
reg_hsv = cv2.cvtColor(reg,cv2.COLOR_RGB2HSV)
reg_hsv[:, :, 0] = cv2.convertScaleAbs(reg_hsv[:,:,0],alpha=255/180)
foil_hsv = cv2.cvtColor(foil,cv2.COLOR_RGB2HSV)
foil_hsv[:, :, 0] = cv2.convertScaleAbs(foil_hsv[:,:,0],alpha=255/180)
full_reg_hsv = cv2.hconcat((reg_hsv[:,:,0],reg_hsv[:,:,1],reg_hsv[:,:,2]))
full_foil_hsv = cv2.hconcat((foil_hsv[:,:,0],foil_hsv[:,:,1],foil_hsv[:,:,2]))

both_hsv = cv2.cvtColor(combo,cv2.COLOR_RGB2HSV)
both_hsv[:, :, 0] = cv2.convertScaleAbs(both_hsv[:, :, 0], alpha=255/180)
full_both_hsv = cv2.hconcat((both_hsv[:, :, 0], both_hsv[:, :, 1], both_hsv[:, :, 2]))
# show side by side
cv2.namedWindow('hsv_reg', cv2.WINDOW_NORMAL)
cv2.namedWindow('hsv_foil', cv2.WINDOW_NORMAL)
cv2.imshow('hsv_reg', full_reg_hsv)
# cv2.setWindowProperty('hsv_reg',cv2.WND_PROP_AUTOSIZE,cv2.WINDOW_NORMAL)
cv2.imshow('hsv_foil', full_foil_hsv)
# cv2.setWindowProperty('hsv_foil',cv2.WND_PROP_AUTOSIZE,cv2.WINDOW_NORMAL)

cv2.namedWindow('Side By Side Comparison', cv2.WINDOW_NORMAL)
cv2.imshow('Side By Side Comparison', full_both_hsv)
cv2.waitKey(0)
