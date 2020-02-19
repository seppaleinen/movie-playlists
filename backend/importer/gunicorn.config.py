import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = "9000000"
#check_config = True
access_log_format = '%(h)s %(r)s %(s)s %(a)s %(L)ss'
accesslog = "-"
errorlog = "-"
#loglevel = "debug"
proc_name = "movie_playlist_backend_importer"