#!/usr/bin/env python

import os
import subprocess
import sys
import xml.etree.ElementTree as ET

user_home = os.environ['HOME']
dans_parent_dir = os.environ.get('DANS_PARENT_DIR', user_home + '/git/service/dans-parent')
repo_base_url = 'git@github.com:DANS-KNAW'

def update_module( module ):
    print '>>> Updating module ' + module + ' ...'
    is_present = os.path.isdir(dans_parent_dir + '/' + module)
    if (is_present):
        print ' ... is present, switching to master and pulling blessed ...'
        os.system('git -C ' + dans_parent_dir + '/' + module + ' add .')
        os.system('git -C ' + dans_parent_dir + '/' + module + ' stash')
        os.system('git -C ' + dans_parent_dir + '/' + module + ' checkout master')
        os.system('git -C ' + dans_parent_dir + '/' + module + ' pull')
    else:
        print ' ... not present yet, cloning ...'
        os.system('git clone -o blessed ' + repo_base_url + '/' + module + '.git ' + dans_parent_dir + '/' + module)
    remotes = subprocess.check_output(('git -C ' + dans_parent_dir + '/' + module + ' remote').split())
    if not('blessed' in remotes):
        print 'WARNING: NO REMOTE blessed found. SKIPPING UPDATE !!! PLEASE FIX THE PROBLEM BY CREATING THE blessed REMOTE'
    else:
        pull_requests_refspec = '+refs/pull/*/head:refs/remotes/blessed/pr/*'
        refspecs = subprocess.check_output(('git -C ' + dans_parent_dir + '/' + module + ' config --local --get-all remote.blessed.fetch').split())
        if not(pull_requests_refspec in refspecs):
            print 'Adding refspec for pull requests ...'
            os.system('git -C ' + dans_parent_dir + '/' + module + ' config --local --add remote.blessed.fetch "' + pull_requests_refspec + '"')
            os.system('git -C ' + dans_parent_dir + '/' + module + ' fetch')
    print '<<<'
    print

def update_modules( modules ):
    for m in modules:
        update_module(m)

def get_module_list(easy_source_dir):
    masterPom = easy_source_dir + '/dans-mvn-parent/pom.xml'
    print 'Retrieving list of modules from: ' + masterPom + ' ...'
    pom = ET.parse(masterPom)
    prefixes = {
        'pom': 'http://maven.apache.org/POM/4.0.0'
    }
    modules = pom.find('pom:modules', prefixes)
    for module in modules.findall('pom:module', prefixes):
        yield module.text[3:]

def update_all_modules():
    print 'Getting master build ...'
    update_module('dans-mvn-parent')
    print 'Getting module list ...'
    modules = list(get_module_list(dans_parent_dir))
    for m in modules:
        print m
    print
    print 'Updating modules ...'
    update_modules(modules)

def ensure_dans_parent_dir_exists():
    print 'Ensure ' + dans_parent_dir + ' exists ...'
    if (not(os.path.isdir(dans_parent_dir))):
        os.makedirs(dans_parent_dir)

def update_code():
    print 'Start updating code ...'
    ensure_dans_parent_dir_exists()
    update_all_modules()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dans_parent_dir = sys.argv[1]
    update_code()
