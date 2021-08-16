"""various functions and class for access to synpase and comparing files with local files"""

import sys
import os.path as osp
import json
from lrgasp.loggingOps import getLrgaspLogger
from lrgasp import LrgaspException


# synpase upload has an really annoying spinner, disable it
import synapseclient.core.utils as synapseutils

def noop_print_tick(self):
    pass

synapseutils.Spinner.print_tick = noop_print_tick

import synapseclient
import synapseutils
from synapseclient import Synapse
from synapseclient.__main__ import login_with_prompt  # function used by synapse command
from lrgasp.objDict import ObjDict
from lrgasp import prog_error_excepts
from lrgasp.defs import Challenge

prog_error_syn_excepts = (synapseclient.core.exceptions.SynapseError, ) + prog_error_excepts

class SynNode:
    "Node in the synapse entity hierarchy."
    def __init__(self, entity):
        self.entity = entity
        self.children = []

class SynTree:
    """Tree of synapse entities (Project, Folder, File, Link)."""
    def __init__(self):
        self.root = None
        self.node_by_synid = {}

    def add(self, entity):
        node = SynNode(entity)
        self.node_by_synid[node.entity.id] = node
        if self.root is None:
            self.root = node
        else:
            parent = self.node_by_synid[entity.parentId]
            parent.children.append(node)
        return node

def syn_tree_load(syn, root_synid):
    """Load existing file hierarchy information from synapse into a SynNode tree"""
    syn_tree = SynTree()
    for root, dir, files in synapseutils.walk(syn, root_synid):
        syn_tree.add(syn.get(dir))
        for f in files:
            syn_tree.add(syn.get(f))
    return syn_tree

class FileNode:
    """Node in the file hierarchy, for uploading or comparing against
    synapse"""
    def __init__(self, filename, parent, isdir):
        self.filename = filename
        self.isdir = isdir
        self.parent = parent
        self.children = []

    def get_path(self, root_dir=None):
        path = []
        n = self
        while n is not None:
            path.insert(0, n.filename)
            n = n.parent
        if root_dir is not None:
            path.insert(0, root_dir)
        return osp.join(*path)

    def dump(self, indent, fh=sys.stderr):
        print((4 * indent * ' ') + self.filename + ('/' if self.isdir > 0 else ''),
              file=fh)
        for node in self.children:
            node.dump(indent + 1, fh)

class FileTree:
    """Tree of files and directories, build from metadata"""
    def __init__(self):
        self.root = None

    def add(self, filepath, parent, isdir=False):
        filename = osp.basename(filepath)
        node = FileNode(filename, parent, isdir)
        if self.root is None:
            assert parent is None
            self.root = node
        else:
            parent.children.append(node)
        return node

    def dump(self, fh=sys.stderr):
        print("FileTree", file=fh)
        if self.root is not None:
            self.root.dump(1, fh)

def add_login_args(parser):
    "add options for logging into synapse"
    parser.add_argument("--test_config_json",
                        help="JSON configuration file for doing testing.  See  See lrgasp.synapse_access.LrgaspSynapseConfig for information.")
    parser.add_argument('-u', '--username', dest='synapseUser',
                        help='Username or email address used to connect to Synapse; if not specified must already be logged in with the --rememberMe option to this program or the synapse program')
    parser.add_argument('-p', '--password', dest='synapsePassword',
                        help='Password or api key used to connect to Synapse')
    parser.add_argument('--rememberMe', '--remember-me', dest='rememberMe', action='store_true', default=False,
                        help='Cache credentials for automatic authentication on future interactions with Synapse')

def syn_connect(args):
    "connect and log in based on options"
    syn_conf = LrgaspSynConfig.factory(args)
    syn = Synapse()
    syn.logger.setLevel(getLrgaspLogger().level)  # cut down on noise

    # None user/password uses cache or prompts.  Command line overrides conf
    user = args.synapseUser if args.synapseUser is not None else syn_conf.user
    password = args.synapsePassword if args.synapsePassword is not None else syn_conf.password
    login_with_prompt(syn, user, password, rememberMe=args.rememberMe)
    getLrgaspLogger().debug(f"logged in as synpase user '{syn.username}'")
    return syn

def get_project_by_name(syn, project_name):
    synid = syn.findEntityId(project_name)
    if synid is None:
        raise LrgaspException(f"synapse project not found '{project_name}'")
    return synid

class LrgaspSynConfig:
    """Object contain configuration for accessing synapse.  For production
    submission, this has the predefined ids from production_lrgasp_syn_ids
    and uses the login prompted or from the --rememberMe cached.

    For testing, the fields are loaded from a JSON file and include a test
    user and password/app key.

    The test JSON file should have the fields 'user' and 'password', and
    fields from set in _init_production
    """
    @classmethod
    def _production_conf(cls):
        self = cls()
        self.user = None
        self.password = None
        self.lrgasp_synchallenge_name = 'LRGASP'
        self.lrgasp_synchallenge_id = 4441
        self.participants_team_name = 'LRGASP Participants',
        self.syn_queue_ids = {
            Challenge.iso_detect_ref: 9614748,
            Challenge.iso_quant: 9614749,
            Challenge.iso_detect_de_novo: 9614750,
        }
        return self

    @classmethod
    def _test_conf(cls, test_config_json):
        with open(test_config_json) as fh:
            conf = json.load(fh, object_pairs_hook=ObjDict)
        self = cls()
        self.user = conf.user
        self.password = conf.password
        self.lrgasp_synchallenge_name = conf.lrgasp_synchallenge_name
        self.lrgasp_synchallenge_id = conf.lrgasp_synchallenge_id
        self.participants_team_name = conf.participants_team_name
        self.syn_queue_ids = {}
        for key, val in conf.syn_queue_ids.items():
            self.syn_queue_ids[Challenge(key)] = val
        return self

    @classmethod
    def factory(cls, args):
        if args.test_config_json is not None:
            return cls._test_conf(args.test_config_json)
        else:
            return cls._production_conf()
