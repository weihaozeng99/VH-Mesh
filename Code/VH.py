import boundingbox3d as d3
import boundingbox2d as d2
import open3d as o3d

caliaddr=input("Input the path of the calibration parameters")
Pmat=d2.cali(caliaddr)
