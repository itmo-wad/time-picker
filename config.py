""" Project settings file """

class Config(object):
	HOST = 'localhost'
	PORT = 5000
	THREADED = 'True'				# Allows multithreading.
	DEBUG = True					# Debug mode. Do not allow in production.
	SEND_FILE_MAX_AGE_DEFAULT = 0 	# Cache lifetime, in hours (0 - disable caching).