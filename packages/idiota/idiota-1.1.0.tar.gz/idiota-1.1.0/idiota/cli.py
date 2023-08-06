#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cli.py: Command line interface for idiota.
"""
__author__ = "prakashsellathurai"
__copyright__ = "Copyright 2021"
__version__ = "1.0.1"
__email__ = "prakashsellathurai@gmail.com"

import argparse
import sys
import subprocess
import textwrap

from . import base
from . import data
from . import diff
from . import remote

def main ():
    """
    Main entry point.
    """
    with data.change_git_dir ('.'):
        args = parse_args ()
        args.func (args)


    
def parse_args ():
    """
    Parse command line arguments.
    """
    
    parser = argparse.ArgumentParser (formatter_class=argparse.RawTextHelpFormatter)

    commands = parser.add_subparsers (dest='command', required=True,    metavar='COMMAND', help='description')
    commands.required = True
    
    oid = base.get_oid

    init_parser = commands.add_parser ('init', help='Initialize a new git repository')
    init_parser.set_defaults (func=init)

    hash_object_parser = commands.add_parser ('hashobject', help='Compute object ID', aliases=['hash-object'])
    hash_object_parser.set_defaults (func=hash_object)
    hash_object_parser.add_argument ('file',help='File to hash')

    cat_file_parser = commands.add_parser ('catfile', help='Print object contents', aliases=['cat-file'])
    cat_file_parser.set_defaults (func=cat_file)
    cat_file_parser.add_argument ('object', type=oid,help='Object to cat')

    write_tree_parser = commands.add_parser ('writetree', help='Write tree object', aliases=['write-tree'])
    write_tree_parser.set_defaults (func=write_tree)

    read_tree_parser = commands.add_parser ('readtree', help='Read tree object', aliases=['read-tree'])
    read_tree_parser.set_defaults (func=read_tree)
    read_tree_parser.add_argument ('tree', type=oid,help='Tree to read')


    commit_parser = commands.add_parser ('commit', help='Commit changes', aliases=['ci'])
    commit_parser.set_defaults (func=commit)
    commit_parser.add_argument ('-m', '--message', required=True,help='Commit message(required)')

    log_parser = commands.add_parser ('log', help='Show commit log', aliases=['lo'])
    log_parser.set_defaults (func=log)
    log_parser.add_argument ('oid', default='@', type=oid, nargs='?',help='Commit to log from')

    show_parser = commands.add_parser ('show', help='Show commit', aliases=['sh'])
    show_parser.set_defaults (func=show)
    show_parser.add_argument ('oid', default='@', type=oid, nargs='?',help='Commit to show')

    diff_parser = commands.add_parser ('diff', help='Show diff', aliases=['di'])
    diff_parser.set_defaults (func=_diff)
    diff_parser.add_argument ('--cached', action='store_true',help='Diff against index')
    diff_parser.add_argument ('commit', nargs='?', type=oid,help='Commit to diff from')

    checkout_parser = commands.add_parser ('checkout', aliases=['co'])
    checkout_parser.set_defaults (func=checkout)
    checkout_parser.add_argument ('commit', type=oid,help='Commit to checkout')

    tag_parser = commands.add_parser ('tag', help='Create a tag', aliases=['ta'])
    tag_parser.set_defaults (func=tag)
    tag_parser.add_argument ('name', help='Tag name')
    tag_parser.add_argument ('oid', default='@', type=oid, nargs='?',help='Commit to tag from')

    branch_parser = commands.add_parser ('branch', help='Create a branch', aliases=['br'])
    branch_parser.set_defaults (func=branch)
    branch_parser.add_argument ('name', nargs='?')
    branch_parser.add_argument ('start_point', default='@', type=oid, nargs='?',help='Commit to start branch from')

    k_parser = commands.add_parser ('k', help='Create a key', aliases=['ke'])
    k_parser.set_defaults (func=k)

    status_parser = commands.add_parser ('status', help='Show status', aliases=['st'])
    status_parser.set_defaults (func=status)

    reset_parser = commands.add_parser ('reset', help='Reset to commit', aliases=['re'])
    reset_parser.set_defaults (func=reset)
    reset_parser.add_argument ('commit', type=oid,help='Commit to reset to')

    merge_parser = commands.add_parser ('merge', help='Merge commit', aliases=['me'])
    merge_parser.set_defaults (func=merge)
    merge_parser.add_argument ('commit', type=oid,help='Commit to merge')

    merge_base_parser = commands.add_parser ('mergebase', help='Find merge base', aliases=['mb'])
    merge_base_parser.set_defaults (func=merge_base)
    merge_base_parser.add_argument ('commit1', type=oid,help='Commit to find merge base from')
    merge_base_parser.add_argument ('commit2', type=oid,help='Commit to find merge base to')

    fetch_parser = commands.add_parser ('fetch', help='Fetch remote', aliases=['fe'])
    fetch_parser.set_defaults (func=fetch)
    fetch_parser.add_argument ('remote', help='Remote to fetch from')

    push_parser = commands.add_parser ('push', help='Push to remote', aliases=['pu'])
    push_parser.set_defaults (func=push)
    push_parser.add_argument ('remote', help='Remote to push to')
    push_parser.add_argument ('branch', nargs='?', help='Branch to push')

    add_parser = commands.add_parser ('add', help='Add file to index', aliases=['ad'])
    add_parser.set_defaults (func=add)
    add_parser.add_argument ('files', nargs='+', help='Files to add')

    return parser.parse_args ()


def init (args):
    base.init ()



def hash_object (args):
    with open (args.file, 'rb') as f:
        print (data.hash_object (f.read ()))


def cat_file (args):
    sys.stdout.flush ()
    sys.stdout.buffer.write (data.get_object (args.object, expected=None))



def write_tree (args):
    print (base.write_tree ())

def read_tree (args):
    base.read_tree (args.tree)


def commit (args):
    print (base.commit (args.message))\

def _print_commit (oid, commit, refs=None):
    refs_str = f' ({", ".join (refs)})' if refs else ''
    print (f'commit {oid}{refs_str}\n')
    print (textwrap.indent (commit.message, '    '))
    print ('')

def log (args):
    refs = {}
    for refname, ref in data.iter_refs ():
        refs.setdefault (ref.value, []).append (refname)

    for oid in base.iter_commits_and_parents ({args.oid}):
        commit = base.get_commit (oid)
        _print_commit (oid, commit, refs.get (oid))


def show (args):
    if not args.oid:
        return
    commit = base.get_commit (args.oid)
    parent_tree = None
    if commit.parents:
        parent_tree = base.get_commit (commit.parents[0]).tree

    _print_commit (args.oid, commit)
    result = diff.diff_trees (
        base.get_tree (parent_tree), base.get_tree (commit.tree))
    sys.stdout.flush ()
    sys.stdout.buffer.write (result)

def _diff (args):
    oid = args.commit and base.get_oid (args.commit)

    if args.commit:
        # If a commit was provided explicitly, diff from it
        tree_from = base.get_tree (oid and base.get_commit (oid).tree)

    if args.cached:
        tree_to = base.get_index_tree ()
        if not args.commit:
            # If no commit was provided, diff from HEAD
            oid = base.get_oid ('@')
            tree_from = base.get_tree (oid and base.get_commit (oid).tree)
    else:
        tree_to = base.get_working_tree ()
        if not args.commit:
            # If no commit was provided, diff from index
            tree_from = base.get_index_tree ()

    result = diff.diff_trees (tree_from, tree_to)
    sys.stdout.flush ()
    sys.stdout.buffer.write (result)
    

def checkout (args):
    base.checkout (args.commit)

def tag (args):
    base.create_tag (args.name, args.oid)

def branch (args):
    if not args.name:
        current = base.get_branch_name ()
        for branch in base.iter_branch_names ():
            prefix = '*' if branch == current else ' '
            print (f'{prefix} {branch}')
    else:
        base.create_branch (args.name, args.start_point)
        print (f'Branch {args.name} created at {args.start_point[:10]}')



def k (args):
    dot = 'digraph commits {\n'
    oids = set ()
    for refname, ref in data.iter_refs (deref=False):
        dot += f'"{refname}" [shape=note]\n'
        dot += f'"{refname}" -> "{ref.value}"\n'
        if not ref.symbolic:
            oids.add (ref.value)

    for oid in base.iter_commits_and_parents (oids):
        commit = base.get_commit (oid)
        dot += f'"{oid}" [shape=box style=filled label="{oid[:10]}"]\n'
        for parent in commit.parents:
            dot += f'"{oid}" -> "{parent}"\n'

    dot += '}'
    print (dot)
    with subprocess.Popen (
        ['dot', '-Tgtk', '/dev/stdin'],
        stdin=subprocess.PIPE) as proc:
        proc.communicate (dot.encode ())




def status (args):
    HEAD = base.get_oid ('@')
    branch = base.get_branch_name ()
    if branch:
        print (f'On branch {branch}')
    else:
        print (f'HEAD detached at {HEAD[:10]}')

    MERGE_HEAD = data.get_ref ('MERGE_HEAD').value
    if MERGE_HEAD:
        print (f'Merging with {MERGE_HEAD[:10]}')

    print ('\nChanges to be committed:\n')
    HEAD_tree = HEAD and base.get_commit (HEAD).tree
    for path, action in diff.iter_changed_files (base.get_tree (HEAD_tree),
                                                 base.get_index_tree ()):
        print (f'{action:>12}: {path}')

    print ('\nChanges not staged for commit:\n')
    for path, action in diff.iter_changed_files (base.get_index_tree (),
                                                 base.get_working_tree ()):
        print (f'{action:>12}: {path}')

def reset (args):
    base.reset (args.commit)



def merge (args):
    base.merge (args.commit)




def merge_base (args):
    print (base.get_merge_base (args.commit1, args.commit2))



def fetch (args):
    remote.fetch (args.remote)



def push (args):
    remote.push (args.remote, f'refs/heads/{args.branch}')




def add (args):
    base.add (args.files)