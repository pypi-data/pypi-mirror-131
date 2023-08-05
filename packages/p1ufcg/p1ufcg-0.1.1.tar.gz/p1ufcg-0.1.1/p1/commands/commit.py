from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import hashlib
import io
import os
import sys

import p1
from p1.utils import data2json, _assert, cprint
from p1.colors import *
from p1.jsonfile import JsonFile

def main():
    _assert(len(sys.argv) in [3, 4], 'Usage: p1 commit [--support-file|-s] <filename>')
    _assert(os.path.exists('.p1/assignment.json'), 'No p1 assignment found')
    filetype = 'support' if sys.argv[2] in ['--support-file', '-s'] else 'answer'
    filename = sys.argv[3 if filetype == 'support' else 2]
    assignment_id = JsonFile('.p1/assignment.json')['iid']
    site = p1.get_site('_DEFAULT')
    commit(filename, filetype, assignment_id, site)


def read_mode(filename):
    return "rw"


def read_content(filename):
    with io.open(filename, encoding='utf-8') as f:
        content = f.read()

    return content


def commit(filename, filetype, key, site):
    content = read_content(filename)
    checksum = hashlib.sha1(content.encode('utf-8')).hexdigest()
    data = {
        "files": [{
                "name": filename,
                "content": content,
                "mode": read_mode(filename),
                "category": "public",
                "type": filetype,
                "hash": checksum
            }],
        "hash": checksum
    }

    response = site.send_answer(data, key)
    if response.ok:
        cprint(LGREEN, 'File saved successfully')
    elif response.status_code == 401:
        cprint(LRED, 'Commit failed (%s)' % response.status_code)
        cprint(LRED, 'run: p1 login')
    elif response.status_code == 412:
        cprint(LRED, 'Commit failed (%s)' % response.status_code)
        cprint(LRED, 'Error: %s' % response.json()['messages'][0])
    else:
        cprint(LRED, 'Commit failed (%s)' % response.status_code)
        cprint(LRED, 'Error: %s' % response.json()['messages'][0])
