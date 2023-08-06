import numpy as np
from scipy import ndimage
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
from pyFAI.detectors import Detector
import silx.io


def find_direct_beam(m, corners=None):
    if corners is None:
        center = ndimage.measurements.center_of_mass(m, index='int')
    else:
        cropM = crop_image(m, corners)
        centerCrop = ndimage.measurements.center_of_mass(cropM, index='int')
        center = [centerCrop[0] + corners[2], centerCrop[1] + corners[0]]
    return list(reversed(center))


def crop_image(m, corners):
    """

    Args:
        m: 2D array
        corners: [x1,Y1, X2, Y2] (bottom left and top right corners)
    Returns:

    """
    i1 = int(corners[0])
    i2 = int(corners[2])
    j1 = int(corners[1])
    j2 = int(corners[3])
    cropM = m[j1:j2, i1:i2]
    return cropM


def regisoPyFAI(data, mask, x0, y0, pixel_size, bins, distance, wavelength):
    det = Detector(pixel1=pixel_size/1000, pixel2=pixel_size/1000)
    poni1 = y0*pixel_size
    # det = Pilatus1M()
    poni1 = y0*pixel_size/1000
    poni2 = x0*pixel_size/1000
    ai = AzimuthalIntegrator(dist=distance/1000, poni1=poni1, poni2=poni2,
                             detector=det, wavelength=wavelength*1e-10)
    results = ai.integrate1d(data, bins, correctSolidAngle=False,
                             error_model='poisson',
                             mask=mask, unit='r_mm')
    return results.radial, results.intensity, results.sigma

# TODO: handle inf and nan pixels
def regiso(data, mask, x0, y0, x_pixel_size, y_pixel_size, bins, error=None):
    y, x = np.indices(data.shape, dtype=np.float)
    y = (y-y0)*y_pixel_size
    x = (x-x0)*x_pixel_size
    r_grid = np.ma.masked_array(data=np.sqrt(x**2+y**2), mask=mask).compressed()
    masked_data = np.ma.masked_array(data=data, mask=mask, dtype=np.float).compressed()
    # masked_data = np.ma.masked_invalid(masked_data)
    if bins is None:
        maxd = np.max(r_grid)
        bins = len(np.arange(0, maxd))
    edges = np.histogram_bin_edges(r_grid, bins=bins)
    # edges = np.arange(np.max(r_grid))
    indexes = np.digitize(r_grid, edges, right=False)
    counts = np.bincount(indexes)[1:]
    r_mean = np.bincount(indexes, weights=r_grid)[1:]/counts
    r_square = np.bincount(indexes, weights=r_grid**2)[1:]/counts
    intensity = np.bincount(indexes, weights=masked_data)[1:]/counts
    if error is None:
        di = np.sqrt(intensity*counts)/counts
    else:
        masked_error = np.ma.masked_array(data=error, mask=mask, dtype=np.float).compressed()
        di = np.sqrt(np.bincount(indexes, weights=masked_error**2)[1:]) / counts
    # TODO: check error bar on r
    dr = np.sqrt(r_square-r_mean**2+1/12)  # 1/12 is the variance of one pixel
    # dr = np.sqrt(r_square - r_mean ** 2 + 1 / 12)
    d = {'counts': np.bincount(indexes), 'edges': edges, 'indexes': indexes, 'r_grid': r_grid,
         'masked_data':  masked_data}
    return r_mean, intensity, di, dr


def regisoPasi(data, mask, x0, y0, pixel_size):
    nx = len(data)
    siz = data.shape
    k = int(np.floor(1.5*nx))
    s = np.zeros(k)
    ds = np.zeros(k)
    ncase = np.zeros(k)
    r = np.zeros(k)
    sr2 = np.zeros(k)
    # centre de regroupement
    creg = np.complex(x0, y0)
    err2 = data.copy()
    max_n = 0
    min_n = nx
    for vi in range(siz[1]):
        for vj in range(siz[0]):
            rij = np.complex(vi, vj)
            d_reg = np.abs(rij-creg)
            if not mask[vj, vi] and data[vj,vi]>=0:
                nr = int(np.round(d_reg))
                if nr > max_n:
                    max_n = nr
                elif nr < min_n:
                    min_n = nr
                s[nr] += data[vj, vi]
                ds[nr] += err2[vj, vi]
                ncase[nr] += 1
                r[nr] += d_reg
                sr2[nr] += d_reg**2
    s = s[min_n:max_n]
    ds = ds[min_n:max_n]
    ncase = ncase[min_n:max_n]
    r = r[min_n:max_n]
    sr2 = sr2[min_n:max_n]

    sc = s/ncase
    dsc = np.sqrt(ds)/ncase
    rc = r/ncase
    drc = np.sqrt((sr2/ncase)-rc**2)
    rc = rc*pixel_size
    drc = (1/(2*3**0.5)+drc)*pixel_size
    return rc, sc, dsc, drc


def xy2polar(data, mask, x0, y0,npt_r, npt_chi):
    """
    truc de descri

    Args:
        data:
        mask:
        x0 (float):
        y0 (float):
        npt_r (int):
        npt_chi (int):

    Returns:
        str : the last entry key

    """
    y, x = np.indices(data.shape, dtype=np.float)
    y = y - y0
    x = x - x0
    r_grid = np.ma.masked_array(data=np.sqrt(x ** 2 + y ** 2), mask=mask).compressed()
    masked_data = np.ma.masked_array(data=data, mask=mask, dtype=np.float).compressed()
    chi_grid = np.ma.masked_array(data=np.angle(x + 1j*y, deg=True), mask=mask).compressed()
    count, b, c = np.histogram2d(r_grid, chi_grid, (npt_r, npt_chi))
    count1 = np.maximum(1, count)
    bins_azim = (b[1:] + b[:-1]) / 2.0
    bins_deg = (c[1:] + c[:-1]) / 2.0
    sum_, b, c = np.histogram2d(r_grid, chi_grid, (npt_r, npt_chi),
                                weights=masked_data)
    i = sum_ / count1
    i[count == 0] = -1
    # i_masked = np.ma.masked_less(i,0, copy=True)
    return bins_azim, bins_deg, i

def qResolPinhole(r, dr, wavelength, dlsurl, r1, r2, l1, l2):
    """
    Compute dQ for pinhole collimator geometry
     - r: distance au centre du détecteur
     - dr: ecart type sur r
     - wavelength : en A
     - dlsurl
     - r1 : rayon du pinhole d'entrée (mm)
     - r2 : rayon du pinhole de sortie (mm)
     - l1 : distance de collimation
     - l2 : distance échantillon détecteur

    calcul d'après:
    Optimization of the experimental resolution for small-angle scattering
    D.F.R. Mildner, J.M. Carpenter
    J. Appl. Cryst., 1984, 17, 249-256
    """
    k = 2 * np.pi / wavelength
    q = k * 2 * np.sin(np.arctan(r / l2) / 2)
    lp = 1 / (1 / l1 + 1 / l2)
    vql = q ** 2 * dlsurl ** 2
    vqd = k ** 2 * (dr / l2) ** 2
    vqc = k ** 2 * ((r1 / l1) ** 2 + (r2 / lp) ** 2) / 4
    dq = np.sqrt(vql + vqd + vqc)
    return q, dq


def qResolSlits(r, dr, wavelength, dlsurl, x1, y1, x2, y2, l1, l2, l):
    """
    Compute dQ for slit collimator geometry
     - r: distance from beam center
     - dr: root mean square variation on r
     - wavelength : in A
     - dlsurl : relative wavelength variation
     - x1 : half width first slit (mm)
     - y1 : half height first slit (mm)
     - x2 : half width second slit (mm)
     - y2 : half height second slit (mm)
     - l1 : distance between slits (mm)
     - l2 : sample to detector distance (mm)
     - l : last slit to sample distance (mm)
    """
    k = 2 * np.pi / wavelength
    q = k * 2 * np.sin(np.arctan(r / l2) / 2)
    lp = 1 / (1 / l1 + 1 / l2)
    dt1 = (x1 ** 2 + y1 ** 2) * (1 + l / l2) ** 2
    dt2 = (x2 ** 2 + y2 ** 2) * (1 + l / (l1 + l2)) ** 2
    dq2 = k ** 2 / 12 * (dt1 / (2 * l1 ** 2) + dt2 / (2 * lp ** 2) + (dr / l2) ** 2) + q ** 2 * dlsurl ** 2
    dq = np.sqrt(dq2)
    return q, dq


def qMapWithResol(data_shape, x0, y0, x1, x2, y1, y2, dc, distance,
                  x_pixel_size, y_pixel_size, wavelength, dlsurl):
    """
    Compute he Q map over a detector and the dQ maps
    Args:
        data_shape: shape of detector data
        x0: beam center horizontal
        y0: beam center vertical
        x1: half width first slit
        x2: half width second slit
        y1: half height first slit
        y2: half height second slit
        dc: collimation distance
        distance: sample to detector distance
        x_pixel_size: horizontal pixel size
        y_pixel_size: vertical pixel size
        wavelength: beam wavelength
        dlsurl: normalized wavelength standard deviation

    Returns:
        qx: 2D array
        qy: 2D array
        qz: 2D array
        dqx: 2D array
        dqy: 2D array
        dqz: 2D array


    """
    y, x = np.indices(data_shape)
    y = (y - y0) * y_pixel_size
    x = (x - x0) * x_pixel_size
    theta = np.arctan(x/distance)
    alpha = np.arctan(y/distance)
    # horizontal componant of Q
    qx = 2*np.pi/wavelength * np.sin(theta)
    # vertical component of Q
    qy = 2*np.pi/wavelength*np.sin(alpha)
    # along beam component (plus component inverse to beam)
    qz = -2*np.pi/wavelength*(np.cos(theta)*np.cos(alpha)-1)
    dtheta2 = 1/3*(x1**2+x2**2)/dc**2+1/3*(x2**2+x_pixel_size**2)/distance**2
    dalpha2 = 1 / 3 * (y1 ** 2 + y2 ** 2) / dc ** 2 + 1 / 3 * (y2 ** 2 + y_pixel_size ** 2) / distance ** 2
    k = 2*np.pi/wavelength
    dqx = (np.sin(alpha) * np.sin(theta))**2 * dalpha2
    dqx += (np.cos(alpha) * np.cos(theta))**2 * dtheta2
    dqx += (np.cos(alpha) * np.sin(theta)*dlsurl)**2
    dqx = k*np.sqrt(dqx)
    dqy = k * np.sqrt(np.cos(alpha)**2 * dalpha2 + (np.sin(alpha)*dlsurl)**2)
    dqz = (dlsurl*(np.cos(theta)*np.cos(alpha)-1))**2
    dqz += (np.sin(alpha)*np.cos(theta))**2 * dalpha2
    dqz += (np.cos(alpha)*np.sin(theta))**2 * dtheta2
    dqz = k * np.sqrt(dqz)
    return qx, qy, qz, dqx, dqy, dqz



if __name__ == '__main__':
   import matplotlib.pyplot as plt
   from matplotlib import colors
   import time
   t0= time.time()
   qx, qy, qz, dqx, dqy, dqz = qMapWithResol((943,1000),64,64, 12,12, 3, 3, 5000,5000, 3,3, 5, 0.1)
   t1=time.time()
   print('%.2f s' % (t1-t0))
   dqsurq2 = (((2*qx*dqx)**2+2*(2*qy*dqy)**2+(2*qz*dqz)**2))**0.5
   # plt.imshow(dqsurq2, norm=colors.LogNorm())

   plt.imshow(dqy/qy,norm=colors.LogNorm())
   plt.show()