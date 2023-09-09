import os
import time
import shutil
import argparse

#
# Setup arguments so we can determine where the version if PICO firmware we want is...
#
parser = argparse.ArgumentParser( description='PICO Flasher' )
parser.add_argument( 'uf2_file_path',  metavar="UF2_FILE", type=str, help='Path to the UF2 file')

args = parser.parse_args()

uf2_file_path = args.uf2_file_path

def find_pico_device():
    """
        Look for the PICO, and if we find it return the path to the PICO.  Note that this function could be called
        once, and the path used forever.  This routine relies on the fact that the PICO will come in as RPI-RP2.  If this
        changes, we will have to change *how* we locate the PICO automatically.

        returns:
            A fully qualified path to the PICO device, or an empty string
    """
    output = ""
    cmd = "lsblk -o MOUNTPOINT | grep RPI-RP2"
    try:
        command = os.popen(cmd)
        output = command.read()
    except Exception as e:
        print (e)
    finally:
        command.close()

    return output.strip()

print( "Press Ctrl-C to exit - DO NOT TERMINATE while transfer is in progress!")

while True:
    device = find_pico_device()
    if os.path.exists( device ):
        print( 'PICO detected on ' + device )
        try:
            print( '    Writing firmware do not terminate!' )
            shutil.copy2(uf2_file_path, device )
            print( '    Firmware installed - Rebooting PICO' )
            time.sleep(2)
        except PermissionError:
            print( '    Permission Error:  Unable to copy firmware to PICO.  Please reconnect the PICO and try again.' )
        except FileNotFoundError:
            print( '    Error: UF2 file not found.  Please check the file location.' )
    else:
        print( 'Searching for PICO...' )

    time.sleep(5)
