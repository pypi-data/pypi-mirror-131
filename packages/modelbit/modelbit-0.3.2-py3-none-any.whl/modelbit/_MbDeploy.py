class _MbDeploy:
  _mbMain = None
  
  def __init__(self, mbMain):
    self._mbMain = mbMain

  def _deploy(self, func, name, warehouseName, args, deps):
    import inspect, traceback
    
    try:
      resolvedName = name or func.__name__
      resp = self._mbMain._getJsonOrPrintError("jupyter/v1/deployments/create", { "deployment": {
        "name": resolvedName,
        "warehouseName": warehouseName,
        "pyState": {
          "source": inspect.getsource(func),
          "name": func.__name__,
          "argNames": list(func.__code__.co_varnames[:func.__code__.co_argcount] or []),
          # "defaultArgVals": list(func.__defaults__ or []),
          "deployVars": self._pickleArgKeys(args),
          "deployVarsDesc": self._strArgDesc(args),
          "deps": deps,
        }
      }})
      if resp and resp["deployOverviewUrl"]:
        self._mbMain._printMk(f'Your deployment for "{resolvedName}" will be ready in about 1 minute.')
        self._mbMain._printMk(f'<a href="{resp["deployOverviewUrl"]}" target="_blank">View status and integration options.</a>')
    except Exception as e:
      print(f'Please supply a function that can be deployed. ({str(e)})')
      traceback.print_exc()
      return

  def _pickleArgKeys(self, args):
    import pickle, codecs
    if type(args) is not dict: raise Exception(f'Args must be a dictionary.')
    if "row" in args: raise Exception(f'Args should not include "row". It will be supplied automatically at runtime.')
    newDict = {}
    for k, v in args.items():
      if type(k) is not str: raise Exception(f'Arg key "{str(k)} needs to be a string."')
      newDict[k] = codecs.encode(pickle.dumps(v), "base64").decode()
    return newDict

  def _strArgDesc(self, args):
    newDict = {}
    for k, v in args.items():
      newDict[k] = str(v)
    return newDict
