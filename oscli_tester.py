#!/usr/bin/env python

import subprocess
import json
import argparse
import os
import shlex
import re
import shutil
import sys

class clientTester():

  def __init__(self, base_dir, openrc, codebase):
    self.base_dir = base_dir
    self.openrc = openrc
    self.codebase = codebase

    # Setup the virtual environment
    try:
      if self.codebase in "newton ocata pike queens rocky stein train":
        subprocess.check_call(["python2.7", "-m", "virtualenv", self.base_dir + self.codebase])
    except Exception as e:
      print e
      sys.exit(1)

  def install_client(self, client, version, codebase):
    # Try to install the desired package
    
    subprocess.check_call([self.base_dir + self.codebase + "/bin/pip", \
      "install", "--isolated", \
      "--constraint", self.codebase + "_files/" + self.codebase + "-constraints.txt", \
      client + "==" + version ])
    # Cleanup 
    #shutil.rmtree("/tmp/" + client)

  def run_tests(self, client, version, codebase, test_commands):
    # Setup the environment variables
    command = shlex.split("env -i bash -c 'source /root/openrc && env'")
    proc = subprocess.Popen(command, stdout = subprocess.PIPE)
    for line in proc.stdout:
      (key, _, value) = line.partition("=")
      os.environ[key] = value.strip('\n')
    proc.communicate()

    # Determine which command we're running so we can execute the tests
    results = re.findall(client[7:-6] + ".*", test_commands)
    client_bin = self.base_dir + self.codebase + "/bin/"
    for i in results:
      client_command = client_bin + i
      try:
        subprocess.check_call(client_command.split(' '))
        self.log_output(i, True)
      except subprocess.CalledProcessError as e:
        self.log_output(i, False)
        
  def log_output(self, line, result=None):
    with open("osa-tester-results.txt", 'a+') as f:
      if result is not None:
        if result:
          line = line + "...PASS"
        else:
          line = line + "...FAIL"
      f.write(line + '\n')


###
# Main Logic
###

base_dir = "/openstack/venvs/"
openrc = "/root/openrc"

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("codebase", type=str, help="The client versions to test.", choices=["newton", "ocata", "pike", "queens", "rocky", "stein", "train", "ussuri"])
arg_parser.add_argument("os-version", type=str, help="The version of OpenStack to test the clients against.")
args = arg_parser.parse_args()

version_file = open("oscli_tester/" + args.codebase + "_files/" + args.codebase + "-versions.json", 'r')
versions_json = json.loads(version_file.read())
version_file.close()

# Get the test commands
test_commands = ""
with open("tests.txt", 'r') as f:
  test_commands = f.read()


cli_tester = clientTester(base_dir, openrc, args.codebase)
#print versions_json

for clients in versions_json["parameters"]:
  print clients
  for client in clients.keys():
#    print "I am going to install" + client + version
    for version in clients[client]:
      print "Starting test run for " + client + " version " + version
      cli_tester.log_output("Starting test run for " + client[7:-6] + " version " + version)
      cli_tester.install_client(client, version, args.codebase)
      cli_tester.run_tests(client, version, args.codebase, test_commands)
