#!/usr/bin/env python3

from dataclasses import dataclass

import cv2
import numpy as np

resName2size = {"2K": (2208, 1242), "FHD": (1920, 1080), "HD": (1280, 720), "VGA": (672, 376)}
resSize2name = {v: k for k, v in resName2size.items()}


@dataclass
class StereolabsCalib:
	sn: str = ""
	size: tuple = (-1, -1)

	cameraMatrixL: np.ndarray = np.float64([])
	distCoeffsL: np.ndarray = np.float64([])

	cameraMatrixR: np.ndarray = np.float64([])
	distCoeffsR: np.ndarray = np.float64([])

	T: np.ndarray = np.float64([])
	R_zed: np.ndarray = np.float64([])


@dataclass
class Params:
	paramsDescription: str = ""
	slCalib: StereolabsCalib = StereolabsCalib
	R: np.ndarray = np.float64([])
	R1: np.ndarray = np.float64([])
	R2: np.ndarray = np.float64([])
	P1: np.ndarray = np.float64([])
	P2: np.ndarray = np.float64([])
	Q: np.ndarray = np.float64([])
	f: float = -1.0
	centers: np.ndarray = np.float64([])


def save_params(calib_dir: str, params: Params):
	filename = calib_dir + "/" + params.slCalib.sn + "_" + resSize2name[params.slCalib.size] + ".yaml"
	fs = cv2.FileStorage(filename, cv2.FILE_STORAGE_WRITE)
	fs.write('description', params.paramsDescription)
	fs.write('sn', params.slCalib.sn)
	fs.write('size', params.slCalib.size)
	fs.write('cameraMatrixL', params.slCalib.cameraMatrixL)
	fs.write('distCoeffsL', params.slCalib.distCoeffsL)
	fs.write('cameraMatrixR', params.slCalib.cameraMatrixR)
	fs.write('distCoeffsR', params.slCalib.distCoeffsR)
	fs.write('stereo_T', params.slCalib.T)
	fs.write('stereo_R_zed', params.slCalib.R_zed)
	fs.write('stereo_R', params.R)
	fs.write('stereoRectify_R1', params.R1)
	fs.write('stereoRectify_R2', params.R2)
	fs.write('stereoRectify_P1', params.P1)
	fs.write('stereoRectify_P2', params.P2)
	fs.write('stereoRectify_Q', params.Q)
	fs.write('stereoRectify_f', params.f)
	fs.write('stereoRectify_centers', params.centers)
	fs.release()


def load_params(filename: str):
	fs = cv2.FileStorage(filename, cv2.FILE_STORAGE_READ)
	params = Params()

	params.paramsDescription = fs.getNode('description').string()
	params.slCalib.sn = fs.getNode('sn').string()
	size_mat = fs.getNode('size').mat()
	params.slCalib.size = (int(size_mat[0][0]), int(size_mat[1][0]))
	params.slCalib.cameraMatrixL = fs.getNode('cameraMatrixL').mat()
	params.slCalib.distCoeffsL = fs.getNode('distCoeffsL').mat()
	params.slCalib.cameraMatrixR = fs.getNode('cameraMatrixR').mat()
	params.slCalib.distCoeffsR = fs.getNode('distCoeffsR').mat()
	params.slCalib.T = fs.getNode('stereo_T').mat()
	params.slCalib.R_zed = fs.getNode('stereo_R_zed').mat()
	params.R = fs.getNode('stereo_R').mat()
	params.R1 = fs.getNode('stereoRectify_R1').mat()
	params.R2 = fs.getNode('stereoRectify_R2').mat()
	params.P1 = fs.getNode('stereoRectify_P1').mat()
	params.P2 = fs.getNode('stereoRectify_P2').mat()
	params.Q = fs.getNode('stereoRectify_Q').mat()
	params.f = fs.getNode('stereoRectify_f').real()
	params.centers = fs.getNode('stereoRectify_centers').mat()

	fs.release()
	return params
