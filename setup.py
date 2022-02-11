#!/usr/bin/env python3
import logging
import subprocess
import sys
import importlib
import errno

log = logging.getLogger("setup")

def install_packages():
    """
    Desc.: This function try to install python packages listed in [packages].
           We can also ask UTF maintainer to help us install package in Docker as well,
           but they have to rebuild the image.
    input: None
    return:
    #1: boolean to indeciate the method works correct or not
    """
    packages = {"pyserial"}

    ret, installed_packages = get_install_packages()
    if ret == False:
        log.error(f"Get installed package list failed. return.")
        return False

    ret = True
    for package in packages:
        if __check_package_installed(package, installed_packages) == True:
            log.info(f"{package} is installed. Verify next.")
            continue
        log.info(f"{package} is not installed. Try to install it.")
        install_ret = __install(package)
        if install_ret != 0:
            ret = False
            log.info(f"{package} can not be installed. install_ret={install_ret}")
        else:
            log.info(f"{package} install success.")
    return ret

def __install(package, timeout = 30):
    """
    Desc.: Install the package via pip install command.
    input:
        package: the package name.
        timeout: the time for interrupting the command in case not to block by its subprocess.
    return:
    #1: the return code after process the command.
    """
    log.info(f"Install {package}...")
    retry = 5
    cmd = [sys.executable, '-m', 'pip', 'install', package]
    while retry > 0:
        try:
            p = subprocess.Popen(cmd, shell = False, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            out, err = p.communicate(timeout = 10)
            out = out.decode("utf-8")
            rcode = p.returncode
            if rcode == 0:
                log.info(f"Install {package} success.")
                return rcode
            else:
                log.error(f"Failed to install: {out}")

        except subprocess.SubprocessError as e:
            log.error(f"run {str(cmd)} triggered excpetion. {str(e)}")
            if type(e) == subprocess.TimeoutExpired:
                p.kill()
                out, err = p.communicate()
                out = out.decode("utf-8")
                log.error(f"stdout: {out}")
                rcode = errno.ETIME
            else:
                rcode = p.returncode
            if retry <= 0:
                return p.returncode

        retry = retry - 1
        log.info(f"Install {package} failed. retry: {retry}")
    return rcode

def __check_package_installed(package, installed_list):
    """
    Desc.: Just compare if the package is in the installed list
    input: None
    return:
    #1: boolean to indeciate if the package has been installed. True is installed.
    """
    if package in installed_list:
        return True
    return False

def get_install_packages():
    """
    Desc.: This function get python instllaed packages via pip freeze command.
           The major usage of this function is to check if the depent package has
           been installed to host PC or not.
    input: None
    return:
    #1: boolean to indeciate the method works correct or not
    #2: The installed package list
    """
    cmd = [sys.executable, '-m', 'pip', 'freeze']
    package_list = {}

    p = subprocess.Popen(cmd, shell = False, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    try:
        out, err = p.communicate(timeout = 10)
        rcode = p.returncode
        out = out.decode("utf-8")
        if rcode != 0:
            log.error(f"Failed to get installed package list {out}")
    except subprocess.SubprocessError as e:
        log.error(f"Got exception: {e}")
        if type(e) == subprocess.TimeoutExpired:
            p.kill()
            out, err = p.communicate()
            out = out.decode("utf-8")
            log.error(f"stdout: {out}")
            rcode = errno.ETIME
        else:
            rcode = p.returncode

    if rcode != 0:
        log.info(f"Failed to transfer device programmer to device: {rcode}.")
        return False, package_list

    installed_packages = out.split()

    for package in installed_packages:
        package_parse = package.split("==")
        package_list[package_parse[0]] = package_parse[1]
    return True, package_list
