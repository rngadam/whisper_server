
# Running

'''
gunicorn --timeout 60 -w 1 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:4000 server:app
'''
