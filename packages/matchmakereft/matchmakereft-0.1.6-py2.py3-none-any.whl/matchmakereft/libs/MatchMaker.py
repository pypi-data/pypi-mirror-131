# MatchMaker.py
import os
import cmd
import readline
import glob
import pickle
import configparser
import inspect
import pkg_resources
from . import match_model
from . import functions
from . import init_mm
from . import test_suite
from yolk import pypi
from pathlib import Path

def _append_slash_if_dir(p):
    if p and os.path.isdir(p) and p[-1] != os.sep:
        return p + os.sep
    else:
        return p


home = str(Path.home())
histfile = os.path.expanduser(home+'/.mm_history')
histfile_size = 1000


def MMV():
    version = pkg_resources.require("matchmakereft")[0].version
    return version

if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

class MatchMaker(cmd.Cmd):


    def __init__(self):
        cmd.Cmd.__init__(self)
        # we temporarily comment this region until we upload a new version to pypi
        print("Checking for updates.")  
        mmv = pypi.CheeseShop().query_versions_pypi("matchmakereft")[1][0]
        if mmv == MMV(): 
            print("matchmakereft is up-to-date.")  
        else:
            print("There is a new version of matchmakereft available, please update it using the --upgrade flag through pip3.")

        init_data = init_mm.initialise_mm()
        self.fr=init_data["fr_path"]
        self.wc=init_data["wc"]

        self.prompt = "matchmakereft> "
        self.intro = """
Welcome to matchmakereft
Please refer to xxx when using this code
"""

        # if mmv == MMV(): 
        #     self.intro  = "Welcome to matchmakereft"+MMV()+". matchmakereft is up-to-date."+"\n"  
        # else:
        #     self.intro  = "Welcome to matchmakereft"+MMV()+". There is a new version of matchmakereft available, please update it using the --upgrade flag through pip."+"\n"


    def do_check_linear_dependence(self, args):
        """Checks linear independence of the operators defined in an EFT."""
        if len(args) == 0:
            print("We need the address of the new physics model that you want to match")
        else:
            try:
                match_model.check_linear_depencence_amplitudes(args,self.wc)
            except Exception as E:
                print(E)

    def complete_check_linear_dependence(self, text, line, begidx, endidx):
        before_arg = line.rfind(" ", 0, begidx)
        if before_arg == -1:
            return # arg not found

        fixed = line[before_arg+1:begidx]  # fixed portion of the arg
        arg = line[before_arg+1:endidx]
        pattern = arg + '*'

        completions = []
        for path in glob.glob(pattern):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        for path in glob.glob(arg):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        return completions

    def do_match_model_to_eft(self, args):
        """Provides the complete one-loop matching between any matchmakereft UV model onto any matchmakereft eft."""
        try:
            self.do_match_model_to_eft_amplitudes(args)
            self.do_compute_wilson_coefficients(args)
        except Exception as E:
            pass

    def complete_match_model_to_eft(self, text, line, begidx, endidx):
        before_arg = line.rfind(" ", 0, begidx)
        if before_arg == -1:
            return # arg not found

        fixed = line[before_arg+1:begidx]  # fixed portion of the arg
        arg = line[before_arg+1:endidx]
        pattern = arg + '*'

        completions = []
        for path in glob.glob(pattern):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        for path in glob.glob(arg):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        return completions

    def do_match_model_to_eft_onlytree(self, args):
        """Provides the complete one-loop matching between any matchmakereft UV model onto any matchmakereft eft."""
        try:
            self.do_match_model_to_eft_amplitudes_onlytree(args)
            self.do_compute_wilson_coefficients(args)
        except Exception as E:
            pass

    def complete_match_model_to_eft_onlytree(self, text, line, begidx, endidx):
        before_arg = line.rfind(" ", 0, begidx)
        if before_arg == -1:
            return # arg not found

        fixed = line[before_arg+1:begidx]  # fixed portion of the arg
        arg = line[before_arg+1:endidx]
        pattern = arg + '*'

        completions = []
        for path in glob.glob(pattern):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        for path in glob.glob(arg):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        return completions

    def do_match_model_to_eft_amplitudes(self, args):
        """Provides the complete one-loop matching between any matchmakereft UV model onto any matchmakereft eft."""
        if len(args) == 0:
            print("We need the address of the new physics model that you want to match")
        else:
            try:
                match_model.match_model(*args.split())
            except Exception as E:
                # inspect.stack()[1].function is the function that calls match_model_to_eft_amplitudes
                # we raise an exception only when it is called from that function
                callingfunction=inspect.stack()[1].function
                if callingfunction in ["do_match_model_to_eft","do_compute_rge_model_to_eft"]:
                    print(E)
                    raise(E)
                print(E)

    def complete_match_model_to_eft_amplitudes(self, text, line, begidx, endidx):
        before_arg = line.rfind(" ", 0, begidx)
        if before_arg == -1:
            return # arg not found

        fixed = line[before_arg+1:begidx]  # fixed portion of the arg
        arg = line[before_arg+1:endidx]
        pattern = arg + '*'

        completions = []
        for path in glob.glob(pattern):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        for path in glob.glob(arg):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        return completions

    def do_match_model_to_eft_amplitudes_onlytree(self, args):
        """Provides the complete one-loop matching between any matchmakereft UV model onto any matchmakereft eft."""
        if len(args) == 0:
            print("We need the address of the new physics model that you want to match")
        else:
            try:
                match_model.match_model(*args.split(),True)
            except Exception as E:
                # inspect.stack()[1].function is the function that calls match_model_to_eft_amplitudes
                # we raise an exception only when it is called from that function
                if inspect.stack()[1].function == "do_match_model_to_eft_onlytree":
                    print(E)
                    raise(E)
                print(E)

    def complete_match_model_to_eft_amplitudes_onlytree(self, text, line, begidx, endidx):
        before_arg = line.rfind(" ", 0, begidx)
        if before_arg == -1:
            return # arg not found

        fixed = line[before_arg+1:begidx]  # fixed portion of the arg
        arg = line[before_arg+1:endidx]
        pattern = arg + '*'

        completions = []
        for path in glob.glob(pattern):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        for path in glob.glob(arg):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        return completions

    def do_create_model(self, args):
        """Generates the matchmakereft model from a FeynRules one"""
        if len(args) == 0:
            print("We need the address of the new physics model that you want to match")
        else:
            try:
                functions.create_model(args.split(), self.wc, self.fr)
            except Exception:
                pass

    def complete_create_model(self, text, line, begidx, endidx):
        before_arg = line.rfind(" ", 0, begidx)
        if before_arg == -1:
            return # arg not found

        fixed = line[before_arg+1:begidx]  # fixed portion of the arg
        arg = line[before_arg+1:endidx]
        pattern = arg + '*'

        completions = []
        for path in glob.glob(pattern):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        for path in glob.glob(arg):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        return completions

    def do_test_installation(self, args):
        """Check matchmakereft installation"""
        test_suite.test_installation(self.wc, self.fr)

    def do_compute_wilson_coefficients(self, args):
        """Computes the Wilson coefficients for an already matched MatchMaker model"""
        if len(args) == 0:
            print("We need the address of the new physics model that you want to match")
        else:
            functions.compute_wilson_coefficients(*args.split(), self.wc)

    def complete_compute_wilson_coefficients(self, text, line, begidx, endidx):
        before_arg = line.rfind(" ", 0, begidx)
        if before_arg == -1:
            return # arg not found

        fixed = line[before_arg+1:begidx]  # fixed portion of the arg
        arg = line[before_arg+1:endidx]
        pattern = arg + '*'

        completions = []
        for path in glob.glob(pattern):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        for path in glob.glob(arg):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        return completions



    def do_compute_rge_model_to_eft(self, args):
        """Computes the Wilson coefficients for an already matched MatchMaker model"""
        if len(args) == 0:
            print("We need the address of the new physics model that you want to match")
        else:
            try:
                self.do_match_model_to_eft_amplitudes(args)
                functions.compute_rge(*args.split(), self.wc)
            except Exception as E:
                pass

    def complete_compute_rge_model_to_eft(self, text, line, begidx, endidx):
        before_arg = line.rfind(" ", 0, begidx)
        if before_arg == -1:
            return # arg not found

        fixed = line[before_arg+1:begidx]  # fixed portion of the arg
        arg = line[before_arg+1:endidx]
        pattern = arg + '*'

        completions = []
        for path in glob.glob(pattern):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        for path in glob.glob(arg):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        return completions

    def do_clean_model(self, args):
        """Removes all calculations from previously matched model so that it can be matched again"""
        if len(args) == 0:
            print("We need the address of the new physics model that you want to clean")
        else:
            for fi in glob.glob(os.path.join(args,"*","proc*","*")):
                os.remove(fi)
            for fi in ['MatchingResult.dat','MatchingProblems.dat','RGEResult.dat']:
                if os.path.isfile(os.path.join(args,fi)):
                    os.remove((os.path.join(args,fi)))
            for fi in ['amplitudes.txt','canonicalnormalization.dat','classicaldimension.dat','EFTMatching.dat','wc2fields.txt']:
                if os.path.isfile(os.path.join(args,"QGRAF","model_data",fi)):
                    os.remove(os.path.join(args,"QGRAF","model_data",fi))

    def complete_clean_model(self, text, line, begidx, endidx):
        before_arg = line.rfind(" ", 0, begidx)
        if before_arg == -1:
            return # arg not found

        fixed = line[before_arg+1:begidx]  # fixed portion of the arg
        arg = line[before_arg+1:endidx]
        pattern = arg + '*'

        completions = []
        for path in glob.glob(pattern):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        for path in glob.glob(arg):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        return completions

    def do_copy_models(self, args):
        """Copy all the required files to create several MatchMaker models"""
        if os.path.isdir(args):
            functions.copy_models(args)
        else:
            print("We need the path of the directory where you want the models to be copied")

    def complete_copy_models(self, text, line, begidx, endidx):
        before_arg = line.rfind(" ", 0, begidx)
        if before_arg == -1:
            return # arg not found

        fixed = line[before_arg+1:begidx]  # fixed portion of the arg
        arg = line[before_arg+1:endidx]
        pattern = arg + '*'

        completions = []
        for path in glob.glob(pattern):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        for path in glob.glob(arg):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        return completions

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    def do_quit(self, args):
        """Exits from the console"""
        return -1

    ## Command definitions to support Cmd object functionality ##
    def do_EOF(self, args):
        """Exit on system end of file character"""
        return self.do_exit(args)

    def do_shell(self, args):
        """Pass command to a system shell when line begins with '!'"""
        os.system(args)

    def do_help(self, args):
        """Get help on commands
           'help' or '?' with no arguments prints a list of commands for which help is available
           'help <command>' or '? <command>' gives help on <command>
        """
        ## The only reason to define this method is for the help text in the doc string
        cmd.Cmd.do_help(self, args)

    ## Override methods in Cmd object ##
    def preloop(self):
        """Initialization before prompting user for commands.
           Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop(self)   ## sets up command completion

        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}

        if readline and os.path.exists(histfile):
            readline.read_history_file(histfile)



    def postloop(self):
        """Take care of any unfinished business.
           Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
        """
        cmd.Cmd.postloop(self)   ## Clean up command completion
        print("Exiting...")
        if readline:
            readline.set_history_length(histfile_size)
            readline.write_history_file(histfile)

    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
        """
        #self._hist += [ line.strip() ]
        return line

    def postcmd(self, stop, line):
        """If you want to stop the console, return something that evaluates to true.
           If you want to do some post command processing, do it here.
        """

        return stop

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        try:
            exec(line) in self._locals, self._globals
        except Exception as e:
            print(e.__class__, ":", e)


def MM():
    my_object = MatchMaker()
    my_object.cmdloop()
