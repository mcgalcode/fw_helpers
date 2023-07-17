from fireworks.core.launchpad import LaunchPad
from jobflow.settings import JobflowSettings
from jobflow.core.store import JobStore

from monty.json import MontyDecoder

import os

CONFIG_DIR_ENV_VAR = "FW_HELPERS_CONFIG_DIR"

def get_config_dir():
    dirname = os.getenv(CONFIG_DIR_ENV_VAR, None)
    if dirname is None:
        raise RuntimeError(f'No config directory specified for fw_helpers! Please define {CONFIG_DIR_ENV_VAR} in .bashrc or elsewhere')
    
def get_job_store():
    settings = JobflowSettings()
    store = settings.JOB_STORE
    store.connect()
    return store

def get_lpad():
    lpad = LaunchPad.auto_load()
    return lpad

def get_wflow_output_by_id(wflow_id, store: JobStore = None):
    lpad = get_lpad()
    wflow = lpad.get_wf_by_fw_id(wflow_id)
    return get_wflow_output(wflow, store)

def get_wflow_output(wflow, store: JobStore = None):
    if store is None:
        store = get_job_store()

    output = store.get_output(wflow.fws[-1].tasks[0].get('job').uuid, load=True)
    return load_output_from_dict(output)

def load_output_from_dict(output_dict):
    return MontyDecoder().process_decoded(output_dict)
