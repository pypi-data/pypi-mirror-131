

""""""  # start delvewheel patch
def _delvewheel_init_patch_0_0_17():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, '.'))
    if sys.version_info[:2] >= (3, 8):
        if os.path.exists(os.path.join(sys.base_prefix, 'conda-meta')):
            # backup the state of the environment variable CONDA_DLL_SEARCH_MODIFICATION_ENABLE
            conda_dll_search_modification_enable = os.environ.get("CONDA_DLL_SEARCH_MODIFICATION_ENABLE")
            os.environ['CONDA_DLL_SEARCH_MODIFICATION_ENABLE']='1'

        os.add_dll_directory(libs_dir)

        if os.path.exists(os.path.join(sys.base_prefix, 'conda-meta')):
            # restore the state of the environment variable CONDA_DLL_SEARCH_MODIFICATION_ENABLE
            if conda_dll_search_modification_enable is None:
                os.environ.pop("CONDA_DLL_SEARCH_MODIFICATION_ENABLE", None)
            else:
                os.environ["CONDA_DLL_SEARCH_MODIFICATION_ENABLE"] = conda_dll_search_modification_enable
    else:
        from ctypes import WinDLL
        with open(os.path.join(libs_dir, '.load-order-saxonpy-0.0.2')) as file:
            load_order = file.read().split()
        for lib in load_order:
            WinDLL(os.path.join(libs_dir, lib))


_delvewheel_init_patch_0_0_17()
del _delvewheel_init_patch_0_0_17
# end delvewheel patch

# setting the saxonc_home.
def set_saxonc_home():
	import os
	if os.getenv('SAXONC_HOME') != None and "saxonc_home" in os.getenv('SAXONC_HOME'):
		pass
	else:
		main_dir = os.path.dirname(os.path.abspath(__file__))
		saxonc_home = "".join([main_dir, "/saxonc_home"])
		os.environ['SAXONC_HOME'] = saxonc_home
set_saxonc_home()
del set_saxonc_home
from saxonc import *