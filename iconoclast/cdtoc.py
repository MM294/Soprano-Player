import sys
import os
from fcntl import ioctl
import struct
import cdrom
from CDROM import *

# ---
fd = cdrom.open('/dev/cdrom', os.O_RDONLY)
# ---

tochdr_fmt = 'BB'

tochdr = struct.pack(tochdr_fmt, 0, 0)
tochdr = ioctl(fd, CDROMREADTOCHDR, tochdr)
start, end = struct.unpack(tochdr_fmt, tochdr)

#---

tocentry_fmt = 'BBBix'
addr_fmt = 'BBB' + 'x' * (struct.calcsize('i') - 3)

for trnum in range(start, end + 1) + [CDROM_LEADOUT]:
    tocentry = struct.pack(tocentry_fmt, trnum, 0, CDROM_MSF, 0)   
    tocentry = ioctl(fd, CDROMREADTOCENTRY, tocentry)

    track, adrctrl, format, addr = struct.unpack(tocentry_fmt, tocentry)
    minute, second, fraction = struct.unpack(addr_fmt, struct.pack('i', addr))

    print "%3d: %2d:%02d.%02d" \
          % (track, minute, second, fraction)

print "Disc length:", str(minute) + ":" + str(second) + "." + str(fraction)

#---
