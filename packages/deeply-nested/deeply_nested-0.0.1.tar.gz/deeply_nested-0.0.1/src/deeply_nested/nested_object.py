'''
pip installable library to work with deeply nested list or key value structures
'''
import json
import os
from pdb import set_trace as st

def get(data, dlist=[], path='', **kwargs):
    if isinstance(data, dict):
        for k, v in data.items():
            _path = f"{path}/{k}"
            if kwargs.get('key') == k:
                dlist.append((_path, v))
            elif kwargs.get('keypath') == _path:
                dlist.append(((_path, v)))
            else:
                get(v, dlist, path=_path, **kwargs)
    elif isinstance(data, (list, tuple)):
        for i, ditem in enumerate(data):
            _path = f"{path}[{i}]"
            if kwargs.get('keypath')==_path:
                dlist.append((_path, ditem))
            get(ditem, dlist, path=_path, **kwargs)
    return dlist[0] if len(dlist)==1 else dlist

def paths(data, pathlist=[], parent="", **kwargs):
    if isinstance(data, dict):
        for k, v in data.items():
            pstring = f"{parent}/{k}"
            pathlist.append(pstring)
            paths(v, pathlist, pstring)
    elif isinstance(data, (list, tuple)):
        for i, ditem in enumerate(data):
            pstring = f"{parent}[{i}]"
            pathlist.append(pstring)
            paths(ditem, pathlist, pstring)
    return pathlist      

class NestedObject:
    def __init__(self, obj=None):
        self._data = obj
        self._paths = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, d):
        if isinstance(d, (dict, list, tuple)):
            self._data = d
        elif isinstance(d, str) and os.path.isfile(d):
            with open(d) as f:
                self._data = json.load(f)
        else:
            raise Exception("Invalid data type, Expecting either dict, list or tuple")

    def _getipath(self, keypath, v=[]):
        _tempkp = keypath.split('[i]')[0]
        if _tempkp:
            _tempv = get(self._data, dlist=[], path='', keypath=_tempkp)
            for i in range(len(_tempv[1])):
                _kp = keypath.replace('[i]',f"[{i}]")
                _v = get(self._data, dlist=[], path='', keypath=_kp)
                v.append(_v)
        else:
            if isinstance(self._data, list):
                for i in range(len(self._data)):
                    _kp = keypath.replace('[i]',f"[{i}]")
                    _v = get(self._data, dlist=[], path='', keypath=_kp)
                    v.append(_v)
        return v

    def get(self,v=[],**kwargs):
        if kwargs.get('key'):
            v = get(self._data, dlist=[], path='', key = kwargs['key'])
        if kwargs.get('keypath'):
            keypath = kwargs.get('keypath')
            if '[i]' in keypath:
                v = self._getipath(keypath)
            else:
                v = get(self._data, dlist=[], path='', keypath=keypath)
        return v if v else None
    
    @property
    def paths(self, **kwargs):
        if not self._paths:
            self._paths = paths(self._data)
        return self._paths

    def keys(self):
        return self._paths

    def items(self, **kwargs):
        items = [self.get(keypath=k) for k in self.paths]
        return items
    
    def __repr__(self):
        return self._data

    def __str__(self):
        return json.dumps(self._data)

if __name__ == "__main__":
    d = NestedObject()
    d.data = './tests/testdata/sample.json'

    # print(d.get(key='city'))
    # print(d.get(keypath='[5]'))
    # print(d.get(keypath='[i]'))
    # print(len(d.keys()))
    # print(d.items())
    # fp = './tests/testdata/sample.json'
    # with open(fp) as f:
    #     jdump = json.load(f)
    #     d = NestedObject(jdump)
    #     print(d.items())
        # print(len(d.items()))
        # print(d.keys())
        # # st()
    # del d
        
        # st()