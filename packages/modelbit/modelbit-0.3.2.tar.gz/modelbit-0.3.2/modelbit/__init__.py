__version__ = "0.3.2"
__author__ = 'Modelbit'

from ._MbDatasets import _MbDatasets
from ._MbDeploy import _MbDeploy
from ._MbWarehouses import _MbWarehouses
class __Modelbit:

  _API_HOST = 'https://app.modelbit.com/'
  _LOGIN_HOST = _API_HOST
  _API_URL = None
  _MAX_DATA_LEN = 10000000
  _state = {
    "notebookEnv": {
      "userEmail": "",
      "signedToken": "",
      "uuid": "",
      "authenticated": False,
      "workspaceName": "",
      "mostReventVersion": ""
    }
  }
    
  def __init__(self):
    import os
    if os.getenv('MB_JUPYTER_API_HOST'):
      self._API_HOST = os.getenv('MB_JUPYTER_API_HOST')
    if os.getenv('MB_JUPYTER_LOGIN_HOST'):
      self._LOGIN_HOST = os.getenv('MB_JUPYTER_LOGIN_HOST')
    self._API_URL = f'{self._API_HOST}api/'

  def _isAuthenticated(self, testRemote=True):
    if testRemote and not self._isAuthenticated(False):
      data = self._getJson("jupyter/v1/login")
      if 'error' in data:
        self._printMk(f'**Error:** {data["error"]}')
        return False
      self._state["notebookEnv"] = data["notebookEnv"]
      return self._isAuthenticated(False)
    return self._state["notebookEnv"]["authenticated"]

  def _getJson(self, path, body = {}):
    import requests, json
    try:
      data = {
        "requestToken": self._state["notebookEnv"]["signedToken"],
        "version": __version__
      }
      data.update(body)
      dataLen = len(json.dumps(data))
      if (dataLen > self._MAX_DATA_LEN):
        return {"error": f'API Error: Request is too large. (Request is{self._sizeof_fmt(dataLen)} Limit is{self._sizeof_fmt(self._MAX_DATA_LEN)})'}
      with requests.post(f'{self._API_URL}{path}', json=data) as url:
        return url.json()
    except BaseException as err:
      return {"error": f'Unable to reach Modelbit. ({err})'}

  def _getJsonOrPrintError(self, path, body = {}):
    if not self._isAuthenticated():
      self._login()
      return False

    data = self._getJson(path, body)
    if 'error' in data:
      self._printMk(f'**Error:** {data["error"]}')
      return False
    return data

  def _printMk(self, str):
    from IPython.display import display, Markdown
    display(Markdown(str))

  def _maybePrintUpgradeMessage(self):
    latestVer = self._state["notebookEnv"]["mostRecentVersion"]
    nbVer = __version__
    if latestVer and latestVer.split('.') > nbVer.split('.'):
      pipCmd = '<span style="color:#E7699A; font-family: monospace;">pip install --upgrade modelbit</span>'
      self._printMk(f'Please run {pipCmd} to upgrade to the latest version. ' + 
        f'(Installed: <span style="font-family: monospace">{nbVer}</span>. ' + 
        f' Latest: <span style="font-family: monospace">{latestVer}</span>)')

  def _printAuthenticatedMsg(self):
    connectedTag = '<span style="color:green; font-weight: bold;">connected</span>'
    email = self._state["notebookEnv"]["userEmail"]
    workspace = self._state["notebookEnv"]["workspaceName"]
    
    self._printMk(f'You\'re {connectedTag} to Modelbit as {email} in the \'{workspace}\' workspace.')
    self._maybePrintUpgradeMessage()

  def _login(self):
    if self._isAuthenticated():
      self._printAuthenticatedMsg()
      return

    displayUrl = f'modelbit.com/t/{self._state["notebookEnv"]["uuid"]}'
    linkUrl = f'{self._LOGIN_HOST}/t/{self._state["notebookEnv"]["uuid"]}'
    aTag = f'<a style="text-decoration:none;" href="{linkUrl}" target="_blank">{displayUrl}</a>'
    helpTag = '<a style="text-decoration:none;" href="/" target="_blank">Learn more.</a>'
    self._printMk('**Connect to Modelbit**<br/>' +
      f'Open {aTag} to authenticate this kernel, then re-run this cell. {helpTag}')
    self._maybePrintUpgradeMessage()

  # From https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
  def _sizeof_fmt(self, num):
    if type(num) != int: return ""
    for unit in ["", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]:
        if abs(num) < 1000.0:
            return f"{num:3.0f} {unit}"
        num /= 1000.0
    return f"{num:.1f} YB"

  # Public APIs
  def datasets(self): return _MbDatasets(self)
  def get_dataset(self, dataset_name): return _MbDatasets(self).get(dataset_name)
  def warehouses(self): return _MbWarehouses(self)
  def deploy(self, func, name=None, warehouse=None, args={}, deps=[]): return _MbDeploy(self)._deploy(func, name, warehouse, args, deps)


def login():
  _modelbit = __Modelbit()
  _modelbit._login()
  return _modelbit
