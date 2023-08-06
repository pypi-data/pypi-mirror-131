print('OIUJHDGSSKIJUDHGLKDIS')
import sys
import os
fp = os.path.dirname(os.path.abspath( __file__ ))
fpp = os.path.join(fp, 'src')
print(fpp)

sys.path.insert(0 , fpp)

from walk_sftp import WalkSFTP
from walk_ftp import WalkFTP

def test_exists():
    assert WalkSFTP != None

def test_exists2():
    assert WalkFTP != None
