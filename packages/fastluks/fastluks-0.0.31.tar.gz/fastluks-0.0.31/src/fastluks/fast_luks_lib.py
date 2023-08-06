# Import dependencies
import logging
import random
from string import ascii_letters, digits, ascii_lowercase
import os
import sys
from pathlib import Path
from datetime import datetime
import re
import zc.lockfile
from configparser import ConfigParser

# Import internal dependencies
from .common import run_command
from .vault_support import write_secret_to_vault


################################################################################
# VARIABLES
alphanum = ascii_letters + digits
LOGFILE = '/tmp/fast_luks.log'
time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
now = datetime.now().strftime('-%b-%d-%y-%H%M%S')

# Get Distribution
# Ubuntu and centos currently supported
try:
    with open('/etc/os-release', 'r') as f:
        os_file = f.read()
        regex = r'\sID="?(\w+)"?\n'
        ID = re.search(regex, os_file).group()
        DISTNAME = 'ubuntu' if ID == 'ubuntu' else 'centos'
except FileNotFoundError:
    print("Not running a distribution with /etc/os-release available")



################################################################################
# FUNCTIONS

#____________________________________
# Intro banner
def intro():
    NEW_PWD = ''
    while not (re.search(r'\w', NEW_PWD) and re.search(r'\d', NEW_PWD)):
        NEW_PWD = ''.join([random.choice(alphanum) for i in range(8)])
    
    print('=========================================================')
    print('                      ELIXIR-Italy')
    print('               Filesystem encryption script\n')             
    print('A password with at least 8 alphanumeric string is needed')
    print("There's no way to recover your password.")
    print('Example (automatic random generated passphrase):')
    print(f'                      {NEW_PWD}\n')
    print('You will be required to insert your password 3 times:')
    print('  1. Enter passphrase')
    print('  2. Verify passphrase')
    print('  3. Unlock your volume\n')
    print('=========================================================')


#____________________________________
# Log levels:
# DEBUG
# INFO
# WARNING
# ERROR

# Check if loglevel is valid
def check_loglevel(loglevel):
    valid_loglevels = ['INFO','DEBUG','WARNING','ERROR']
    if loglevel not in valid_loglevels:
        raise ValueError(f'loglevel must be one of {valid_loglevels}')


# Echo function
def echo(loglevel, text):
    check_loglevel(loglevel)
    message = f'{loglevel} {time} {text}\n'
    print(message)
    return message


# Logs config
logging.basicConfig(filename=LOGFILE, filemode='a+', level=0, format='%(levelname)s %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


#____________________________________
# Lock/UnLock Section
def lock(LOCKFILE):

    # Start locking attempt
    try:
        lock = zc.lockfile.LockFile(LOCKFILE, content_template='{pid};{hostname}') # storing the PID and hostname in LOCKFILE
        return lock
    except zc.lockfile.LockError:
        # Lock failed: retrieve the PID of the locking process
        with open(LOCKFILE, 'r') as lock_file:
            pid_hostname = lock_file.readline()
            PID = re.search(r'^\s(\d+);', pid_hostname).group()
        echo('ERROR', f'Another script instance is active: PID {PID}')
        sys.exit(2)

    # lock is valid and OTHERPID is active - exit, we're locked!
    echo('ERROR', f'Lock failed, PID {PID} is active')
    echo('ERROR', f'Another fastluks process is active')
    echo('ERROR', f'If you are sure fastluks is not already running,')
    echo('ERROR', f'You can remove {LOCKFILE} and restart fastluks')
    sys.exit(2)


#____________________________________
def unlock(lock, LOCKFILE, do_exit=True, message=None):
    lock.close()
    os.remove(LOCKFILE)
    if do_exit:
        sys.exit(f'UNLOCK: {message}')


#____________________________________
def unlock_if_false(function_return, lock, LOCKFILE, message=None):
    if function_return == False:
        unlock(lock, LOCKFILE, message=message)


#____________________________________
def create_random_cryptdev_name():
    return ''.join([random.choice(ascii_lowercase) for i in range(8)])


#____________________________________
def info(device, cipher_algorithm, hash_algorithm, keysize, cryptdev, mountpoint, filesystem):
    echo('DEBUG', f'LUKS header information for {device}')
    echo('DEBUG', f'Cipher algorithm: {cipher_algorithm}')
    echo('DEBUG', f'Hash algorithm {hash_algorithm}')
    echo('DEBUG', f'Keysize: {keysize}')
    echo('DEBUG', f'Device: {device}')
    echo('DEBUG', f'Crypt device: {cryptdev}')
    echo('DEBUG', f'Mapper: /dev/mapper/{cryptdev}')
    echo('DEBUG', f'Mountpoint: {mountpoint}')
    echo('DEBUG', f'File system: {filesystem}')


#____________________________________
# Install cryptsetup
def install_cryptsetup(LOGFILE=None):
    if DISTNAME == 'ubuntu':
        echo('INFO', 'Distribution: Ubuntu. Using apt.')
        run_command('apt-get install -y cryptsetup pv', LOGFILE)
    else:
        echo('INFO', 'Distribution: CentOS. Using yum.')
        run_command('yum install -y cryptsetup-luks pv', LOGFILE)


#____________________________________
# Check cryptsetup installation
def check_cryptsetup():
    echo('INFO', 'Check if the required applications are installed...')
    
    _, _, dmsetup_status = run_command('type -P dmsetup &>/dev/null')
    if dmsetup_status != 0:
        echo('INFO', 'dmsetup is not installed. Installing...')
        if DISTNAME == 'ubuntu':
            run_command('apt-get install -y dmsetup')
        else:
            run_command('yum install -y device-mapper')
    
    _, _, cryptsetup_status = run_command('type -P cryptsetup &>/dev/null')
    if cryptsetup_status != 0:
        echo('INFO', 'cryptsetup is not installed. Installing...')
        install_cryptsetup(LOGFILE=LOGFILE)
        echo('INFO', 'cryptsetup installed.')


#____________________________________
# Passphrase Random generation
def create_random_secret(passphrase_length):
    return ''.join([random.choice(alphanum) for i in range(passphrase_length)])


#____________________________________
def end_encrypt_procedure(SUCCESS_FILE):
    # send signal to unclok waiting condition for automation software (e.g Ansible)
    with open(SUCCESS_FILE, 'w') as success_file:
        success_file.write('LUKS encryption completed.') # WARNING DO NOT MODFIFY THIS LINE, THIS IS A CONTROL STRING FOR ANSIBLE
    echo('INFO', 'SUCCESSFUL.')


#____________________________________
def end_volume_setup_procedure(SUCCESS_FILE):
    # send signal to unclok waiting condition for automation software (e.g Ansible)
    with open(SUCCESS_FILE,'w') as success_file:
        success_file.write('Volume setup completed.')
    echo('INFO', 'SUCCESSFUL.')


#____________________________________
def load_default_config(defaults_file='./defaults.conf'):
    global cipher_algorithm, keysize, hash_algorithm, device, cryptdev, mountpoint, filesystem, paranoid, non_interactive, foreground, luks_cryptdev_file, luks_header_backup

    if os.path.isfile(defaults_file):
        logging.info('Loading default configuration from defaults.conf')
        config = ConfigParser()
        config.read_file(open(defaults_file))
        defaults = config['defaults']
        cipher_algorithm = defaults['cipher_algorithm']
        keysize = defaults['keysize']
        hash_algorithm = defaults['hash_algorithm']
        device = defaults['device']
        cryptdev = defaults['cryptdev']
        mountpoint = defaults['mountpoint']
        filesystem = defaults['filesystem']
        paranoid = defaults['paranoid']
        non_interactive = defaults['non_interactive']
        foreground = defaults['foreground']
        luks_cryptdev_file = defaults['luks_cryptdev_file']
        luks_header_backup = defaults['luks_header_backup']


#____________________________________
# Read ini file
def read_ini_file(cryptdev_ini_file):
    config = ConfigParser()
    config.read_file(open(cryptdev_ini_file))
    luks_section = config['luks']
    return {key:luks_section[key] for key in luks_section}


#____________________________________
def check_passphrase(passphrase_length, passphrase, passphrase_confirmation):
    if passphrase_length == None:
        if passphrase == None:
            echo('ERROR', "Missing passphrase!")
            return False
        if passphrase_confirmation == None:
            echo('ERROR', 'Missing confirmation passphrase!')
            return False
        if passphrase == passphrase_confirmation:
            s3cret = passphrase
        else:
            echo('ERROR', 'No matching passphrases!')
            return False
    else:
            s3cret = create_random_secret(passphrase_length)
            return s3cret


################################################################################
# CLASSES

#____________________________________
class device:
    
    def __init__(self, device_name, cryptdev, mountpoint, filesystem):
        self.device_name = device_name
        self.cryptdev = cryptdev
        self.mountpoint = mountpoint
        self.filesystem = filesystem
    
    def check_vol(self):
        logging.debug('Checking storage volume.')

        # Check if a volume is already mounted to mountpoint
        if os.path.ismount(self.mountpoint):
            mounted_device, _, _ = run_command(f'df -P {self.mountpoint} | tail -1 | cut -d" " -f 1')
            logging.debug(f'Device name: {mounted_device}')

        else:
            # Check if device_name is a volume
            if Path(self.device_name).is_block_device():
                logging.debug(f'External volume on {self.device_name}. Using it for encryption.')
                if not os.path.isdir(self.mountpoint):
                    logging.debug(f'Creating {self.mountpoint}')
                    os.makedirs(self.mountpoint, exist_ok=True)
                    logging.debug(f'Device name: {self.device_name}')
                    logging.debug(f'Mountpoint: {self.mountpoint}')
            else:
                logging.error('Device not mounted, exiting! Please check logfile:')
                logging.error(f'No device mounted to {self.mountpoint}')
                run_command('df -h', LOGFILE=LOGFILE)
                return False # unlock and terminate process
    
    def is_encrypted(self):
        logging.debug('Checking if the volume is already encrypted.')
        devices, _, _ = run_command('lsblk -p -o NAME,FSTYPE')
        if re.search(f'{self.device_name}\s+crypto_LUKS', devices):
                logging.info('The volume is already encrypted')
                return True
        else:
            return False

    def umount_vol(self):
        logging.info('Umounting device.')
        run_command(f'umount {self.mountpoint}', LOGFILE=LOGFILE)
        logging.info(f'{self.device_name} umounted, ready for encryption!')

    def luksFormat(self, s3cret, cipher_algorithm, keysize, hash_algorithm):
        return run_command(f'printf "{s3cret}\n" | cryptsetup -v --cipher {cipher_algorithm} --key-size {keysize} --hash {hash_algorithm} --iter-time 2000 --use-urandom luksFormat {self.device_name} --batch-mode')

    def luksHeaderBackup(self, luks_header_backup_dir, luks_header_backup_file):
        return run_command(f'cryptsetup luksHeaderBackup --header-backup-file {luks_header_backup_dir}/{luks_header_backup_file} {self.device_name}')

    def luksOpen(self, s3cret):
        return run_command(f'printf "{s3cret}\n" | cryptsetup luksOpen {self.device_name} {self.cryptdev}')

    def setup_device(self, luks_header_backup_dir, luks_header_backup_file, cipher_algorithm, keysize, hash_algorithm,
                    passphrase_length, passphrase, passphrase_confirmation, use_vault, vault_url, wrapping_token, secret_path, user_key):
            echo('INFO', 'Start the encryption procedure.')
            logging.info(f'Using {cipher_algorithm} algorithm to luksformat the volume.')
            logging.debug('Start cryptsetup')
            info(self.device_name, cipher_algorithm, hash_algorithm, keysize, self.cryptdev, self.mountpoint, self.filesystem)
            logging.debug('Cryptsetup full command:')
            logging.debug('cryptsetup -v --cipher $cipher_algorithm --key-size $keysize --hash $hash_algorithm --iter-time 2000 --use-urandom --verify-passphrase luksFormat $device --batch-mode')

            s3cret = check_passphrase(passphrase_length, passphrase, passphrase_confirmation)
            if s3cret == False:
                return False # unlock and exit
            
            # Start encryption procedure
            self.luksFormat(s3cret, cipher_algorithm, keysize, hash_algorithm)

            # Write the secret to vault
            if use_vault:
                write_secret_to_vault(vault_url, wrapping_token, secret_path, user_key, s3cret)
                echo('INFO','Passphrase stored in Vault')

            # Backup LUKS header
            if not os.path.isdir(luks_header_backup_dir):
                os.mkdir(luks_header_backup_dir)
            _, _, luksHeaderBackup_ec = self.luksHeaderBackup(luks_header_backup_dir, luks_header_backup_file)

            if luksHeaderBackup_ec != 0:
                # Cryptsetup returns 0 on success and a non-zero value on error.
                # Error codes are:
                # 1 wrong parameters
                # 2 no permission (bad passphrase)
                # 3 out of memory
                # 4 wrong device specified
                # 5 device already exists or device is busy.
                logging.error(f'Command cryptsetup failed with exit code {luksHeaderBackup_ec}! Mounting {self.device_name} to {self.mountpoint} and exiting.')
                if luksHeaderBackup_ec == 2:
                    echo('ERROR', 'Bad passphrase. Please try again.')
                return False # unlock and exit

            return s3cret
    
    def open_device(self, s3cret):
        echo('INFO', 'Open LUKS volume')
        if not Path(f'/dev/mapper{self.cryptdev}').is_block_device():
            _, _, openec = self.luksOpen(s3cret)
            
            if openec != 0:
                if openec == 2:
                    echo('ERROR', 'Bad passphrase. Please try again.')
                    return False # unlock and exit
                else:
                    echo('ERROR', f'Crypt device already exists! Please check logs: {LOGFILE}')
                    logging.error('Unable to luksOpen device.')
                    logging.error(f'/dev/mapper/{self.cryptdev} already exists.')
                    logging.error(f'Mounting {self.device_name} to {self.mountpoint} again.')
                    run_command(f'mount {self.device_name} {self.mountpoint}', LOGFILE=LOGFILE)
                    return False # unlock and exit
    
    def encryption_status(self):
        logging.info(f'Check {self.cryptdev} status with cryptsetup status')
        run_command(f'cryptsetup -v status {self.cryptdev}', LOGFILE=LOGFILE)
    
    def create_cryptdev_ini_file(self, luks_cryptdev_file, cipher_algorithm, hash_algorithm, keysize, luks_header_backup_dir, luks_header_backup_file,
                                 save_passphrase_locally, s3cret, now=now):
        luksUUID, _, _ = run_command(f'cryptsetup luksUUID {self.device_name}')

        with open(luks_cryptdev_file, 'w') as f:
            f.write('# This file has been generated using fast_luks.sh script\n')
            f.write('# https://github.com/mtangaro/galaxycloud-testing/blob/master/fast_luks.sh\n')
            f.write('# The device name could change after reboot, please use UUID instead.\n')
            f.write('# LUKS provides a UUID (Universally Unique Identifier) for each device.\n')
            f.write('# This, unlike the device name (eg: /dev/vdb), is guaranteed to remain constant\n')
            f.write('# as long as the LUKS header remains intact.\n')
            f.write(f'# LUKS header information for {self.device_name}\n')
            f.write(f'# luks-{now}\n')

            config = ConfigParser()
            config.add_section('luks')
            config_luks = config['luks']
            config_luks['cipher_algorithm'] = cipher_algorithm
            config_luks['hash_algorithm'] = hash_algorithm
            config_luks['keysize'] = str(keysize)
            config_luks['device'] = self.device_name
            config_luks['uuid'] = luksUUID
            config_luks['cryptdev'] = self.cryptdev
            config_luks['mapper'] = f'/dev/mapper/{self.cryptdev}'
            config_luks['mountpoint'] = self.mountpoint
            config_luks['filesystem'] = self.filesystem
            config_luks['header_path'] = f'{luks_header_backup_dir}/{luks_header_backup_file}'
            if save_passphrase_locally:
                config_luks['passphrase'] = s3cret
                config.write(f)
                echo('INFO', f'Device informations and key have been saved in {luks_cryptdev_file}')
            else:
                config.write(f)
                echo('INFO', f'Device informations have been saved in {luks_cryptdev_file}')

        run_command(f'dmsetup info /dev/mapper/{self.cryptdev}', LOGFILE=LOGFILE)
        run_command(f'cryptsetup luksDump {self.device_name}', LOGFILE=LOGFILE)

    def wipe_data(self):
        echo('INFO', 'Paranoid mode selected. Wiping disk')
        logging.info('Wiping disk data by overwriting the entire drive with random data.')
        logging.info('This might take time depending on the size & your machine!')
        
        run_command(f'dd if=/dev/zero of=/dev/mapper/{self.cryptdev} bs=1M status=progress')
        
        logging.info(f'Block file /dev/mapper/{self.cryptdev} created.')
        logging.info('Wiping done.')

    def create_fs(self):
        echo('INFO', 'Creating filesystem.')
        logging.info(f'Creating {self.filesystem} filesystem on /dev/mapper/{self.cryptdev}')
        _, _, mkfs_ec = run_command(f'mkfs -t {self.filesystem} /dev/mapper/{self.cryptdev}', LOGFILE=LOGFILE)
        if mkfs_ec != 0:
            echo('ERROR', f'While creating {self.filesystem} filesystem. Please check logs.')
            echo('ERROR', 'Command mkfs failed!')
            return False # unlock and exit
    
    def mount_vol(self):
        echo('INFO', 'Mounting encrypted device.')
        logging.info(f'Mounting /dev/mapper/{self.cryptdev} to {self.mountpoint}')
        run_command(f'mount /dev/mapper/{self.cryptdev} {self.mountpoint}', LOGFILE=LOGFILE)
        run_command('df -Hv', LOGFILE=LOGFILE)

    def encrypt(self, cipher_algorithm, keysize, hash_algorithm, luks_header_backup_dir, luks_header_backup_file, 
               LOCKFILE, SUCCESS_FILE, luks_cryptdev_file, passphrase_length, passphrase, passphrase_confirmation,
               save_passphrase_locally, use_vault, vault_url, wrapping_token, secret_path, user_key):
        
        locked = lock(LOCKFILE) # Create lock file

        cryptdev = create_random_cryptdev_name() # Assign random name to cryptdev

        check_cryptsetup() # Check that cryptsetup and dmsetup are installed

        unlock_if_false(self.check_vol(), locked, LOCKFILE, message='Volume checks not satisfied') # Check which virtual volume is mounted to mountpoint, unlock and exit if it's not mounted

        if not self.is_encrypted(): # Check if the volume is encrypted, if it's not start the encryption procedure
            self.umount_vol()
            s3cret = self.setup_device(luks_header_backup_dir, luks_header_backup_file, cipher_algorithm, keysize, hash_algorithm,
                                       passphrase_length, passphrase, passphrase_confirmation, use_vault, vault_url, wrapping_token,
                                       secret_path, user_key)
            unlock_if_false(s3cret, locked, LOCKFILE, message='Device setup procedure failed.')
        
        unlock_if_false(self.open_device(s3cret), locked, LOCKFILE, message='luksOpen failed, mapping not created.') # Create mapping

        self.encryption_status() # Check status

        self.create_cryptdev_ini_file(luks_cryptdev_file, cipher_algorithm, hash_algorithm, keysize, luks_header_backup_dir,
                                      luks_header_backup_file, save_passphrase_locally, s3cret) # Create ini file

        end_encrypt_procedure(SUCCESS_FILE) # LUKS encryption finished. Print end dialogue.

        unlock(locked, LOCKFILE, do_exit=False) # Unlock
    
    def volume_setup(self, cipher_algorithm, hash_algorithm, keysize, luksUUID, luks_header_backup_dir,
                     luks_header_backup_file, LOCKFILE, SUCCESS_FILE):
        
        locked = lock(LOCKFILE) # Create lock file

        unlock_if_false(self.create_fs(), locked, LOCKFILE, message='Command mkfs failed.') # Create filesystem

        self.mount_vol() # Mount volume
        
        end_volume_setup_procedure(SUCCESS_FILE) # Volume setup finished. Print end dialogue

        unlock(locked, LOCKFILE, do_exit=False) # Unlock once done


################################################################################
# MAIN SCRIPT FUNCTION

def main_script(device_name='/dev/vdb', cryptdev='crypt', mountpoint='/export', filesystem='ext4',
                cipher_algorithm='aes-xts-plain64', keysize=256, hash_algorithm='sha256', luks_header_backup_dir='/etc/luks',
                luks_header_backup_file='luks-header.bck', luks_cryptdev_file='/etc/luks/luks-cryptdev.ini',
                passphrase_length=8, passphrase=None, passphrase_confirmation=None, save_passphrase_locally=None,
                use_vault=False, vault_url=None, wrapping_token=None, secret_path=None, user_key=None):
    
    if not os.geteuid() == 0:
        sys.exit('Error: Script must be run as root.')

    device_to_encrypt = device(device_name, cryptdev, mountpoint, filesystem)
    
    LOCKFILE = '/var/run/fast-luks-encryption.lock'
    SUCCESS_FILE = '/var/run/fast-luks-encryption.success'
    
    device_to_encrypt.encrypt(cipher_algorithm, keysize, hash_algorithm, luks_header_backup_dir, luks_header_backup_file, 
                              LOCKFILE, SUCCESS_FILE, luks_cryptdev_file, passphrase_length, passphrase, passphrase_confirmation,
                              save_passphrase_locally, use_vault, vault_url, wrapping_token, secret_path, user_key)

    cryptdev_variables = read_ini_file(luks_cryptdev_file)
    luksUUID = cryptdev_variables['uuid']
    LOCKFILE = '/var/run/fast-luks-volume-setup.lock'
    SUCCESS_FILE = '/var/run/fast-luks-volume-setup.success'

    device_to_encrypt.volume_setup(cipher_algorithm, hash_algorithm, keysize, luksUUID, luks_header_backup_dir,
                        luks_header_backup_file, LOCKFILE, SUCCESS_FILE)