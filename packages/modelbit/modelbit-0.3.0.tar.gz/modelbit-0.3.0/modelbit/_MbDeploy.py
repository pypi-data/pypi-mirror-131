class _MbDeploy:
  _mbMain = None
  
  def __init__(self, mbMain):
    self._mbMain = mbMain

  def _deploy(self, func, name, warehouseName):
    import inspect
    
    try:
      resp = self._mbMain._getJsonOrPrintError("jupyter/v1/deployments/create", { "deployment": {
        "funcSource": inspect.getsource(func),
        "funcName": func.__name__,
        "arguments": list(func.__code__.co_varnames[:func.__code__.co_argcount] or []),
        "defaultArgVals": list(func.__defaults__ or []),
        "name": name,
        "warehouseName": warehouseName
      }})
      if resp and resp["deployOverviewUrl"]:
        self._mbMain._printMk(f'Your deployment for "{name}" will be ready in about 1 minute.')
        self._mbMain._printMk(f'<a href="{resp["deployOverviewUrl"]}" target="_blank">View status and integration options.</a>')
    except Exception as e:
      print(f'Please supply a function that can be deployed. ({str(e)})')
      return
