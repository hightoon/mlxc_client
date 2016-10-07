#-*- coding=utf8 -*-

import time
import pika
import shutil
import os
import os.path
import sys

from ftplib import FTP

FTP_SVR = '112.74.68.197'
FTP_USR = 'ubuntu'
FTP_PAS = '12345678'

def retr_file_from_ftp(filepath):
    usr, passwd = FTP_USR, FTP_PAS
    ret = True
    path, filename = os.path.split(filepath)
    localfn = filename
    with open(localfn, 'wb') as lf:
        try:
            ftp = FTP(FTP_SVR, timeout=120)
            ftp.login(usr, passwd)
        except Exception as e:
            print e
            ret = False
        else:
            try:
              ftp.cwd(path)
              ftp.retrbinary('RETR ' + filename, lf.write)
            except Exception as e:
              print 'get pic failed ', e
              ret = False
            finally:
              ftp.close()
    if not ret:
        os.remove(localfn)
    return ret

credentials = pika.PlainCredentials('bc', 'bc123456')

connected = False
while not connected:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
               '112.74.68.197', 5672, '/', credentials=credentials))
        break
    except Exception as e:
        print 'connection to rabbit failed.', e
        time.sleep(2)
channel = connection.channel()

'''
channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
'''

channel.exchange_declare(exchange='dipuadmin',
                         type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
print queue_name

channel.queue_bind(exchange='dipuadmin',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %s" % body)
    if body.startswith('remove:'):
      folder, filename = body[7:].split('&&')
      if sys.platform.startswith('win'):
        filename = filename.decode('utf8').encode('gbk')
      print filename
      try:
        os.remove(os.path.join('static', folder, filename))
      except:
        print 'remove failed'
    else:
      folder, filepath = body.split('&&')
      path, filename = os.path.split(filepath)
      if retr_file_from_ftp(filepath):
        if sys.platform.startswith('win'):
          dest = filename.decode('utf8').encode('gbk')
        else:
          dest = filename
        print filename, dest
        try:
          shutil.move(filename, os.path.join('static', folder, dest))
        except shutil.Error as e:
          print 'failed to mv file'
          os.remove(filename)


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()