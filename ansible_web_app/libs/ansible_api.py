#!/usr/bin/env python

import json
import os
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from tempfile import NamedTemporaryFile
import ansible.constants as C


class ResultCallback(CallbackBase):
    """ The format ansible result callback """
    def __init__(self, *args, **kwargs):
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class AnsibleApi(object):
    """The init ansible class"""
    def __init__(self):
        self.Options = namedtuple('Options',['connection', 'remote_user', 'ask_sudo_pass', 'verbosity',
            'ack_pass', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check',
            'listhosts', 'listtasks', 'listtags', 'syntax', 'sudo_user', 'sudo', 'diff'])

        self.ops = self.Options(connection='smart', remote_user=None, ack_pass=None, sudo_user=None,
            forks=5, sudo=None, ask_sudo_pass=False, verbosity=5, become=None, become_method=None,
            module_path='/usr/local/lib/python2.7/site-packages/ansible/modules/', become_user=None,
            check=False, diff=False, listhosts=None, listtasks=None, listtags=None, syntax=None)

        """create a tmpfile to save host_list"""
        self.hostsFile = NamedTemporaryFile(delete=False)
        for host in host_list:
            self.hostsFile.write(str(host) + "\n")
        self.hostsFile.close()

        self.passwords = dict(vault_pass='secret')
        self.loader = DataLoader()
        self.results_callback = ResultCallback()
        self.inventory = InventoryManager(loader=self.loader, sources=self.hostsFile.name)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

    def run(self,host_list, task_list):
        play_source = dict(
            name="Ansible Task",
            hosts=host_list,
            gather_facts='no',
            tasks=task_list
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None

        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.ops,
                passwords=self.passwords,
                stdout_callback=self.results_callback,
                run_additional_callbacks=C.DEFAULT_LOAD_CALLBACK_PLUGINS,
                run_tree=False,
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
                os.remove(self.hostsFile.name)
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

        results_raw = {}
        results_raw['success'] = {}
        results_raw['failed'] = {}
        results_raw['unreachable'] = {}

        for host, result in self.results_callback.host_ok.items():
            results_raw['success'][host] = result._result["stdout_lines"]

        for host, result in self.results_callback.host_failed.items():
            results_raw['failed'][host] = result._result["stdout_lines"]

        for host, result in self.results_callback.host_unreachable.items():
            results_raw['unreachable'][host] = "Failed to connect to the host"

        print json.dumps(results_raw)


    def playbookrun(self, playbook_path):

        self.variable_manager.extra_vars = {'customer': 'test', 'disabled': 'yes'}
        playbook = PlaybookExecutor(playbooks=playbook_path,
                                    inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader, options=self.ops, passwords=self.passwords)
        result = playbook.run()
        return result


if __name__ == "__main__":
    host_list = ['140.143.154.13', '192.168.0.1']
    tasks_list = [
        dict(action=dict(module='raw', args='ls')),
    ]
    ansible = AnsibleApi()
    ansible.run(host_list,tasks_list)
    ansible.playbookrun(playbook_path=['/root/ansible-project/test.yml'])
