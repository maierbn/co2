
import RPi.GPIO as GPIO
import time
import timeit
from DRV8825 import DRV8825

def turn_close(n_rotations=20):

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
		c = 3.01
		
		# fast start
		n_steps = 32*200*(n_rotations-3)
		duration = 1
		
		tstart = timeit.default_timer()
		Motor1.TurnStep(Dir='forward', steps=int(n_steps), stepdelay=duration/c/n_steps)
		tstop = timeit.default_timer()
		print(f"duration: {tstop-tstart} s")
		
		# slow end
		n_steps = 32*200*3
		duration = 10
		
		tstart = timeit.default_timer()
		Motor1.TurnStep(Dir='forward', steps=int(n_steps), stepdelay=duration/c/n_steps)
		Motor1.Stop()
		tstop = timeit.default_timer()
		
	except:
		# GPIO.cleanup()
		traceback.print_exc()
		print("\nException, Motor stop")
		Motor1.Stop()

def turn_open(n_rotations=20):
	
	try:
		Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
		
		Motor1.SetMicroStep('softward','fullstep')
		c = 3.01
	
	
		# slow start
		n_steps = 32*200*3
		duration = 10
		
		tstart = timeit.default_timer()
		Motor1.TurnStep(Dir='backward', steps=int(n_steps), stepdelay=duration/c/n_steps)
		tstop = timeit.default_timer()
		print(f"duration: {tstop-tstart} s")
		
		# fast end
		n_steps = 32*200*(n_rotations-3)
		duration = 1
		
		tstart = timeit.default_timer()
		Motor1.TurnStep(Dir='backward', steps=int(n_steps), stepdelay=duration/c/n_steps)
		Motor1.Stop()
		tstop = timeit.default_timer()
		
	except:
		# GPIO.cleanup()
		print("\nException: Motor stop")
		Motor1.Stop()
