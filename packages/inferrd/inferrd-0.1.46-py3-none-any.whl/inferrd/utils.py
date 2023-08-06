import zipfile
import os
from easysettings import EasySettings
from pathlib import Path
import requests
import glob
import sys
import fnmatch
import pandas as pd
import numpy as np
import json

try:
    from importlib import metadata
except ImportError: # for Python<3.8
    import importlib_metadata as metadata

api_host = 'https://api.inferrd.com'
#api_host = 'http://localhost:3000'

IN_COLAB = False
try:
  import google.colab
  IN_COLAB = True
except:
  IN_COLAB = False

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            filePath = os.path.join(root, file)
            inZipPath = os.path.relpath(os.path.join(root, file), os.path.join(path, '..'))
            # remove base folder
            ziph.write(filePath, inZipPath.replace(path.split('/')[-1] + '/', ''))

def add_files_to_zip(ziph, **kwargs):
  filePaths = []

  if 'include' in kwargs:
    # include all files
    for includePath in kwargs['include']:
      for name in glob.glob(includePath, recursive=True):
        isExcluded = False

        if 'exclude' in kwargs:
          for excluded in kwargs['exclude']:
            if fnmatch.fnmatch(name, excluded):
              isExcluded = True

        if not isExcluded:
          filePaths.append(name)

  for filePath in filePaths:
    print('> Zipping {0}'.format(filePath))
    isDir = os.path.isdir(filePath)

    if isDir:
      zipdir(filePath, ziph)
    else:
      ziph.write(filePath, filePath)

def set_api_host(host):
  api_host = host

def get_api_host():
  return api_host

def auth(key):
  '''
  Authenticates the user with Inferrd.com.
  It'll raise an error if the token is invalid.
  '''
  settings = getEasySettings()

  # it should try the key to make sure it works.
  r = requests.get(api_host + '/me', headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + key})

  if r.status_code != 200:
    raise Exception('API Key in valid.')

  email = r.json()['email']

  print('> Logged in as {0}'.format(email))

  settings.set('api_key', key)
  settings.save()

def getEasySettings():
  # google collab returns /root for Path.home() and it breaks
  settings = EasySettings(str(Path() if IN_COLAB else Path.home()) + "/.inferrd.conf")
  return settings

def getApiKey():
  settings = getEasySettings()
  return settings.get('api_key')

def get_model(name):
  api_key = getApiKey()

  r = requests.get(get_api_host() + '/service/find/' + name, headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})

  model = r.json()

  if 'id' not in model:
    raise Exception("Model \"{0}\" not found in your Inferrd account. Please double check spelling.".format(name))

  return model

def is_model_framework(model, frameworkName):
  return model['desiredStack']['humanReadableId'].startswith(frameworkName)

def new_version(modelId,  **kwargs):
  api_key = getApiKey()

  body = {}

  if 'test_inputs' in kwargs and kwargs['test_inputs'] is not None:
    body['testInputs'] = kwargs['test_inputs']

  r = requests.post(api_host + '/service/' + modelId + '/versions', headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key}, json=body)

  return r.json()

def new_job(job_name, team_name, **kwargs):
  gpu_ram = 2000
  cpu_ram = 4000

  if 'cpu_ram' in kwargs:
    cpu_ram = kwargs['cpu_ram']

  if 'gpu_ram' in kwargs:
    gpu_ram = kwargs['gpu_ram']

  api_key = getApiKey()

  team = get_team(team_name)

  r = requests.post(get_api_host() + '/team/' + team['id'] + '/jobs', json={
    "name": job_name,
    "cpuRamMb": cpu_ram,
    "gpuRamMb": gpu_ram
  }, headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})

  job = r.json()

  if 'error' in job:
    raise Exception(job['message'])

  return job

def run_job(jobId):
  api_key = getApiKey()
  r = requests.post(get_api_host() + '/job/' + jobId + '/run', headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})
  job = r.json()

  if 'error' in job:
    raise Exception(job['message'])

def get_team(name):
  api_key = getApiKey()

  r = requests.get(get_api_host() + '/team/find/' + name, headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})
  team = r.json()

  if 'id' not in team:
    raise Exception("Team \"{0}\" not found in your Inferrd account. Please double check spelling.".format(name))

  return team


def deploy_version(versionId, **kwargs):
  api_key = getApiKey()

  obj = {
    "sampleInputs": kwargs['sampleInputs'] if 'sampleInputs' in kwargs else None
  }

  r = requests.post(api_host + '/version/' + versionId + '/deploy', headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key}, json=obj)

  return r.json()

def find_version(modelId, name):
  api_key = getApiKey()

  r = requests.get(api_host + '/service/' + modelId + '/versions/find/' + name, headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})

  return r.json()

def generate_requirements_file():
  dists = metadata.distributions()

  with open('./reqs.txt', 'a') as requirementsFile:
    for dist in dists:
      name = dist.metadata["Name"]
      version = dist.version

      # don't install version 0.0.0
      if str(version) == "0.0.0":
        continue

      # don't install colab packages
      if "colab" in name:
        continue

      requirementsFile.write(f'{name}=={version}\n')

# this validates that the inputs provided
# to inferrd are either Numpy of Pandas DataFrames
def validate_inputs_and_return(X):
  if isinstance(X, np.ndarray):
    test_inputs = X[:5]

    # transform the input to a list
    return test_inputs.tolist()

  if isinstance(X, pd.DataFrame):
    test_inputs = X.head(5)

    # transform the input to a list of records
    return test_inputs.to_dict(orient='records')

  if isinstance(X, pd.Series):
    test_inputs = X[:5]

    # transform the input to a list of records
    return test_inputs.tolist()

  raise Exception('The test inputs need to be either a Numpy array or a DataFrame. Found {0}'.format(type(X)))