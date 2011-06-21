import os
__dirCache = {}

def listDir(directory, listHiddenFiles=False):
    """
        Return a list of tuples (filename, path) with the given directory content
        The dircache module sorts the list of files, and either it's not needed or it's not sorted the way we want
    """
    if directory in __dirCache: cachedMTime, list = __dirCache[directory]
    else:                       cachedMTime, list = None, None

    if os.path.exists(directory): mTime = os.stat(directory).st_mtime
    else:                         mTime = 0

    if mTime != cachedMTime:
        # Make sure it's readable
        if os.access(directory, os.R_OK | os.X_OK): list = os.listdir(directory)
        else:                                       list = []

        __dirCache[directory] = (mTime, list)

    return [(filename, os.path.join(directory, filename)) for filename in list if listHiddenFiles or filename[0] != '.']

def getDirContents(directory):
	directories = []
        mediaFiles  = []

	for (file, path) in listDir(directory, False):
		if os.path.isdir(path):
			directories.append(file)
		elif os.path.isfile(path):
                #if media.isSupported(file):
			mediaFiles.append(file)
	return (directories, mediaFiles)
################
#stuff below this is test stuff
################
root = '/home/mike'
folders, files = getDirContents(root)

dirtree = []

for f in range(0, len(folders)):
	dirtree.append([folders[f]])
	folders2, files2 = getDirContents(os.path.join(root + '/' + [folders[f]][0]))
	for g in range(0, len(folders2)):
		dirtree[f].append([folders2[g]])
print(dirtree)
	
