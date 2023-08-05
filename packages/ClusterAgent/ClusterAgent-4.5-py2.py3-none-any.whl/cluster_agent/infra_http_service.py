#!/usr/bin/evn python
# -*- coding: utf-8 -*-

"""Dell EMC Confidential: Restricted Internal Distribution
Copyright 2018-2020 Dell EMC, all rights reserved.
This software contains the intellectual property of Dell EMC or is
licensed to Dell EMC from third parties. Use of this software and
the intellectual property contained therein is expressly limited
to the terms and conditions of the License Agreement under which
it is provided by or on behalf of Dell EMC.


@package Initialization
@brief This file contains all generic attributes and functions for all kinds of test platforms.
@date 4/8/2021
@author Shuangshuang.Li@dell.com
@par Owner Shuangshuang.Li@dell.com
"""

import os
import socket
import logging
import shutil
import subprocess
import os.path
import sys
import time
from flask import Flask
from flask import request, Response
from flask import send_from_directory
from flask import stream_with_context
sys.path.append(os.path.join(os.path.dirname(__file__)))
from task_excution import RestartSvf, PhaseTwoStepLog, PhaseScriptLog, CollectLog, StartMultiSvf, \
    RunScriptTest, ExecuteDeviceTask

# Create flask instance
app = Flask(__name__)
service_version = "3.5"


@app.route("/check_service_ready", methods=["POST"])
def check_service_ready():
    """
    Check if service is ready
    """
    app.logger.info("Test PC of IP {} is ready".format(ip_local_pc))
    app.logger.info("Service version: {}".format(service_version))
    result = {"service_ready": True,
              "Test PC IP": ip_local_pc,
              "service_version": service_version,
              }

    return result


@app.route("/get_data", methods=["GET"])
def get_data():
    """
    Return get status
    """
    get_status = request.form.get("get_status")
    return get_status


@app.route("/get_base_code_path", methods=["POST"])
def get_base_code_path():
    global base_code_path, test_type, db_name, save_bin_path, db_type
    base_code_path = request.form.get("base_code_path")
    test_type = request.form.get("test_type")
    db_name = request.form.get("db_name")
    db_type = request.form.get("db_type")
    app.logger.info("Get base code path: {}".format(base_code_path))
    app.logger.info("Get cluster test type: {}".format(test_type))
    app.logger.info("Get mongoDB name: {}".format(db_name))
    app.logger.info("Get mongoDB type: {}".format(db_type))

    app.logger.info("Check FW bin path")
    save_bin_path = os.path.join(base_code_path, "cluster_bin_path")
    app.logger.info("FW bin path: {}".format(save_bin_path))
    if os.path.exists(save_bin_path):
        logging.info("Delete file {}".format(save_bin_path))
        shutil.rmtree(save_bin_path, ignore_errors=True)

    return "Get base code path {} successfully".format(base_code_path)


@app.route("/execute_script", methods=["POST"])
def execute_script():
    """
    execute test script
    """

    shell_command = request.form.get("shell_command")
    result_col = request.form.get("result_col")
    device_name = request.form.get("device_name")
    test_obj = request.form.get("test_obj")
    case = request.form.get("case")
    debug_mode = True if request.form.get("debug_mode", False) in ["True", True] else False
    app.logger.info('Shell Command: {}'.format(shell_command))
    app.logger.info('Input parameters: '
                    'result_col:{}, '
                    'device_name:{}, '
                    'test_obj:{}, '
                    'case:{}, '
                    'debug_mode:{}, '.format(result_col, device_name, test_obj, case, debug_mode))

    RunScriptTest(logger=app.logger,
                  db_name=db_name,
                  db_type=db_type,
                  result_col=result_col,
                  shell_command=shell_command,
                  device_name=device_name,
                  test_obj=test_obj,
                  case=case,
                  test_type=test_type,
                  base_code_path=base_code_path,
                  debug_mode=debug_mode).run_script()
    return "Run {} {} in device {} successfully".format(test_obj, case, device_name)


@app.route("/execute_device_task", methods=["POST"])
def execute_device_task():
    """
    execute device tasks
    """

    shell_command = request.form.get("shell_command")
    device_name = request.form.get("device_name")
    port_num = request.form.get("port_num")
    task_type = request.form.get("task_type")
    recover = request.form.get("recover")
    app.logger.info('Shell Command: {}'.format(shell_command))

    ExecuteDeviceTask(logger=app.logger,
                      db_name=db_name,
                      db_type=db_type,
                      shell_command=shell_command,
                      device_name=device_name,
                      port_num=port_num,
                      task_type=task_type,
                      recover=recover,
                      base_code_path=base_code_path).execute_task()

    return "Execute task {} in device {} successfully".format(task_type, device_name)


@app.route("/post_data", methods=["POST"])
def post_data():
    """
    Receive and execute two kind commands(shell command, OS command)
    """

    shell_command = request.form.get("shell_command")
    oscmd = request.form.get("oscmd")

    def generate():
        if shell_command is not None:
            app.logger.info('Shell Command: {}'.format(shell_command))
            subprocess.Popen(shell_command, shell=True)

        if oscmd is not None:
            try:
                if oscmd.split(':', 1)[0] == 'chdir':
                    os.chdir(oscmd.split(':', 1)[1])
                    yield 'os.chdir successfully!'
                elif oscmd.split(':', 1)[0] == 'mkdir':
                    os.makedirs(oscmd.split(':', 1)[1])
                    yield 'os.makedirs successfully!'
                elif oscmd.split(':', 1)[0] == 'rmdir':
                    shutil.rmtree(oscmd.split(':', 1)[1])
                    yield 'os.rmdir successfully!'
                elif oscmd.split(':', 1)[0] == 'remove':
                    os.remove(oscmd.split(':', 1)[1])
                    yield 'os.makedirs successfully!'
                elif oscmd.split(':', 1)[0] == 'system':
                    os.system(oscmd.split(':', 1)[1])
                    yield 'os system cmd successfully!'

            except IOError:
                yield 'Error: os.chdir fail!'

    return Response(stream_with_context(generate()), mimetype='text/plain')


@app.route("/download", methods=["GET"])
def download():
    """
    Send the data to client which is required
    """

    request_filename = request.args.get("filename")
    app.logger.info(request_filename)
    return send_from_directory('./temp/', filename=request_filename, as_attachment=True)


@app.route("/upload", methods=["POST"])
def upload():
    """
    Receive and save data from Client
    """
    file = request.files['file']

    if file.filename.split(".")[-1] in ['bin', "cap", "json"]:
        if not os.path.exists(save_bin_path):
            os.makedirs(save_bin_path)
        save_path = save_bin_path

    elif file.filename.split(".")[-1] == 'yaml':
        if file.filename.split(".")[0] == 'oakgate':
            save_path = os.path.join(base_code_path, "test-platform", "Config", "BasicConfig")
        else:
            save_path = os.path.join(base_code_path, "test-platform", "TestCaseSuite", "Redtail", "Regression_suite")

        if not os.path.exists(save_path):
            os.makedirs(save_path)
    else:
        save_path = './'

    app.logger.info("Will save the file {} to path {}".format(save_path, file.filename))
    file.save(os.path.join(save_path, file.filename))
    app.logger.info("Save the file {} to path {} done!!".format(save_path, file.filename))

    return save_path


@app.route("/get_test_status", methods=["POST"])
def get_test_status():
    """
    Get test script status and device status
    """
    script_name = request.form.get("script_name")
    device_name = request.form.get("device_name")
    app.logger.info("Try to phase script {} log which tests in device {}".format(script_name, device_name))
    if test_type == "DPI_test":
        test_script_status_dic = PhaseScriptLog(app.logger, test_type).parseResultDPI(base_code_path, script_name,
                                                                                      device_name)
    else:
        test_script_status_dic = PhaseScriptLog(app.logger, test_type).parseResult(base_code_path, script_name,
                                                                                   device_name)
    return test_script_status_dic


@app.route("/restart_svf_service", methods=["POST"])
def restart_svf_service():
    """
    Get test script status and device status
    """
    app.logger.info("Try to restart SVF service")
    cli_port = None
    rest_port = None
    try:
        cli_port, rest_port = RestartSvf(app.logger).re_start_svf()
    except Exception as e:
        app.logger.error(e)

    if rest_port != None:
        restart_svf_result = "success"
    else:
        restart_svf_result = "fail"

    result = {"restart_svf_result": restart_svf_result,
              "cli_port": cli_port,
              "rest_port": rest_port
              }
    return result


@app.route("/start_multi_svf", methods=["POST"])
def start_multi_svf():
    """
    This is function for satrt multi SVF GUI
    :return: result, details
    """

    app.logger.info("Try to start multi SVF GUI for test")
    cli_rest_port_list = []
    svf_num = int(request.form.get("svf_num"))
    try:
        cli_rest_port_list = StartMultiSvf(svf_num=svf_num, logger=app.logger).start_multi_svf_ports()
    except Exception as e:
        app.logger.error(e)

    if len(cli_rest_port_list) != 0:
        start_multi_svf_result = "success"
    else:
        start_multi_svf_result = "fail"

    result = {"start_multi_svf_result": start_multi_svf_result,
              "cli_rest_port_list": cli_rest_port_list,
              }
    return result


@app.route("/collect_script_logs", methods=["GET", "POST"])
def collect_script_logs():
    """
    collect script logs and UART logs
    """
    device_name = request.form.get("device_name")
    app.logger.info("Collect script logs in path {}, test device name {}"
                    .format(os.path.join(base_code_path, "test-platform", "Logs"), device_name))
    result, script_log_tar = CollectLog(app.logger, test_type).tar_script_file(base_code_path, device_name)
    if not result:
        messeage = "Tar and Copy script logs to share folder failed "
        app.logger.error(messeage)
        return messeage
    else:
        app.logger.info("Tar and Copy script logs to share folder successfully ")
        request_file_path, request_file_name = os.path.split(script_log_tar)

        return send_from_directory(request_file_path, filename=request_file_name, as_attachment=True)


@app.route("/collect_uart_logs", methods=["GET", "POST"])
def collect_uart_logs():
    """
    collect UART logs
    """
    device_name = request.form.get("device_name")
    app.logger.info("Collect UART logs in device {}, path {}".format(device_name,
                                                                     os.path.join(base_code_path, "test-platform",
                                                                                  "Logs", "UART_LOG")))
    result, script_log_tar = CollectLog(app.logger).tar_uart_file()
    if not result:
        app.logger.error("Tar and Copy UART logs to share folder failed ")
        return None
    else:
        app.logger.info("Tar and Copy UART logs to share folder successfully ")
        request_file_path, request_file_name = os.path.split(script_log_tar)

        return send_from_directory(request_file_path, filename=request_file_name, as_attachment=True)


@app.route("/get_file_list", methods=["POST"])
def get_file_list():
    """
    Get file list of specified source dir
    """

    file_path = request.form.get("file_path")
    log_file_dic = {}
    for root, dir_list, file_list in os.walk(os.path.join(base_code_path, file_path)):
        log_file_dic[root] = file_list
        print(log_file_dic)

    return log_file_dic


@app.route("/collect_2step_logs", methods=["GET", "POST"])
def collect_2step_logs():
    """
    collect two step download logs
    """
    source_dir = os.path.join("C:\\", "UART_LOG_Cluster", "Two_step_download_logs")

    device_name = request.form.get("device_name")
    file_name = request.form.get("file_name")
    app.logger.info("Collect two step download log {} in device {}, path {}".format(file_name, device_name, source_dir))
    if not os.path.exists(source_dir):
        logging.error("Target folder {} is not existing".format(source_dir))
        return None
    else:
        pathfile = os.path.join(source_dir, file_name)
        request_file_path, request_file_name = os.path.split(pathfile)
        app.logger.info("Transfer file {} successfully.".format(pathfile))
        return send_from_directory(request_file_path, filename=request_file_name, as_attachment=True)


def run():
    global base_code_path, base_code_path, test_type, db_name, db_type, app, ip_local_pc

    base_code_path = "C:\\shuang\\"
    base_code_path = None
    test_type = "common_test"  # DPI_test
    db_name = None
    db_type = "local"

    # Record the console output
    console_log_name = time.strftime('%Y%m%d-%H%M%S_', time.localtime(time.time())) + "console_output.log"
    console_log_folder = os.path.join(os.getcwd(), 'console_logs')

    if os.path.exists(console_log_folder) is False:
        os.makedirs(console_log_folder)
    console_log_path = os.path.join(console_log_folder, console_log_name)

    logging_format_str = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'
    logging_format = logging.Formatter(logging_format_str)

    logging.basicConfig(level=logging.INFO,
                        format=logging_format_str,
                        filename=console_log_path,
                        filemode="w")

    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(console_log_path, mode="a+", encoding='UTF-8')
    app.logger.addHandler(file_handler)

    if app.logger.handlers:
        for handler in app.logger.handlers:
            handler.setFormatter(logging_format)

    app.logger.info("Get IP address of this PC")
    ip_list1 = socket.getaddrinfo(socket.gethostname(), None)
    ip_list = map(lambda x: x[4][0], socket.getaddrinfo(socket.gethostname(), None))
    for ip_temp in ip_list:
        if "192.168." in ip_temp:
            ip_local_pc = ip_temp
            app.logger.info("Local PC private IP is {}".format(ip_temp))
            break

    # start this server
    app.logger.info("Start the services")
    app.logger.info("Service version: {}".format(service_version))
    app.run(port=4999, host=ip_local_pc, threaded=True, debug=1)

if __name__ == "__main__":

    """
    server running here
    """
    run()

    # base_code_path = "C:\\shuang\\"
    # save_bin_path = None
    # test_type = "common_test"  # DPI_test
    # db_name = None
    # db_type = "local"
    #
    # # Record the console output
    # console_log_name = time.strftime('%Y%m%d-%H%M%S_', time.localtime(time.time())) + "console_output.log"
    # console_log_folder = os.path.join(os.getcwd(), 'console_logs')
    #
    # if os.path.exists(console_log_folder) is False:
    #     os.makedirs(console_log_folder)
    # console_log_path = os.path.join(console_log_folder, console_log_name)
    #
    # logging_format_str = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'
    # logging_format = logging.Formatter(logging_format_str)
    #
    # logging.basicConfig(level=logging.INFO,
    #                     format=logging_format_str,
    #                     filename=console_log_path,
    #                     filemode="w")
    #
    # stream_handler = logging.StreamHandler()
    # app.logger.addHandler(stream_handler)
    #
    # file_handler = logging.FileHandler(console_log_path, mode="a+", encoding='UTF-8')
    # app.logger.addHandler(file_handler)
    #
    # if app.logger.handlers:
    #     for handler in app.logger.handlers:
    #         handler.setFormatter(logging_format)
    #
    # app.logger.info("Get IP address of this PC")
    # ip_list1 = socket.getaddrinfo(socket.gethostname(), None)
    # ip_list = map(lambda x: x[4][0], socket.getaddrinfo(socket.gethostname(), None))
    # for ip_temp in ip_list:
    #     if "192.168." in ip_temp:
    #         ip_local_pc = ip_temp
    #         app.logger.info("Local PC private IP is {}".format(ip_temp))
    #         break
    #
    # # start this server
    # app.logger.info("Start the services")
    # app.logger.info("Service version: {}".format(service_version))
    # app.run(port=4999, host=ip_local_pc, threaded=True, debug=1)
