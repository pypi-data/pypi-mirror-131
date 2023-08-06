import os
from time import sleep
from template_flask.funcs import create_dir_and_venv, activate_venv_and_install_reqs


if __name__ == '__main__':

    TEST = True

    p_name = input('\nEnter the name of your project: ')
    p_path = os.getcwd()
    print('Starting creation of virtual environment and directory structure')

    create_dir_and_venv(p_name, p_path, test=TEST)
    print('Created virtual environment and directory structure')
    print('Starting installation of packages into virtual environment')
    activate_venv_and_install_reqs(p_name, p_path)

    print('Successfully Completed Setup')
    sleep(1)
