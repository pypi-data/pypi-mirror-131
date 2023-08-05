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
import getpass
import json
import subprocess
import tarfile
import datetime
import logging
import os
import re
import time
import pandas as pd
from sshtunnel import SSHTunnelForwarder
from pymongo import MongoClient, errors


class RunScriptTest(object):
    """
    Class for execute script and upload test result to database
    """

    def __init__(self, logger=None, db_name=None, db_type="local", result_col=None, shell_command=None,
                 device_name=None, test_obj=None,
                 case=None, test_type=None, base_code_path=None, debug_mode=False):
        self.logger = logger if logger else logging
        self.database_lib = ConnectDataBase(logger=self.logger, db_name=db_name, db_type=db_type)
        self.result_col = result_col
        self.shell_command = shell_command
        self.device_name = device_name
        # self.test_obj = test_obj
        self.script_name = case
        self.test_type = test_type
        self.base_code_path = base_code_path
        self.debug_mode = debug_mode
        self.exit_code_dic = {
            0: ["succeed", "Execute test succeed"],
            1: ["failed", "Execute test failed"],
            -1: ["skip", "Execute test skipped"],
            10: ["un_healthy", "Device Unhealthy"],
            100: ["script_exception", "Execute script error"],
        }

    def exit_state(self, exit_code):
        if exit_code in self.exit_code_dic.keys():
            return self.exit_code_dic[exit_code]
        else:
            return self.exit_code_dic[100]

    def run_script(self, update_result_2db=True):
        self.logger.info("Test start: test device: {}, test script: {}".format(self.device_name, self.script_name))

        result_dic = {"device": self.device_name,
                      "test_start_time": time.time(),
                      "result": "running"
                      }

        self.database_lib.update_data(update_condition={"_id": self.script_name},
                                      updata_info={self.result_col: result_dic},
                                      collection_name="execute_scripts_status",
                                      update_one=True)

        self.database_lib.update_data(update_condition={"_id": self.device_name},
                                      updata_info={"status": "busy", "test_obj": self.script_name},
                                      collection_name="execute_devices_status",
                                      update_one=True)

        try:
            out_bytes = subprocess.check_output(self.shell_command, shell=True)
            # out_text = out_bytes.decode('utf-8')
            # subprocess.Popen(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            output_msg = e.output.decode('utf-8')  # Output generated before error
            exit_code = e.returncode  # Return code
            if exit_code == 10:
                output_msg = "Device is not healthy, skip test"
        else:
            output_msg = "Test complete successfully"
            exit_code = 0

        self.logger.info("Test script result: {}, "
                         "description: {}, "
                         "exit code: {}\n "
                         "message: {}".format(self.exit_state(exit_code=exit_code)[0],
                                              self.exit_state(exit_code=exit_code)[1],
                                              exit_code,
                                              output_msg))

        self.exit_state(exit_code=exit_code)
        self.logger.info("Messages: {}".format(output_msg))

        if update_result_2db:
            test_exit_status = {
                "Test_complete_status": self.exit_state(exit_code=exit_code)[0],
                "description": self.exit_state(exit_code=exit_code)[1],
                "exit_code": exit_code,
                "messages": output_msg
            }

            self.update_test_status_to_db(test_exit_status=test_exit_status)

    def update_test_status_to_db(self, test_exit_status):

        self.logger.info(
            "Try to phase script {} log which tests in device {}".format(self.script_name, self.device_name))
        if self.test_type == "DPI_test":
            test_script_status_dic = PhaseScriptLog(self.logger, self.test_type).parseResultDPI(self.base_code_path,
                                                                                                self.script_name,
                                                                                                self.device_name)
        else:
            test_script_status_dic = PhaseScriptLog(self.logger, self.test_type).parseResult(self.base_code_path,
                                                                                             self.script_name,
                                                                                             self.device_name)
        if test_script_status_dic["log_generate"] is True:
            result_dic = {}
            try:
                result_dic = {
                    "device": self.device_name,
                    "FW_version": test_script_status_dic["result_detail"]["FW_version"],
                    "start_time": test_script_status_dic["result_detail"]["start_time"],
                    "end_time": test_script_status_dic["result_detail"]["end_time"],
                    "execution_time": test_script_status_dic["result_detail"]["execution_time"],
                    "result": test_script_status_dic["result_detail"]["result"],
                    "test_exit_status": test_exit_status
                }
            except Exception as e:
                self.logger.info("Get script log details failed.")
                self.logger.error(e)
            else:
                self.logger.info("Get script log details script: {}, device: {}\n Result: {}."
                                 .format(self.script_name, self.device_name, result_dic))

            if test_script_status_dic["result_detail"]["result"] == "Hung" or test_exit_status["exit_code"] == 10:

                self.database_lib.update_data(
                    update_condition={"_id": self.device_name, "result_col": self.result_col},
                    updata_info={"status": "hung"},
                    collection_name="execute_devices_status",
                    update_one=False)

                self.database_lib.update_data(
                    update_condition={"status": "backup", "result_col": self.result_col},
                    updata_info={"status": "ready"},
                    collection_name="execute_devices_status",
                    update_one=True)

                self.database_lib.update_data(update_condition={"_id": self.script_name},
                                              updata_info={self.result_col: "not run"},
                                              collection_name="execute_scripts_status",
                                              update_one=True)

            elif self.debug_mode and test_script_status_dic["result_detail"]["result"] == "Fail":

                self.database_lib.update_data(update_condition={"_id": self.device_name},
                                              updata_info={"status": "hung"},
                                              collection_name="execute_devices_status",
                                              update_one=True)

                self.database_lib.update_data(update_condition={"_id": self.script_name},
                                              updata_info={self.result_col: result_dic},
                                              collection_name="execute_scripts_status",
                                              update_one=True)

                self.logger.info("Script failed and debug mode is enabled, keep failure scene")
                self.logger.info("Test Script {} Done, test device: {}, result: {}"
                                 .format(self.script_name, self.device_name,
                                         test_script_status_dic["result_detail"]["result"]))
            else:
                self.database_lib.update_data(update_condition={"_id": self.device_name},
                                              updata_info={"status": "ready"},
                                              collection_name="execute_devices_status",
                                              update_one=True)

                self.database_lib.update_data(update_condition={"_id": self.script_name},
                                              updata_info={self.result_col: result_dic},
                                              collection_name="execute_scripts_status",
                                              update_one=True)

                self.logger.info("Test Script {} Done, test device: {}, result: {}"
                                 .format(self.script_name, self.device_name,
                                         test_script_status_dic["result_detail"]["result"]))
        else:

            self.logger.info("Device {} hung, test {} not start".format(self.device_name, self.script_name))
            self.database_lib.update_data(update_condition={"_id": self.device_name},
                                          updata_info={"status": "hung"},
                                          collection_name="execute_devices_status",
                                          update_one=True)

            self.database_lib.update_data(
                update_condition={"status": "backup", "result_col": self.result_col},
                updata_info={"status": "ready"},
                collection_name="execute_devices_status",
                update_one=True)

            self.database_lib.update_data(update_condition={"_id": self.script_name},
                                          updata_info={self.result_col: "not run"},
                                          collection_name="execute_scripts_status",
                                          update_one=True)

            self.logger.info(
                "Script {} test failed in test env init, device {} hung, re-run this script"
                    .format(self.script_name, self.device_name))


class ExecuteDeviceTask(object):
    """
    Class for execute script and upload test result to database
    """

    def __init__(self, logger=None, db_name=None, db_type="local", shell_command=None, device_name=None, port_num=None,
                 task_type=None,
                 base_code_path=None, recover=False):
        self.logger = logger if logger else logging
        self.database_lib = ConnectDataBase(logger=self.logger, db_name=db_name, db_type=db_type)
        self.shell_command = shell_command
        self.device_name = device_name
        self.port_num = port_num
        self.task_type = task_type
        self.base_code_path = base_code_path
        self.recover = recover

        bin_list = [os.path.join(os.path.join(self.base_code_path, "cluster_bin_path"), bin_temp)
                    for bin_temp in os.listdir(os.path.join(self.base_code_path, "cluster_bin_path"))]
        self.image2 = [para for para in bin_list if "Redtail_DownloadFile_ALL" in para][0]

    def execute_task(self):
        if self.task_type == "fw_download":
            self.task_fw_download(timeout=1500)
        elif self.task_type == "fill_drive":
            self.task_fill_drive(timeout=3000)
        elif self.task_type == "basic_feature_check":
            self.task_basic_feature_check(timeout=600)
        elif self.task_type == "post_two_step_tasks":
            self.task_post_two_step_tasks(timeout=60)

    def execute_shell_cmd(self, shell_cmd=None, timeout=None):
        if not shell_cmd:
            shell_cmd = self.shell_command
        try:
            out_bytes = subprocess.check_output(shell_cmd, timeout=timeout, shell=True)
            # out_bytes = subprocess.check_output(shell_cmd, shell=True)
            # out_text = out_bytes.decode('utf-8')
            # subprocess.Popen(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            output_msg = "[ERROR]CallError ：" + e.output.decode('utf-8')  # Output generated before error
            exit_code = e.returncode  # Return code
        except subprocess.TimeoutExpired as e:
            output_msg = "[ERROR]Timeout : " + str(e)
            exit_code = 100
        except Exception as e:
            output_msg = "[ERROR]Unknown Error : " + str(e)
            exit_code = 200
        else:
            output_msg = "Task {} complete successfully".format(self.task_type)
            exit_code = 0

        task_execute_status = {
            "exit_code": exit_code,
            "messages": output_msg
        }
        self.logger.info("exit code: {}\n "
                         "message: {}".format(exit_code, output_msg))
        return task_execute_status

    def task_fill_drive(self, timeout=3000):
        self.database_lib.update_data(update_condition={"_id": self.device_name},
                                      updata_info={"fill_drive_result": "fill drive ongoing"},
                                      collection_name="execute_devices_status",
                                      update_one=True)

        test_script_list = ["tc_datapath_512lba_seq_r0_w100_bs128k_qd32.py",
                            "tc_datapath_512lba_random_r0_w100_bs8k_qd128.py"]

        for test_script_temp in test_script_list:
            shell_cmd = "py -3 run.py --script {} --oakgate {}  --io_duration 2700  --image2 {}  --recover" \
                .format(test_script_temp, self.device_name, self.image2)

            os.chdir(os.path.join(self.base_code_path, "test-platform"))
            task_execute_status = self.execute_shell_cmd(shell_cmd, timeout=timeout)
            if task_execute_status["exit_code"] != 0:
                self.logger.info("For device {}, fill drive failed".format(self.device_name))
                self.database_lib.update_data(update_condition={"_id": self.device_name},
                                              updata_info={"fill_drive_result": "Fail", "status": "hung"},
                                              collection_name="execute_devices_status",
                                              update_one=True)
                return

        self.database_lib.update_data(update_condition={"_id": self.device_name},
                                      updata_info={"fill_drive_result": "Succeed"},
                                      collection_name="execute_devices_status",
                                      update_one=True)

    def task_basic_feature_check(self, timeout=600):
        self.database_lib.update_data(update_condition={"_id": self.device_name},
                                      updata_info={"basic_feature_check_result": "basic feature check ongoing"},
                                      collection_name="execute_devices_status",
                                      update_one=True)

        shell_cmd = "py -3 run.py --script tc_device_healthy_check.py --oakgate {} --image2 {} --recover" \
            .format(self.device_name, self.image2)
        os.chdir(os.path.join(self.base_code_path, "test-platform"))

        task_execute_status = self.execute_shell_cmd(shell_cmd, timeout=timeout)
        if task_execute_status["exit_code"] != 0:
            self.logger.info("For device {}, basic feature failed".format(self.device_name))
            self.database_lib.update_data(update_condition={"_id": self.device_name},
                                          updata_info={"basic_feature_check_result": "Fail", "status": "hung"},
                                          collection_name="execute_devices_status",
                                          update_one=True)
        else:
            self.database_lib.update_data(update_condition={"_id": self.device_name},
                                          updata_info={"basic_feature_check_result": "Succeed"},
                                          collection_name="execute_devices_status",
                                          update_one=True)

    def task_post_two_step_tasks(self, timeout=60):
        self.database_lib.update_data(update_condition={"_id": self.device_name},
                                      updata_info={"post_two_step_tasks_result": "post two step tasks ongoing"},
                                      collection_name="execute_devices_status",
                                      update_one=True)

        shell_cmd = "py -3 run.py --script u_post_two_step_tasks.py --oakgate {}".format(self.device_name)
        os.chdir(os.path.join(self.base_code_path, "test-platform"))

        task_execute_status = self.execute_shell_cmd(shell_cmd, timeout=timeout)
        if task_execute_status["exit_code"] != 0:
            self.logger.info("For device {}, post two step tasks failed".format(self.device_name))
            self.database_lib.update_data(update_condition={"_id": self.device_name},
                                          updata_info={"post_two_step_tasks_result": "Fail"},
                                          collection_name="execute_devices_status",
                                          update_one=True)
        else:
            self.database_lib.update_data(update_condition={"_id": self.device_name},
                                          updata_info={"post_two_step_tasks_result": "Succeed"},
                                          collection_name="execute_devices_status",
                                          update_one=True)

    def task_fw_download(self, timeout=900):
        start_time = time.time()
        expect_completion_time = timeout  # 15 mins
        self.logger.info("Expect fw download will complete in {} mins".format(expect_completion_time // 60))

        self.database_lib.update_data(update_condition={"_id": self.device_name},
                                      updata_info={"status": "FW download ongoing"},
                                      collection_name="execute_devices_status",
                                      update_one=True)

        p = subprocess.Popen(self.shell_command, shell=True)

        while time.time() - start_time <= expect_completion_time:
            two_step_result_dic = PhaseTwoStepLog(self.logger).parse_two_step_status(self.device_name)

            two_step_result = two_step_result_dic["two_step_result"]
            result_line = two_step_result_dic["result_line"]
            self.logger.info("For test device {}, test status: {}\n result line: {}"
                             .format(self.device_name, two_step_result, result_line))

            task_execute_status = {
                "two_step_result": two_step_result,
                "result_line": result_line
            }

            self.database_lib.update_data(update_condition={"_id": self.device_name},
                                          updata_info={"fw_download_info": task_execute_status},
                                          collection_name="execute_devices_status",
                                          update_one=True)

            if two_step_result == "completed":
                self.database_lib.update_data(update_condition={"_id": self.device_name},
                                              updata_info={"status": "ready", "fw_download_info": task_execute_status},
                                              collection_name="execute_devices_status",
                                              update_one=True)
                break
            time.sleep(1 * 60)
            self.logger.info("2step download have run {} min".format((time.time() - start_time) // 60))

        # check if two step download has completed
        if p.poll() is None:
            p.kill()
        else:
            self.logger.info("Two step download for device {} completed".format(self.device_name))

        if self.recover:
            self.database_lib.update_data(update_condition={"_id": self.device_name, "status": "FW download ongoing"},
                                          updata_info={"status": "ready",
                                                       "fw_download_info.two_step_result": "two step failed"},
                                          collection_name="execute_devices_status",
                                          update_one=True)
            self.logger.warning(
                "Since some drives didn't complete two step download, will try to recover in test step")
            self.logger.info("Device status: {}".format(
                self.database_lib.export_db_to_df(collection_name="execute_devices_status")))

        else:
            self.database_lib.update_data(update_condition={"_id": self.device_name, "status": "FW download ongoing"},
                                          updata_info={"status": "hung",
                                                       "fw_download_info.two_step_result": "two step failed"},
                                          collection_name="execute_devices_status",
                                          update_one=True)


class PhaseTwoStepLog(object):

    def __init__(self, logger=None):
        self.logger = logger if logger else logging
        self.two_step_log_path = os.path.join("C:\\", "UART_LOG_Cluster", "Two_step_download_logs")

    def parse_two_step_status(self, device_name):
        two_step_result = "running"
        result_line = ""
        self.logger.info("Try to get two step download log: {}".format(self.two_step_log_path))
        try:
            for root, dir, files in os.walk(self.two_step_log_path):
                for file in files:
                    if device_name + "-" in file:
                        with open(os.path.join(self.two_step_log_path, file),
                                  "r", encoding='utf8') as two_step_log:
                            lines = two_step_log.readlines()
                            lines.reverse()
                            for line in lines[0:30]:
                                result_line = line
                                if "Two step download complete state:" in result_line:
                                    two_step_result = "completed"
                                    break
                                else:
                                    two_step_result = "running"
                                    result_line = lines[0]
        except Exception as e:
            self.logger.error(e)

        return {"two_step_result": two_step_result,
                "result_line": result_line}


class RestartSvf(object):

    def __init__(self, logger=None):
        self.logger = logger if logger else logging

    def get_svf_service_ports_windows(self):
        self.logger.info("Try to get SVF service ports")
        cli_service_port_list = [7779, 7879, 7979, 8079, 8179, 8279, 8379, 8479, 8579, 8679, 8779, 8879, 8979, 9079]
        rest_service_port_list = [9998, 9999, 10000, 10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009,
                                  10010, 10011]

        chk_ps_cmd_str = "tasklist.exe -V -FI \"IMAGENAME EQ java.exe\""
        cmd_run = subprocess.Popen(args=chk_ps_cmd_str, stdout=subprocess.PIPE)
        output_lines = cmd_run.stdout.readlines()
        # output_lines = [line for line in output_lines if "OakGate Technology Validation Framework" in line]
        output_lines = [line for line in output_lines if b"OakGate Enduro powered by SVF Pro" in line]
        if not output_lines:
            return None, None
        else:
            pid = output_lines[0].strip().split()[1]
        chkPortCmdStr = "netstat -ano -p TCP"
        cmd_run = subprocess.Popen(args=chkPortCmdStr, stdout=subprocess.PIPE)
        output_lines = cmd_run.stdout.readlines()
        listeningList = [line.strip().split() for line in output_lines if b"LISTENING" in line]
        portList = [int(localAddr.split(b":")[-1]) for _, localAddr, _, _, portPid in listeningList if portPid == pid]
        cli_portList = [port for port in portList if port in cli_service_port_list]
        rest_portList = [port for port in portList if port in rest_service_port_list]
        if not cli_portList:
            cli_port = None
        elif len(cli_portList) == 1:
            cli_port = cli_portList[0]
        else:
            raise EnvironmentError("cli_portList have multi port, please check that %s" % cli_portList)
        if not rest_portList:
            rest_port = None
        elif len(rest_portList) == 1:
            rest_port = rest_portList[0]
            self.logger.info("Get SVF service ports successfully")
        else:
            raise EnvironmentError("rest_portList have multi port, please check that %s" % rest_portList)
        return cli_port, rest_port

    def init_svf_ctrl_path(self):
        """
        Init oakgate controller path(svf software)
        :return:
        """
        controller_path = None
        pc_user_name = getpass.getuser()
        oakgate_root_path_list = [r"C:\Users\{}\OakGate".format(pc_user_name), r"C:\Program Files (x86)\OakGate",
                                  r"C:\Program Files\OakGate"]

        for oakgate_absolute_path in oakgate_root_path_list:
            if os.path.isdir(oakgate_absolute_path):
                latest_oakgate_version_num = max(
                    re.findall(r"Enduro-v[0-9]+\.[0-9]+\.[0-9]", str(os.listdir(oakgate_absolute_path))))
                controller_path = os.path.join(oakgate_absolute_path, latest_oakgate_version_num, "ApplicationUIBundle")

                self.logger.info("Oakgate controller path: {}".format(controller_path))
                break
        if not controller_path:
            raise Exception("SVF path is not exist, please start SVF manually")

        return controller_path

    def start_svf(self):
        controller_path = self.init_svf_ctrl_path()
        startDir = os.getcwd()
        if os.path.isdir(controller_path):
            pass
        else:
            raise Exception("SVF path is not exist")
        os.chdir(os.path.join(controller_path, 'bin'))
        bat_path = os.path.join(controller_path, 'bin', 'call_oakgate.bat')
        if os.path.exists(bat_path):
            pass
        else:
            self.logger.info("create")
            with open(bat_path, 'w+') as f:
                f.write('start ApplicationUIBundle.bat')
        os.system("call call_oakgate.bat")
        os.chdir(startDir)
        time.sleep(10)

    def re_start_svf(self):

        self.logger.info("Step1: Kill SVF GUI (java.exe)")
        subprocess.Popen("taskkill /F /T /IM java.exe", shell=True)
        time.sleep(3)

        self.logger.info("Step2: Start SVF GUI service (java.exe)")
        cli_port = None
        rest_port = None
        self.start_svf()

        self.logger.info("Step3: Get SVF service port number (java.exe)")
        wait_time = 30
        start_time = time.time()

        while cli_port is None or rest_port is None:
            time.sleep(1)
            if time.time() - start_time > wait_time:
                raise EnvironmentError("Can't start SVF controller service in %d seconds" % wait_time)
            cli_port, rest_port = self.get_svf_service_ports_windows()
        return cli_port, rest_port


class StartMultiSvf(RestartSvf):
    def __init__(self, svf_num=1, logger=None):
        super(StartMultiSvf, self).__init__()

        self.logger = logger if logger else logging
        self.svf_num = svf_num
        self.cli_service_port_list = [7779, 7879, 7979, 8079, 8179, 8279, 8379, 8479, 8579, 8679, 8779, 8879, 8979,
                                      9079]
        self.rest_service_port_list = [9998, 9999, 10000, 10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009,
                                       10010, 10011]

    def get_cli_rest_port_by_pid(self, pid):
        """
        Get svf service (OakGate Enduro powered by SVF) cli port and rest port by system pid
        :param pid: pid in system task list
        :return: cli_port, rest_port
        """

        chkPortCmdStr = "netstat -ano -p TCP"
        cmd_run = subprocess.Popen(args=chkPortCmdStr, stdout=subprocess.PIPE)
        output_lines = cmd_run.stdout.readlines()
        listeningList = [line.strip().split() for line in output_lines if b"LISTENING" in line]
        portList = [int(localAddr.split(b":")[-1]) for _, localAddr, _, _, portPid in listeningList if portPid == pid]
        cli_portList = [port for port in portList if port in self.cli_service_port_list]
        rest_portList = [port for port in portList if port in self.rest_service_port_list]
        if not cli_portList:
            cli_port = None
        elif len(cli_portList) == 1:
            cli_port = cli_portList[0]
        else:
            raise EnvironmentError("cli_portList have multi port, please check that %s" % cli_portList)
        if not rest_portList:
            rest_port = None
        elif len(rest_portList) == 1:
            rest_port = rest_portList[0]
            self.logger.info("Get SVF service ports successfully")
            self.logger.info("System PID: {}, CLI port ID: {}, REST port ID: {}".format(pid, cli_port, rest_port))

        else:
            raise EnvironmentError("rest_portList have multi port, please check")

        return cli_port, rest_port

    def get_cli_rest_ports(self):
        """
        Get all svf cli ports and rest ports
        CLI Legacy Server Port: 7779
        CLI Telnet Server Port: 8889
        REST Server Port: 9998
        :return: cli ports and rest ports list [[cli_port1, rest_port1], [cli_port2, rest_port2]]
        """
        self.logger.info("Try to get SVF service ports information")

        chk_ps_cmd_str = "tasklist.exe -V -FI \"IMAGENAME EQ java.exe\""
        cmd_run = subprocess.Popen(args=chk_ps_cmd_str, stdout=subprocess.PIPE)
        output_lines = cmd_run.stdout.readlines()
        output_lines = [line for line in output_lines if b"OakGate Enduro powered by SVF Pro" in line]
        if not output_lines:
            return None, None
        else:
            pid_list = [line_temp.strip().split()[1] for line_temp in output_lines]

        cli_rest_port_list = list(map(self.get_cli_rest_port_by_pid, pid_list))

        return cli_rest_port_list

    def start_multi_svf_ports(self):
        """
        This is function for starting multi SVF GUI and return the corespondent cli port number and rest port number
        :return:
        """
        self.logger.info("Step1: Kill SVF GUI (java.exe)")
        subprocess.Popen("taskkill /F /T /IM java.exe", shell=True)
        time.sleep(3)

        self.logger.info("Step2: Start SVF GUI service (java.exe) for multi times")
        self.logger.info("Try to start {} SVF GUI".format(self.svf_num))
        for i in range(self.svf_num):
            self.logger.info("Try to start No.{} SVF GUI".format(i + 1))
            self.start_svf()
            time.sleep(2)

        self.logger.info("Step3: Get SVF service cli and rest ports information (java.exe)")
        cli_rest_port_list = []
        wait_time = 50
        start_time = time.time()

        while len(cli_rest_port_list) < self.svf_num:
            time.sleep(1)
            if time.time() - start_time > wait_time:
                raise EnvironmentError("Can't start SVF controller service in %d seconds" % wait_time)
            cli_rest_port_list = self.get_cli_rest_ports()

        return cli_rest_port_list


class PhaseScriptLog(object):

    def __init__(self, logger=None, test_type=None):
        self.logger = logger if logger else logging
        self.test_type = test_type

    def parseScriptStatus(self, script_log_path):
        """
        Get script status and last line in script log
        """
        if isinstance(script_log_path, str):
            script_log_path = script_log_path.encode("ascii")
        scriptResult = None
        try:
            with open(script_log_path, "r") as script_log:
                lines = script_log.readlines()
                lines.reverse()
                for line in lines[0:30]:
                    result_line = line
                    if "Test Passed." in result_line:
                        scriptResult = "Pass"
                        break
                    elif "Test Skipped" in result_line:
                        scriptResult = "Skip"
                        break
                    elif "Test Blocked" in result_line:
                        scriptResult = "Block"
                        break
                    elif "Test Failed" in result_line:
                        scriptResult = "Fail"
                        break
                    elif "The device healthy is not good, skip test directly" in result_line:
                        scriptResult = "Hung"
                        break
                    elif "requests.exceptions.ReadTimeout: HTTPConnectionPool" in result_line or \
                            "RestClient.resource.svf_python_rest.helper.RestError" in result_line or \
                            "AttributeError:" in result_line:
                        scriptResult = "Fail"
                        break
                    else:
                        scriptResult = "Fail"

        except Exception as error:
            logging.warning("parseScriptStatus file {} error {}}".format(script_log_path, str(error)))

        return (scriptResult, result_line)

    def parseDeviceFwInfo(self, script_log_path):
        """
        Get script status and last line in script log
        """

        if isinstance(script_log_path, str):
            script_log_path = script_log_path.encode("ascii")
        device_name = None
        FW_version = None
        try:
            with open(script_log_path, "r") as script_log:
                lines = script_log.readlines()
                for line_temp in lines:
                    if "Device name: " in line_temp:
                        device_name = line_temp.split(":")[-1].strip()
                        break
                for line_temp in lines:
                    if "The firmware version" in line_temp:
                        FW_version = line_temp.split(":")[- 1].strip().replace(".", "")
                        break
        except Exception as error:
            logging.warning("get FW info file %s error %s" % (script_log_path, str(error)))

        return str(device_name), str(FW_version)

    def getExecutionTime(self, script_log_path):
        """
        Get script execution time
        """
        execution_time = 0
        if isinstance(script_log_path, str):
            script_log_path = script_log_path.encode("ascii")
        try:
            with open(script_log_path, "r") as script_log:
                lines = script_log.readlines()
                endIndex = -1
                startTimeLine = lines[0]
                endTimeLine = lines[endIndex]
                match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}', startTimeLine)
                start_time = datetime.datetime.strptime(match.group(), '%Y-%m-%d %H:%M:%S,%f')
                match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}', endTimeLine)
                if match:
                    end_time = datetime.datetime.strptime(match.group(), '%Y-%m-%d %H:%M:%S,%f')
                else:
                    while not match:
                        endIndex = endIndex - 1
                        endTimeLine = lines[endIndex]
                        match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}', endTimeLine)
                    end_time = datetime.datetime.strptime(match.group(), '%Y-%m-%d %H:%M:%S,%f')
                execution_time = end_time - start_time
                execution_time = int(execution_time.total_seconds())
        except Exception as error:
            logging.warning("getExecutionTime file %s error %s" % (script_log_path, str(error)))

        return execution_time, end_time, start_time

    def get_files_sorted_time(self, path, script_name, device_name):
        script_key = script_name.split(".")[0]
        all_file_list = []
        for root, dir_list, file_list in os.walk(path):
            for file_temp in file_list:
                if device_name in root:
                    if script_key == re.split("[-.]", file_temp.replace(' ', ''))[-2]:
                        all_file_list.append(os.path.join(root, file_temp))

        all_file_list = sorted(all_file_list, key=lambda x: os.path.getmtime(x))
        all_file_list.reverse()

        return all_file_list

    def parseResult(self, base_code_path, script_name, device_name):
        log_path = os.path.join(base_code_path, "test-platform", "Logs")
        self.logger.info("Try to phase log: log path: {}, script: {}".format(log_path, script_name))
        script_logs_list = self.get_files_sorted_time(log_path, script_name, device_name)
        if len(script_logs_list) == 0:
            result_dic = {
                "log_generate": False,
                "result": {}
            }
        else:
            script_log_path = script_logs_list[0]
            device_name, FW_version = self.parseDeviceFwInfo(script_log_path)
            result, result_line = self.parseScriptStatus(script_log_path)
            execution_time, end_time, start_time = self.getExecutionTime(script_log_path)

            # Set Timeout time, script failed when test run more than 1h
            try:
                if time.time() - time.mktime(
                        time.strptime(str(end_time), "%Y-%m-%d %H:%M:%S.%f")) > 600 and result == "Running":
                    result = "Fail"
            except Exception as message:
                self.logger.error(message, "\n Get log time: {} \n test log end time: {}"
                                  .format(time.time(), end_time))

            execution_time = str(execution_time)
            end_time = str(end_time)
            start_time = str(start_time)

            result_dic = {
                "log_generate": True,
                "result_detail": {
                    "device_name": device_name,
                    "FW_version": FW_version,
                    "script_name": script_name,
                    "result": result,
                    "execution_time": execution_time,
                    "start_time": start_time,
                    "end_time": end_time,
                    "result_line": str(result_line)
                }
            }

        return result_dic

    def parseTextContentDPI(self, case_log_path):
        test_case_complete = False
        test_case_result = "Running"
        report_path = None
        for root, dir_list, file_list in os.walk(case_log_path):
            for file_temp in file_list:
                if "report" in file_temp:
                    report_path = os.path.join(case_log_path, file_temp)

        if report_path:
            with open(report_path, "r") as f:
                data = f.read()
                list = re.split("[\n\t.]", data.replace(' ', ''))
                if "Fail" in list or "Pass" in list or "Abort" in list:
                    test_case_complete = True
                    if list.count("Pass") == 2:
                        test_case_result = "Pass"
                    else:
                        test_case_result = "Fail"

                else:
                    test_case_complete = False
                    test_case_result = "Running"

        return test_case_complete, test_case_result

    def parseResultDPI(self, base_code_path, case_name, device_name):
        case_log_path = None
        log_path = os.path.join(base_code_path, "test-platform", "Logs")
        self.logger.info("Try to phase log: log path: {}, case: {}".format(log_path, case_name))

        for root, dir_list, file_list in os.walk(log_path):
            for dir_temp in dir_list:
                if case_name + "_" + device_name in dir_temp:
                    case_log_path = os.path.join(log_path, dir_temp)

        if not case_log_path:
            result_dic = {
                "log_generate": False,
                "result_detail": {}
            }
        else:
            test_case_complete, test_case_result = self.parseTextContentDPI(case_log_path)
            if test_case_complete:
                script_path = os.path.join(case_log_path, case_name)
                if len(os.listdir(script_path)) > 0:
                    script_path_temp = os.path.join(script_path, os.listdir(script_path)[0])

                    device_name, FW_version = self.parseDeviceFwInfo(script_path_temp)
                    result_script, result_line = self.parseScriptStatus(script_path_temp)
                    execution_time, end_time, start_time = self.getExecutionTime(script_path_temp)

                    # Set Timeout time, script failed when test run more than 1h
                    try:
                        if time.time() - time.mktime(
                                time.strptime(str(end_time),
                                              "%Y-%m-%d %H:%M:%S.%f")) > 3600 and result_script == "Running":
                            test_case_result = "Fail"
                    except Exception as message:
                        self.logger.error(message, "\n Get log time: {} \n test log end time: {}"
                                          .format(time.time(), end_time))

                    execution_time = str(execution_time)
                    end_time = str(end_time)
                    start_time = str(start_time)

                    result_dic = {
                        "log_generate": True,
                        "result_detail": {
                            "device_name": device_name,
                            "FW_version": FW_version,
                            "script_name": case_name,
                            "result": result_script if result_script == "Hung" else test_case_result,
                            "execution_time": execution_time,
                            "start_time": start_time,
                            "end_time": end_time,
                            "result_line": str(result_line)
                        }
                    }

                else:
                    result_dic = {
                        "log_generate": True,
                        "result_detail": {
                            "result": "Fail"
                        }
                    }

            else:
                if time.time() - os.path.getctime(case_log_path) > 300 and len(os.listdir(case_log_path)) < 3:
                    self.logger.error("DPI test doesn't start in 300s, exit test")
                    result_dic = {
                        "log_generate": True,
                        "result_detail": {
                            "result": "Hung"
                        }
                    }
                else:
                    result_dic = {
                        "log_generate": True,
                        "result_detail": {
                            "result": test_case_result
                        }
                    }

        return result_dic


class CollectLog(object):

    def __init__(self, logger=None, test_type=None):
        self.logger = logger if logger else logging
        self.test_type = test_type
        self.cluster_log_path = os.path.join("C:\\", "UART_LOG_Cluster")

    def tar_uart_file(self):
        source_dir = os.path.join(self.cluster_log_path, "UART_logs")
        output_filename = os.path.join(source_dir, "uart_logs.tar")
        if not os.path.exists(source_dir):
            logging.error("Target folder {} is not existing".format(source_dir))
            return False, None
        tar = tarfile.open(output_filename, "w")
        for root, dir, files in os.walk(source_dir):
            for file in files:
                pathfile = os.path.join(root, file)
                tar.add(pathfile, file)
        tar.close()
        logging.info("Tar uart log {} successfully, {}".format(source_dir, output_filename))
        return True, output_filename

    def tar_2step_file(self):
        source_dir = os.path.join(self.cluster_log_path, "Two_step_download_logs")
        output_filename = os.path.join(source_dir, "2step_dl_logs.tar")
        if not os.path.exists(source_dir):
            logging.error("Target folder {} is not existing".format(source_dir))
            return False, None
        tar = tarfile.open(output_filename, "w")
        for root, dir, files in os.walk(source_dir):
            for file in files:
                pathfile = os.path.join(root, file)
                tar.add(pathfile, file)
        tar.close()
        logging.info("Tar uart log {} successfully, {}".format(source_dir, output_filename))
        return True, output_filename

    def tar_script_file(self, base_code_path, device_name):
        source_dir = os.path.join(base_code_path, "test-platform", "Logs")
        output_filename = os.path.join(source_dir, device_name + "_script_logs.tar")
        logging.info("Try to get script logs: {}".format(source_dir))
        if not os.path.exists(source_dir):
            logging.error("Target folder {} is not existing".format(source_dir))
            return False, None

        tar = tarfile.open(output_filename, "w")

        if self.test_type == "DPI_test":
            # Only package the folders and files of the first-level directory
            for root, dir, files in os.walk(source_dir):
                for dir_temp in dir:
                    if device_name in root:
                        for root, dir, files in os.walk(os.path.join(root, dir_temp)):
                            for file_temp in files:
                                pathfile = os.path.join(root, file_temp)
                                tar.add(pathfile, os.path.join(dir_temp, file_temp))

        else:
            # Only package all the script logs
            for root, dir, files in os.walk(source_dir):
                for file in files:
                    if device_name in root:
                        pathfile = os.path.join(root, file)
                        tar.add(pathfile, file)

        tar.close()
        logging.info("Tar script log {} successfully, {}".format(source_dir, output_filename))
        return True, output_filename


class ConnectDataBase(object):

    def __init__(self, db_name=None, logger=None, db_type="local"):
        self.logger = logger if logger else logging
        self.db_name = db_name
        self.db_obj = None
        self.collection = None
        self.db_client = None
        self.db_type = db_type

    def open_db(self):
        """
        Connect database
        :return:
        """
        if self.db_type != "local":
            db_config = {"mongo_host": "192.168.187.64",  # "10.199.209.33",  # "10.124.126.64",
                         "mongo_user": "issd",
                         "mongo_password": "issd123"}

            server = SSHTunnelForwarder(
                db_config["mongo_host"],
                ssh_username=db_config["mongo_user"],
                ssh_password=db_config["mongo_password"],
                remote_bind_address=('127.0.0.1', 27017)
            )

            server.start()

            self.db_client = MongoClient('127.0.0.1',
                                         server.local_bind_port)  # server.local_bind_port is assigned local port
        else:
            self.db_client = MongoClient("localhost", 27017)

        self.db_obj = self.db_client[self.db_name]

    def judge_connection(self):
        """
        This is to check maogoDB service
        :return:
        """
        if not self.db_client:
            self.open_db()
        try:
            self.db_client.admin.command('ismaster')
        except errors.PyMongoError as e:
            self.logger.error("DB ERROR!!\n Details: {}".format(e))
            self.logger.info("Try to connect DB again...")
            self.open_db()
            try:
                self.db_client.admin.command('ismaster')
            except errors.PyMongoError as e:
                self.logger.error("DB ERROR!!\n Details: {}".format(e))
                self.logger.exception("Please check mongoDB service manually!!! ")

    def close_db(self):
        """
        Close database
        :return:
        """
        self.db_client.close()

    def connect_create_collection(self, collection_name=None):
        self.judge_connection()
        self.collection = self.db_obj[collection_name]

    def import_df_to_db(self, collection_name=None, df=None):
        """
        import dataframe to database
        :param collection_name:
        :param df:
        :return:
        """
        df['_id'] = df.index

        self.connect_create_collection(collection_name=collection_name)
        self.collection.insert(json.loads(df.T.to_json()).values())

    def index_data(self, index_condition, collection_name=None):
        self.judge_connection()
        self.collection = self.db_obj[collection_name]
        self.collection.ensureIndex(index_condition)

    def update_data(self, update_condition, updata_info, collection_name=None, update_one=True):
        """
        Update target data
        :param update_condition:
        :param updata_info:
        :param collection_name:
        :param update_one:
        :return:
        """
        self.judge_connection()
        if collection_name is not None:
            self.collection = self.db_obj[collection_name]

        if not isinstance(updata_info, dict):
            self.logger.exception("Update info is not a dic, please check it!")

        if update_one:
            self.collection.update_one(filter=update_condition, update={'$set': updata_info}, upsert=False)
        else:
            self.collection.update_many(filter=update_condition, update={'$set': updata_info}, upsert=False)

    def get_data(self, condition, collection_name=None, find_one=True, limit=None):
        self.judge_connection()
        if collection_name is not None:
            self.collection = self.db_obj[collection_name]
        if find_one:
            result_data = self.collection.find_one(condition)
        else:
            if limit:
                result_data = self.collection.find(condition).limit(limit)
            else:
                result_data = self.collection.find(condition)

        return result_data

    def get_data_or(self, condition, collection_name=None):
        self.judge_connection()
        if collection_name is not None:
            self.collection = self.db_obj[collection_name]

        result_data = self.collection.find({"$or": condition})

        return result_data

    def export_db_to_df(self, collection_name=None, condition=None):
        """
        import dataframe to database
        :param collection_name:
        :return:
        """
        self.judge_connection()
        if collection_name is not None:
            self.collection = self.db_obj[collection_name]
        if condition:
            cursor = self.collection.find({}, condition)
        else:
            cursor = self.collection.find({})
        df = pd.DataFrame(list(cursor))

        return df

    def count_items(self, condition=None, collection_name=None):
        """
        import dataframe to database
        :param collection_name:
        :return:
        """
        self.judge_connection()
        if collection_name is not None:
            self.collection = self.db_obj[collection_name]

        if condition:
            return self.collection.count_documents(condition)
        else:
            return self.collection.estimated_document_count()

    def db_cmd_execute(self, cmd):
        self.judge_connection()
        self.logger.info("Execute MongoDB command: {}".format(cmd))
        self.db_obj.command(cmd)  # "dropDatabase"
