# Import dependencies
from flask import jsonify
import json, requests
from pathlib import Path
import os, sys, distro
from configparser import ConfigParser

# Import internal dependencies
from ..utilities import run_command, create_logger
from ..vault_support import read_secret
from .ssl_certificate import generate_self_signed_cert



################################################################################
# LOGGING FACILITY

LOGFILE = '/tmp/luksctl-api.log'
LOGGER_NAME = 'luksctl_api'
api_logger = create_logger(logfile=LOGFILE, name=LOGGER_NAME)



################################################################################
# NODES CLASSES

class master:


    def __init__(self, infrastructure_config, virtualization_type=None, node_list=None):

        self.infrastructure_config = infrastructure_config
        self.virtualization_type = virtualization_type
        self.node_list = node_list
        self.distro_id = distro.id()


    def get_infrastructure_config(self): return self.infrastructure_config
    def get_virtualization_type(self): return self.virtualization_type
    def get_node_list(self): return self.node_list


    def write_api_config(self, luks_cryptdev_file='/etc/luks/luks-cryptdev.ini'):

        config = ConfigParser()
        config.read(luks_cryptdev_file)
        # Remove luksctl_api section if written previously
        if 'luksctl_api' in config.sections():
            config.remove_section('luksctl_api')

        config.add_section('luksctl_api')
        api_config = config['luksctl_api']

        api_config['INFRASTRUCTURE_CONFIGURATION'] = self.infrastructure_config

        if self.virtualization_type != None:
            api_config['VIRTUALIZATION_TYPE'] = self.virtualization_type

        if self.node_list != None:
            api_config['WN_IPS'] = self.node_list

        with open(luks_cryptdev_file, 'w') as f:
            config.write(f)


    def write_systemd_unit_file(self, working_directory, environment_prefix, ssl,
                                user, group, CN='localhost', cert_file='/etc/luks/gunicorn-cert.pem',
                                expiration_days=3650, key_size=4096, key_file='/etc/luks/gunicorn-key.pem',
                                service_file='/etc/systemd/system/luksctl-api.service'):
        
        # Exit if command is not run as root
        if not os.geteuid() == 0:
            sys.exit('Error: write_systemd_unit_file must be run as root.')
        
        config = ConfigParser()
        config.optionxform = str
        
        config.add_section('Unit')
        config['Unit']['Description'] = 'Gunicorn instance to serve luksctl api server'
        config['Unit']['After'] = 'network.target'

        config.add_section('Service')
        config['Service']['User'] = user
        config['Service']['Group'] = group
        config['Service']['WorkingDirectory'] = working_directory
        config['Service']['Environment'] = f'"PATH={environment_prefix}/bin"'
        
        if ssl:
            generate_self_signed_cert(CN=CN, cert_file=cert_file, expiration_days=expiration_days, key_size=key_size, key_file=key_file)
            config['Service']['ExecStart'] = f'{environment_prefix}/bin/gunicorn --workers 2 --bind 0.0.0.0:5000 -m 007 --certfile={cert_file} --keyfile={key_file} app:master_app'
        else:
            config['Service']['ExecStart'] = f'{environment_prefix}/bin/gunicorn --workers 2 --bind 0.0.0.0:5000 -m 007 app:master_app'
        
        config.add_section('Install')
        config['Install']['WantedBy'] = 'multi-user.target'

        with open(service_file, 'w') as sf:
            config.write(sf)


    def get_status(self):

        status_command = 'sudo luksctl status'
        status, stdout, stderr = run_command(status_command)

        api_logger.debug(f'Volume status stdout: {stdout}')
        api_logger.debug(f'Volume status stderr: {stderr}')
        api_logger.debug(f'Volume status: {status}')

        if str(status) == '0':
            return jsonify({'volume_state': 'mounted' })
        elif str(status)  == '1':
            return jsonify({'volume_state': 'unmounted' })
        else:
            return jsonify({'volume_state': 'unavailable', 'output': stdout, 'stderr': stderr })


    def open(self, vault_url, wrapping_token, path, secret_key, secret_root):

        status_command = 'sudo luksctl status'
        status, stodut, stderr = exec_cmd(status_command)

        if str(status) == '0':
            return jsonify({'volume_state': 'mounted'})
        
        else:
            # Read passphrase from vault
            secret = read_secret(vault_url, wrapping_token, path, secret_key, secret_root)
            
            # Open volume
            open_command = f'printf "{secret}\n" | sudo luksctl open' 
            status, stdout, stderr = exec_cmd(command)

            api_logger.debug(f'Volume status stdout: {stdout}')
            api_logger.debug(f'Volume status stderr: {stderr}')
            api_logger.debug(f'Volume status: {status}')

            if str(status) == '0':
                if self.infrastructure_config == 'cluster':
                    self.nfs_restart()
                elif self.virtualization_type == 'docker':
                    self.docker_restart
                return jsonify({'volume_state': 'mounted' })

            elif str(status)  == '1':
                return jsonify({'volume_state': 'unmounted' })

            else:
                return jsonify({'volume_state': 'unavailable', 'output': stdout, 'stderr': stderr})


    def nfs_restart(self):

        api_logger.debug(f'Restarting NFS on: {self.distro_id}')

        if self.distro_id == 'centos':
            restart_command = 'sudo systemctl restart nfs-server'
        elif self.distro_id == 'ubuntu':
            restart_command = 'sudo systemctl restart nfs-kernel-server'
        else:
            restart_command = ''
        
        api_logger.debug(restart_command)

        status, stdout, stderr = run_command(restart_command)

        api_logger.debug(f'NFS status: {status}')
        api_logger.debug(f'NFS status stdout: {stdout}')
        api_logger.debug(f'NFS status stderr: {stderr}')

        if str(status) == '0':
            self.mount_nfs_on_wns()


    def mount_nfs_on_wns(self):

        for node in self.node_list:
            url = f'http://{node}:5000/luksctl_api_wn/v1.0/nfs-mount'
            response = requests.post(url, verify=False)
            response.raise_for_status()
            deserialized_response = json.loads(response.text)
            api_logger.debug(f'{node} NFS: {deserialized_response["nfs_state"]}')


    def docker_restart(self):

        restart_command = 'sudo systemctl restart docker'

        status, stdout, stderr = run_command(restart_command)

        api_logger.debug(f'Docker service status: {status}')
        api_logger.debug(f'Docker service stdout: {stdout}')
        api_logger.debug(f'Docker service stderr: {stderr}')



class wn:


    def __init__(self, nfs_mountpoint_list):

        self.nfs_mountpoint_list = nfs_mountpoint_list

    
    def write_api_config(self, luks_cryptdev_file='/etc/luks/luks-cryptdev.ini'):

        config = ConfigParser()
        config.read(luks_cryptdev_file)
        # Remove luksctl_api section if written previously
        if 'luksctl_api' in config.sections():
            config.remove_section('luksctl_api')

        config.add_section('luksctl_api')
        api_config = config['luksctl_api']

        api_config['NFS_MOUNTPOINT_LIST'] = json.dumps(self.nfs_mountpoint_list)

        with open(luks_cryptdev_file, 'w') as f:
            config.write(f)


    def write_systemd_unit_file(self, working_directory, environment_prefix, user,
                                group, service_file='/etc/systemd/system/luksctl-api.service'):
        
        # Exit if command is not run as root
        if not os.geteuid() == 0:
            sys.exit('Error: write_systemd_unit_file must be run as root.')
        
        config = ConfigParser()
        config.optionxform = str
        
        config.add_section('Unit')
        config['Unit']['Description'] = 'Gunicorn instance to serve luksctl api server'
        config['Unit']['After'] = 'network.target'

        config.add_section('Service')
        config['Service']['User'] = user
        config['Service']['Group'] = group
        config['Service']['WorkingDirectory'] = working_directory
        config['Service']['Environment'] = f'"PATH={environment_prefix}/bin"'
        config['Service']['ExecStart'] = f'{environment_prefix}/bin/gunicorn --workers 2 --bind 0.0.0.0:5000 -m 007 app:wn_app'
        
        config.add_section('Install')
        config['Install']['WantedBy'] = 'multi-user.target'

        with open(service_file, 'w') as sf:
            config.write(sf)


    def check_status(self):

        for mountpoint in self.nfs_mountpoint_list:
            api_logger.debug(f'{mountpoint}: {os.path.ismount(mountpoint)}')
            if not os.path.ismount(mountpoint):
                return False
        
        return True


    def get_status(self):

        api_logger.debug(self.nfs_mountpoint_list)
        if self.check_status():
            return jsonify({'nfs_state':'mounted'})
        else:
            return jsonify({'nfs_state':'unmounted'})


    def nfs_mount(self):

        if self.check_status():
            return jsonify({'nfs_state':'mounted'})
        
        mount_command = 'sudo mount -a -t nfs'

        api_logger.debug(mount_command)

        status, stdout, stderr = run_command(mount_command)

        api_logger.debug(f'NFS mount subprocess call status: {status}')
        api_logger.debug(f'NFS mount subprocess call stdout: {stdout}')
        api_logger.debug(f'NFS mount subprocess call stderr: {stderr}')

        return self.get_status()
