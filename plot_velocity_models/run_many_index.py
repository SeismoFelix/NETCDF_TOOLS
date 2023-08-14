import os
import numpy as np
import glob

def write_param(par,lat_bound,lon_bound,depth):
    open_param = open('param_{}.txt'.format(depth),'w')
    open_param.write('Variable: {}\n'.format(par))
    open_param.write('Depth: {}\n'.format(depth))
    open_param.write('Latitude_boundaries: {}\n'.format(lat_bound))
    open_param.write('Longitude_boundaries: {}'.format(lon_bound))
    open_param.close()
    cp_par = 'cp param_{}.txt param.txt'.format(depth)
    print(cp_par)
    os.system(cp_par)

def run_plot(depth):
    run = 'python index_vm.py -mode 2 -file MESWA_2.nc'
    print(run)
    os.system(run)
    pdf_list = glob.glob('*{}.pdf'.format(depth))
    if  len(pdf_list) != 0:
        mv_sol = 'mv *{}.pdf param_{}.txt ALL_DEPTHS/'.format(depth,depth)
        print(mv_sol)
        os.system(mv_sol)
        work = True
    else:
        work = False
    return(work)

if __name__=='__main__':
    par = 'VP'
    #[  0.   2.   4.   6.   8.  10.  12.  14.  16.  18.  20.  22.  24.  26.
    #  28.  30.  32.  34.  36.  38.  40.  42.  44.  46.  48.  50.  52.  54.
    #  56.  58.  60.  62.  64.  66.  68.  70.  80.  90. 100. 110. 120. 130.
    # 140. 150. 160. 170. 180. 190. 200. 210. 220. 230. 240. 250. 260. 270.
    # 280. 290. 300. 310. 320. 330. 340. 350. 360. 370. 380. 390. 400.]
    depth_list = np.arange(0,82,2)
    lat_bound = ''
    lon_bound = ''

    bad_run = []
    for depth in depth_list:
        print('*******')
        write_param(par,lat_bound,lon_bound,depth)
        work = run_plot(depth)
        if work:
            pass
        else:
            bad_run.append(depth)
    
    if len(bad_run) == 0:
        print('All the depths worked')
        
    else:
        open_bad = open('bad_report.txt','w')
        for bad in bad_run:
            open_bad.write('{},'.format(bad))
