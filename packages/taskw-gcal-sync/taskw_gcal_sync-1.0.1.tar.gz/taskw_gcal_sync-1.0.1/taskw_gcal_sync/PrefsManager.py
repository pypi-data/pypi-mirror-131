import atexit
import os
import platform
import re
from pathlib import Path

import yaml

from taskw_gcal_sync.logger import logger


class PrefsManager:
    """Manage application-related preferences."""

    def __init__(self, app_name: str, config_file: str = None):
        """Initialization method.

        :param app_name: Name of the application the PrefsManager is running
                         under. This is used to define the path where the
                         configuration data is to be stored.
        :param config_file: Optional path to the configuration that is to be
                            used.  If that is not provided, configuration is
                            stored in the standard OS-dependent path. If
                            provided, the given configuration file is considered
                            read-only.

                            Default value: $HOME/.config/<appname>/config.yaml

        .. todo:: Verify that the directory structure is as it should be - on
                  directory structure creation
        """
        super(PrefsManager, self).__init__()

        if platform.system() not in ["Linux", "Darwin"]:
            raise NotImplementedError(
                f'PrefsManager does not support current OS [{platform.system() or "UNKNOWN"}]'
            )

        self.app_name = app_name
        self.cleaned_up = False

        # Preferences top-level directory
        self.prefs_dir = os.path.basename(re.sub(r"\.py$", "", self.app_name))
        if platform.system() == "Linux":
            self.prefs_dir_full = os.path.join(
                os.path.expanduser("~"), ".config", self.prefs_dir
            )
        elif platform.system() == "Darwin":
            self.prefs_dir_full = os.path.join(
                os.path.expanduser("~"), "Application Support", self.prefs_dir
            )
        else:
            raise RuntimeError("Invalid code path")

        logger.info(f"Initialising Preferences Manager -> {self.prefs_dir}")

        # static preferences file
        prefs_file_static = "cfg.yaml"
        self.prefs_file_static_full = os.path.join(self.prefs_dir_full, prefs_file_static)
        self.prefs_file_is_ro = False

        # Overwrite latter settings if config_file is manually specified
        if config_file:
            logger.debug("Custom configuration file is specified.")
            self.prefs_file_static_full = config_file
            self.prefs_file_is_ro = True

        # Indicates the latest fetched setting of the PrefsManager instance
        # This is use ful for updating that setting in a straightforward way
        self.latest_accessed = None

        self.conts = {}
        # Create or Load the preferences
        # If prefs_dir_full doesn't exist this along with all the files in it
        # should be created
        if os.path.isdir(self.prefs_dir_full):  # already there
            logger.info("Loading preferences from cache...")
        else:
            logger.info("Creating preferences directory from scratch...")
            os.makedirs(self.prefs_dir_full)
            Path(self.prefs_file_static_full).touch()

        # static preferences file
        with open(self.prefs_file_static_full, "r") as static_f:
            tmp = yaml.load(static_f, Loader=yaml.Loader)
            if tmp:
                self.conts = tmp

        atexit.register(self.cleanup)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.cleanup()

    def __contains__(self, key):
        return key in self.conts

    def __getitem__(self, key):
        self.latest_accessed = key
        return self.conts[key]

    def __setitem__(self, key, item):
        self.conts[key] = item

    def update_last(self, new_val):
        """Update the latest fetched setting."""
        if self.latest_accessed is None:
            raise RuntimeError(
                "update_last has been called even though no element has been accessed yet."
            )
        self.conts[self.latest_accessed] = new_val

    def cleanup(self):
        """Class destruction code."""
        if not self.cleaned_up:
            if not self.prefs_file_is_ro:
                logger.info("Updating preferences cache...")
                self.write_prefs(self.prefs_file_static_full)

                self.cleaned_up = True
            else:
                logger.debug("Skipping updating preferences file - Running in read-only mode")

    def write_prefs(self, p):
        """Helper class for writing the current cached settings to a file.

        :param p: Path to write the current settings. The given file is to
                  be overwritten
        :type p: str
        """
        with open(p, "w") as f:
            yaml.dump(self.conts, f, default_flow_style=False)
