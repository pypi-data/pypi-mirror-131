from typing import Any, Dict, List, Optional
from functools import cached_property,wraps
from pydantic import BaseModel
import atexit
import httpx

def kill_go():
    import psutil
    for p in psutil.process_iter():
        if "pygobin" in p.name():
            proc = psutil.Process(p.pid)
            proc.terminate()

atexit.register(kill_go)

def auto_abort(func):
    @wraps(func)
    def instead(self,*args,**kwd):
        try:
            res = func(self,*args,**kwd)
            return res
        except httpx.ConnectError:
            raise
        except Exception as e:
            kill_go()
            raise e
        finally:
            ...
    return instead


class XlService(BaseModel):

    file_name:str

    class Config:
        # arbitrary_types_allowed = True
        keep_untouched = (cached_property,)

    @cached_property
    @auto_abort
    def api(self):
        # host = globals()["HOST"]
        # info = globals()["service_pool"][self.file_name]
        from .core import HOST,service_pool
        info = service_pool[self.file_name]
        return f"{HOST}:{info.port}/{self.schema()['title']}"

    @auto_abort
    def get(self,data:Dict={}):
        d = self.dict()
        if data:
            d.update(data)
        res = httpx.get(self.api,params=d)
        return res.json()

class Hello(XlService):
    ...

class Save(XlService):
    ...

class SaveAs(XlService):
    path:str

class Close(XlService):
    ...

class AddSheet(XlService):
    sheet_name:str

class DeleteSheet(XlService):
    sheet_name:str

class GetSheet(XlService):
    sheet_name:str

class GetSheets(XlService):
    ...


class SheetService(BaseModel):
    sheet_name:str
    file_name:str

    class Config:
        # arbitrary_types_allowed = True
        keep_untouched = (cached_property,)

    @auto_abort
    def get(self,data:dict={}):
        d = self.dict()
        if data:
            d.update(data)
        res = httpx.get(self.api,params=d,timeout=None)
        return res.json()
    
    @auto_abort
    def post(self,data:dict={}):
        d = {**self.dict(),**data}
        res = httpx.post(self.api,json=d,timeout=None)
        return res.json()


    @cached_property
    def api(self):
        from .core import HOST,service_pool
        info = service_pool[self.file_name]
        return f"{HOST}:{info.port}/{self.schema()['title']}"


class CellAxis(str):
    ...


class GetRows(SheetService):
    ...

class GetCols(SheetService):
    ...

class WriteRows(SheetService):
    rows:Dict

class GetCell(SheetService):
    axis:str

class SetCell(SheetService):
    axis:str
    val:Any

class TotalCols(SheetService):
    ...

class SearchCell(SheetService):
    val:str
    regex:Optional[str]=None


