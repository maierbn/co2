
import RPi.GPIO as GPIO
import time
import timeit
import numpy as np
import traceback
from DRV8825 import DRV8825

def turn_close(n_rotations=6):

	try:
		Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))

		"""
		# 1.8 degree: nema23, nema14
		# softward Control :
		# 'fullstep': A cycle = 200 steps
		# 'halfstep': A cycle = 200 * 2 steps
		# '1/4step': A cycle = 200 * 4 steps
		# '1/8step': A cycle = 200 * 8 steps
		# '1/16step': A cycle = 200 * 16 steps
		# '1/32step': A cycle = 200 * 32 steps
		"""
		
		Motor1.SetMicroStep('softward','fullstep')
		c = 2.32
		
		# fast start
		n_steps = int(32*200*(n_rotations))
		duration = 10
		
		tstart = timeit.default_timer()
		Motor1.TurnStep(Dir='forward', steps=int(n_steps), stepdelay=duration/c/n_steps)
		tstop = timeit.default_timer()
		print(f"duration: {tstop-tstart} s")
		
		# slow end
		if False:
			n_steps = int(32*200*0.3)
			duration = 15
		
			tstart = timeit.default_timer()
			Motor1.TurnStep(Dir='forward', steps=int(n_steps), stepdelay=duration/c/n_steps)
			Motor1.Stop()
			tstop = timeit.default_timer()
		Motor1.Stop()
		
	except:
		# GPIO.cleanup()
		traceback.print_exc()
		print("\nException, Motor stop")
		Motor1.Stop()

def turn_open(n_rotations=6):
	
	try:
		Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
		
		Motor1.SetMicroStep('softward','fullstep')
		c = 2.32
	
	
		# slow start
		tstart = timeit.default_timer()
		n_steps = 32*200*n_rotations
			
		n_steps_per_iteration = 100
		for step in range(0,n_steps,n_steps_per_iteration):
			
			stepdelay = 1e-4*(2.0-np.sin(step/n_steps*np.pi))
			print(f"{step} {stepdelay}")
			Motor1.TurnStep(Dir='backward', steps=int(n_steps_per_iteration),
						stepdelay=stepdelay)

		
		tstop = timeit.default_timer()
		print(f"duration: {tstop-tstart} s")
		Motor1.Stop()
		
	except:
		# GPIO.cleanup()
		print("\nException: Motor stop")
		Motor1.Stop()
		traceback.print_exc()
