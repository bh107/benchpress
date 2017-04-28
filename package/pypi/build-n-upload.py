#!/usr/bin/env python
from subprocess import Popen, PIPE, STDOUT
from os import path
import argparse
import re
import traceback

log = ""  # The output of this build and/or testing

def bash_cmd(cmd, cwd=None):
    global log
    print cmd
    out = ""
    try:
        p = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True, cwd=cwd)
        while p.poll() is None:
            t = p.stdout.readline()
            out += t
            print t,
        t = p.stdout.read()
        out += t
        print t,
        p.wait()
    except KeyboardInterrupt:
        p.kill()
        raise
    log = "%s%s%s" % (log, cmd, out)
    return out


def main(args):
    global log
    bp_dir = args.benchpress_root

    # Clean up the repos
    if args.git_cleanup:
        bash_cmd('git reset --hard master', cwd=bp_dir)
        bash_cmd('git clean -xdf', cwd=bp_dir)

    # Update the repos
    bash_cmd('git checkout master', cwd=bp_dir)
    ret = bash_cmd('git pull', cwd=bp_dir)
    if args.only_on_changes and 'Already up-to-date' in ret:
        log += "No changes to the git repos, exiting."
        return

    # Get latest git tag e.g. v2.1
    version = bash_cmd("git describe --tags --match *v[0-9]* ", cwd=bp_dir)
    bash_cmd('git checkout %s' % version, cwd=bp_dir)

    # Build the source distribution package
    bash_cmd('python setup.py sdist', cwd=bp_dir)

    # Upload the package to <https://pypi.python.org/pypi>
    bash_cmd('twine upload --sign --identity "%s" dist/*' % args.gpg_identity, cwd=bp_dir)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                description='Build the PyPi package (PIP) and upload it to <https://pypi.python.org/pypi>.',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '--benchpress-root',
        default=str(path.join(path.dirname(path.abspath(__file__)), "..", "..")),
        type=str,
        help='Path to the root of Benchpress.'
    )
    parser.add_argument(
        '--gpg-identity',
        default="Bohrium Builder <builder@bh107.org>",
        type=str,
        help='The PGP sign identity (specified in ~/.gnupg/pubring.gpg).'
    )
    parser.add_argument(
        '--email',
        type=str,
        help='The result of the build and/or test will be emailed to the specified address.'
    )
    parser.add_argument(
        '--only-on-changes',
        action="store_true",
        help='Only execute when the git repos has been changed.'
    )
    parser.add_argument(
        '--git-cleanup',
        action="store_true",
        help='Clean up the git repos (WILL DELETE non-committed files!).'
    )
    args = parser.parse_args()
    status = "SUCCESS"
    try:
        main(args)
    except StandardError, e:
        log += "*"*70
        log += "\nERROR: %s"%traceback.format_exc()
        log += "*"*70
        log += "\n"
        status = "FAILURE"
        try:
            log += e.output
        except:
            pass
    print
    print log
    if args.email:
        print ("send status email to '%s'" % args.email)
        p = Popen(['mail','-s','"[Bohrium PyPi Build] The result of build was a %s"' % status, args.email],
                  stdin=PIPE)
        p.communicate(input=log)

