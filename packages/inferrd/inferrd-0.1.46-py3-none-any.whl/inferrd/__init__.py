import requests
import json
from easysettings import EasySettings
import sys
from pathlib import Path
import shutil
import dill
import os
from joblib import dump
import zipfile
import pandas as pd
import numpy as np

from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

from .utils import zipdir, is_model_framework, validate_inputs_and_return, add_files_to_zip, getApiKey, run_job, new_job, get_api_host, generate_requirements_file, auth, set_api_host,  get_model, new_version, deploy_version, find_version

settings = EasySettings(str(Path.home()) + "/.inferrd.conf")

__all__ = [
    'indextools',
    'doctools'
]

def __set_api_host(host):
  set_api_host(host)
  print('API Endpoint set to ' + host)

def sizeof_fmt(num, suffix='B'):
  for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
    if abs(num) < 1024.0:
      return "%3.1f%s%s" % (num, unit, suffix)
    num /= 1024.0
  return "%.1f%s%s" % (num, 'Yi', suffix)

# arguments
# includeFailures=True/False
def get_requests(name, **kwargs):
  model = get_model(name)
  api_key = getApiKey()

  includeFailures = False
  version = None
  limit = 100
  page = 0

  if 'limit' in kwargs:
    limit = kwargs['limit']

  if 'page' in kwargs:
    page = kwargs['page']

  if 'includeFailures' in kwargs:
    includeFailures = kwargs['includeFailures']

  if 'version' in kwargs:
    v = find_version(model['id'], kwargs['version'])
    version = v['id']

  url = get_api_host() + '/service/' + model['id'] + '/requests?' + ('responseStatus=200&' if not includeFailures else '') + 'limit=' + str(limit) + '&page=' + str(page) + ('&version=' + version if version else '')

  r = requests.get(url, headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})

  return r.json()

# ------ JOBS
def run(team_name, job, **kwargs):
  if(getApiKey() == ''):
    raise Exception('No api key. Use inferrd.auth() first.')

  if 'name' not in kwargs:
    raise Exception('Missing argument "name". Your job needs a name.')

  gpu_ram = 2000
  cpu_ram = 4000

  if 'cpu_ram' in kwargs:
    cpu_ram = kwargs['cpu_ram']

  if 'gpu_ram' in kwargs:
    gpu_ram = kwargs['gpu_ram']
  
  print('> Packaging your job')

  if os.path.exists('./job.dill'):
    os.remove('./job.dill')

  dill.dump(job, open('./job.dill', mode='wb'), byref=False, recurse=True)

  if os.path.exists('./reqs.txt'):
    os.remove('./reqs.txt')

  generate_requirements_file()

  print('> Zipping job for upload')

  zipf = zipfile.ZipFile('job.zip', 'w', zipfile.ZIP_DEFLATED)
  zipf.write('./job.dill', './job.dill')
  zipf.write('./reqs.txt', './requirements.txt')

  if 'includeFiles' in kwargs:
    add_files_to_zip(zipf, include=kwargs['includeFiles'])

  if 'setup' in kwargs:
    setupFile = open('./setup.sh', 'w')
    setupFile.write(kwargs['setup'])
    setupFile.close()
    zipf.write('./setup.sh', './setup.sh')

  zipf.close()

  job = new_job(
    kwargs['name'],
    team_name,
    gpu_ram=gpu_ram,
    cpu_ram=cpu_ram
  )

  model_size = Path('./job.zip').stat().st_size
  print('> Uploading job ({0})'.format(sizeof_fmt(model_size)), flush=True)
  f = open("./job.zip", 'rb')

  with tqdm(total=model_size, unit="B", unit_scale=True, unit_divisor=1024, ncols=100) as t:
    wrapped_file = CallbackIOWrapper(t.update, f, "read")
    r = requests.put(job['signedUpload'], data=wrapped_file, headers={'Content-Type': 'application/zip'})

  print('> Starting job ' + job['name'])
  run_job(job['id'])

  os.remove('./job.zip')
  os.remove('./job.dill')
  os.remove('./reqs.txt')

  if 'setup' in kwargs:
    os.remove('./setup.sh')

# ------ CUSTOM MODEL
def deploy(model, **kwargs):
  if(getApiKey() == ''):
    raise Exception('No api key. Use inferrd.auth() first.')

  # also checks that python is compatible
  if sys.version_info < (3, 7) or sys.version_info >= (3, 8):
    raise Exception('Inferrd is incomptible with your Python (version ' + str(sys.version_info.major) + '.' + str(sys.version_info.minor) +'.' + str(sys.version_info.micro) +'). Only Python 3.7.x is supported.')

  prediction_fn = model
  name = kwargs['name']
  
  if prediction_fn is None:
    raise Exception('Empty function model. Make sure the first argument is a function.')

  model = get_model(name)

  if not is_model_framework(model, 'custom'):
    raise Exception('The model is not a Custom model.')

  version = new_version(model['id'])

  print('> Packaging your model for deployment')

  if os.path.exists('./model.dill'):
    os.remove('./model.dill')

  dill.dump(prediction_fn, open('./model.dill', mode='wb'), byref=False, recurse=True)

  if os.path.exists('./reqs.txt'):
    os.remove('./reqs.txt')

  generate_requirements_file()

  print('> Zipping model for upload')

  zipf = zipfile.ZipFile('model.zip', 'w', zipfile.ZIP_DEFLATED)
  zipf.write('./model.dill', './model.dill')
  zipf.write('./reqs.txt', './requirements.txt')

  if 'includeFiles' in kwargs:
    add_files_to_zip(zipf, include=kwargs['includeFiles'])
  else:
    print('> Zipping all Python files in directory. To include more files, use the `includeFiles` option.')
    add_files_to_zip(zipf, include=['**/*.py', '*.py'])

  if 'setup' in kwargs:
    setupFile = open('./setup.sh', 'w')
    setupFile.write(kwargs['setup'])
    setupFile.close()
    zipf.write('./setup.sh', './setup.sh')

  zipf.close()
  
  # upload to storage
  model_size = Path('./model.zip').stat().st_size
  print('> Uploading model ({0})'.format(sizeof_fmt(model_size)), flush=True)
  f = open("./model.zip", 'rb')

  with tqdm(total=model_size, unit="B", unit_scale=True, unit_divisor=1024, ncols=100) as t:
    wrapped_file = CallbackIOWrapper(t.update, f, "read")
    r = requests.put(version['signedUpload'], data=wrapped_file, headers={'Content-Type': 'application/zip'})

  print('> Deploying version v' + str(version['number']))
  deploy_version(version['id'])

  os.remove('./model.zip')
  os.remove('./model.dill')
  os.remove('./reqs.txt')

  if 'setup' in kwargs:
    os.remove('./setup.sh')

  print('> Your model is now deploying!')

# ------ TENSORFLOW
def deploy_tf(tf_model, name):
  if(getApiKey() == ''):
    raise Exception('No api key. Use inferrd.auth() first.')

  if tf_model is None:
    raise Exception('Empty tensorflow model. Make sure the first argument is a TensorFlow v2 model.')

  if not is_model_framework(model, 'tensorflow'):
    raise Exception('The model is not a TensorFlow v2 model.')

  model = get_model(name)

  print('> Saving model to folder')

  version = new_version(model['id'])

  if os.path.exists('./inferrd-model'):
    shutil.rmtree('./inferrd-model')

  import tensorflow as tf

  tf.saved_model.save(tf_model, './inferrd-model')
    
  print('> Zipping model for upload')

  if os.path.exists('./model.zip'):
    os.remove('./model.zip')

  zipf = zipfile.ZipFile('model.zip', 'w', zipfile.ZIP_DEFLATED)
  zipdir('./inferrd-model', zipf) 
  zipf.close()

  # upload to storage
  model_size = Path('./model.zip').stat().st_size
  print('> Uploading model ({0})'.format(sizeof_fmt(model_size)), flush=True)
  f = open("./model.zip", 'rb')
  
  with tqdm(total=model_size, unit="B", unit_scale=True, unit_divisor=1024, ncols=100) as t:
    wrapped_file = CallbackIOWrapper(t.update, f, "read")
    r = requests.put(version['signedUpload'], data=wrapped_file, headers={'Content-Type': 'application/zip'})

  print('> Deploying version v' + str(version['number']))
  deploy_version(version['id'])

  shutil.rmtree('./inferrd-model')
  #os.remove('./model.zip')

  print('> TensorFlow Model deployed')

# ------ SCIKIT
def deploy_scikit(scikit_model, name, **kwargs):
  if(getApiKey() == ''):
    raise Exception('No api key. Use inferrd.auth() first.')

  if scikit_model is None:
    raise Exception('Empty Scikit model. Make sure the first argument is a Scikit Learn model.')

  model = get_model(name)

  if not is_model_framework(model, 'sklearn'):
    raise Exception('The model is not a Scikit-Learn model.')

  print('> Saving model to folder')

  test_inputs = None

  if 'X' in kwargs:
    test_inputs = validate_inputs_and_return(kwargs['X'])

  version = new_version(model['id'], test_inputs=test_inputs)

  if os.path.exists('./inferrd-scikit.joblib'):
    os.remove('./inferrd-scikit.joblib')

  dump(scikit_model, './inferrd-scikit.joblib')

  print('> Zipping model for upload')

  if os.path.exists('./model.zip'):
    os.remove('./model.zip')

  zipf = zipfile.ZipFile('model.zip', 'w', zipfile.ZIP_DEFLATED)
  zipf.write('./inferrd-scikit.joblib', './model.joblib')
  zipf.close()

  # upload to storage
  model_size = Path('./model.zip').stat().st_size
  print('> Uploading model ({0})'.format(sizeof_fmt(model_size)), flush=True)
  f = open("./model.zip", 'rb')
  
  with tqdm(total=model_size, unit="B", unit_scale=True, unit_divisor=1024, ncols=100) as t:
    wrapped_file = CallbackIOWrapper(t.update, f, "read")
    r = requests.put(version['signedUpload'], data=wrapped_file, headers={'Content-Type': 'application/zip'})

  print('> Deploying version v' + str(version['number']))
  deploy_version(version['id'])

  os.remove('./inferrd-scikit.joblib')
  os.remove('./model.zip')

  print('> Scikit Model deployed')

# ------ SPACY
def deploy_spacy(nlp_model, name):
  if(getApiKey() == ''):
    raise Exception('No api key. Use inferrd.auth() first.')

  print('> Saving model to disk')

  if nlp_model is None:
    raise Exception('Empty spaCy model. Make sure the first argument is a spaCy model.')

  model = get_model(name)

  if not is_model_framework(model, 'spacy'):
    raise Exception('The model is not a Spacy model.')

  if os.path.exists('./inferrd-model'):
    shutil.rmtree('./inferrd-model')

  nlp_model.to_disk('./inferrd-model')
    
  print('> Zipping model for upload')

  if os.path.exists('./model.zip'):
    os.remove('./model.zip')

  zipf = zipfile.ZipFile('model.zip', 'w', zipfile.ZIP_DEFLATED)
  zipdir('./inferrd-model', zipf) 
  zipf.close()

  # upload to storage
  version = new_version(model['id'])
  model_size = Path('./model.zip').stat().st_size
  print('> Uploading model ({0})'.format(sizeof_fmt(model_size)), flush=True)
  f = open("./model.zip", 'rb')

  with tqdm(total=model_size, unit="B", unit_scale=True, unit_divisor=1024, ncols=100) as t:
    wrapped_file = CallbackIOWrapper(t.update, f, "read")
    r = requests.put(version['signedUpload'], data=wrapped_file, headers={'Content-Type': 'application/zip'})

  print('> Deploying version v' + str(version['number']))
  deploy_version(version['id'])

  shutil.rmtree('./inferrd-model')
  os.remove('./model.zip')

  print('> spaCy model deployed')
  
# ------ KERAS
def deploy_keras(keras_model, name):
  if(getApiKey() == ''):
    raise Exception('No api key. Use inferrd.auth() first.')

  if keras_model is None:
    raise Exception('Empty Kears model. Make sure the first argument is a Keras model.')

  from tensorflow import keras

  model = get_model(name)

  if not is_model_framework(model, 'keras'):
    raise Exception('The model is not a Keras model.')

  print('> Saving model to disk')

  if os.path.exists('./_inferrd_keras.h5'):
    os.remove('./_inferrd_keras.h5')

  # by default use the h5 format, otherwise it'd be a tensorflow deploy
  keras_model.save('_inferrd_keras.h5', save_format='h5')

  print('> Zipping model for upload')

  if os.path.exists('./model.zip'):
    os.remove('./model.zip')

  zipf = zipfile.ZipFile('model.zip', 'w', zipfile.ZIP_DEFLATED)
  zipf.write('./_inferrd_keras.h5', './model.h5')
  zipf.close()

  # upload to storage
  version = new_version(model['id'])
  model_size = Path('./model.zip').stat().st_size
  print('> Uploading model ({0})'.format(sizeof_fmt(model_size)), flush=True)
  f = open("./model.zip", 'rb')

  with tqdm(total=model_size, unit="B", unit_scale=True, unit_divisor=1024, ncols=100) as t:
    wrapped_file = CallbackIOWrapper(t.update, f, "read")
    r = requests.put(version['signedUpload'], data=wrapped_file, headers={'Content-Type': 'application/zip'})

  print('> Deploying version v' + str(version['number']))
  deploy_version(version['id'])
  os.remove('./model.zip')
  os.remove('./_inferrd_keras.h5')

  print('> spaCy model deployed')


def get_request_history(apiKey, kwargs):
  print('Getting request')

def call_model(serveKey, payload):
  r = requests.post(get_api_host() + '/infer/' + serveKey + '/predict', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
  return r.json()

def get(modelName):
  model = get_model(modelName)
  serveKey = model['key']

  def infer(payload):
    headers = {'Content-Type': 'application/json'}

    # transform numpy arrays to lists
    if isinstance(payload, np.ndarray):
      payload = payload.tolist()

    # transform data frames to list
    if isinstance(payload, pd.DataFrame):
      payload = payload.to_dict(orient='records')

    # transform data frames to list
    if isinstance(payload, pd.Series):
      payload = payload.tolist()
    
    # pass in the token when you can, to authenticate requests
    if(getApiKey() != ''):
      headers['Authorization'] = 'Token ' + getApiKey()

    r = requests.post(get_api_host() + '/infer/' + serveKey + '/predict', data=json.dumps(payload), headers=headers)
    return r.json()

  return infer