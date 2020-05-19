""" Project settings file """

class Config(object):
	HOST = 'localhost'
	PORT = 5000
	THREADED = 'True'				# Allows multithreading.
	DEBUG = True					# Debug mode. Do not allow in production.
	SEND_FILE_MAX_AGE_DEFAULT = 0 	# Cache lifetime, in hours (0 - disable caching).
	MONGO_URI = "mongodb://heroku_b95q3p7j:56tnmhd9hh38u4htitc845sej9@ds145220.mlab.com:45220/heroku_b95q3p7j?retryWrites=false"
	MAPS_API = "8TRGpb7lMwAJ7WkzaYDirvvmrx932kcqM7zroFbK7r0"
