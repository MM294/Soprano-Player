import os, os.path, stat, time
from datetime import date, timedelta

fileFormats = {'.mp3','.ogg','.oga','.wma','.flac','.m4a','.mp4'}
dirsNotUsed = []

def getdirs(basedir, age):
    for root, dirs, files in os.walk(basedir):
        print "root =", root
        print "dirs =", dirs
        print "files =", files

        found = 1
        for file in files:
           found_file = datecheck(root, file, age)
           if not found_file :             #At least one file is not old enough
               found = 0

           """ or backup all of the files that are old enough
           if found_file:
              backup_list.append(os.path.join(root, file))
           """

        if found:
           archive(root, files)

def datecheck(root, file, age):
    basedate = date.today() - timedelta(days=age)
    fname = os.path.join(root, file)
    used = os.stat(fname).st_mtime    # st_mtime=modified, st_atime=accessed
    year, day, month = time.localtime(used)[:3]
    lastused = date(year, day, month)
    if lastused < basedate:             #Gets files older than (age) days
       return 1
    return 0                                  # Not old enough

def archive(root, files):
   for file in files:
      fname=os.path.join(root, file)
      print "archiving", fname

if __name__ == '__main__':
    basedir = raw_input('Choose directory to scan: ')
    age = raw_input('Only scan files older than... (days): ')
    getdirs(basedir, int(age))
