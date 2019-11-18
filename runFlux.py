#/share/apps/python/3.7.2/bin/python
import os
import test
import sys
import subprocess
import numpy as np
import h5py
import itertools
from itertools import product
import time
from math import pi
import multiprocessing
from multiprocessing import Pool #  Process pool
from multiprocessing import sharedctypes
print('--->')
particle = sys.argv[1]
print('--->'+str(particle))

#kineticE1 = np.arange(10.0,50.1,1.0)
#kineticE2 = np.arange(55.0,100.1,5.0)
#kineticE3 = np.arange(200.0,1000.1,100.0)
#kineticE = np.hstack([kineticE1,kineticE2,kineticE3])

kineticE = np.arange(1.0,60.1,1.0)
latitude = np.arange(-18.0,18.1,1.0)
altitude = np.arange(0.0,120.1,1.0)

#print(str(latitude))
#print(str(altitude))
#print(str(kineticE))

tic = time.time()

paramlist = list(itertools.product(kineticE, latitude, altitude))
print('made the set of independent variables...')

_flux_ = np.ctypeslib.as_ctypes(np.empty((61,38,122)))
shared_array_flux = sharedctypes.RawArray(_flux_._type_, _flux_)
print('made the array to hold the flux...')

def calculateFlux(paramlist):
	#print ('starting child process with id:%d '% os.getpid())
	#print ('parent process:%d' % os.getppid())
	
	k_i = paramlist[0] # k_e
	l_j = paramlist[1] # lat
	a_k = paramlist[2] # alt
	
	if k_i <= 40.0:
		_ke = 9.0+k_i	# MeV
	elif k_i > 40.0 and k_i <= 50.0:
		_ke = 45.0+5.0*(k_i-40.0)	# MeV
	elif k_i > 50.0:
		_ke = 100.0*(k_i-50.0)	# MeV
	
	_lt = 5.0*l_j	# deg
	_ht = 0.5*a_k	# km
	
	tmp_flux = np.ctypeslib.as_array(shared_array_flux)
	fx = 0.0
	#print('--->'+str(particle)+'     '+str(k_i)+'     '+str(l_j)+'     '+str(akm))
	rc = subprocess.check_call("./FluxTest.sh %s %s %s %s %s %s" % (os.getppid(), os.getpid(), particle, _ke, _lt, _ht), shell=True)
	
	with open('flux_'+str(os.getppid())+'_'+str(os.getpid())+'.txt') as fd:
		for line in fd:
			fx = line
	print('->->-> '+str(_ke)+'     '+str(l_j)+'     '+str(_ht)+'     '+str(fx))
	os.remove('flux_'+str(os.getppid())+'_'+str(os.getpid())+'.txt')
	tmp_flux[int(k_i), int(l_j), int(a_k)] = float(fx)
print('distribute the jobs across workers...')
p = Pool()
result = p.map(calculateFlux, paramlist)
_flux_ = np.ctypeslib.as_array(shared_array_flux)

with h5py.File('CosmicNeutronFlux__1MeVto1GeV__180d_per_5d__60km_per_500m__grid1.hdf5','w') as hf:
	hf.create_dataset('flux_map',data=_flux_)
print('---x---')

