from functools import cached_property,wraps
from .complete_helper import autocomplete
from typing import Any, Dict, Optional, Union
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


class Service(BaseModel):
    file_name:str
    sheet_name:str=""

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





class Hello(Service):
    ...


class Save(Service):
    ...


class SaveAs(Service):
    path:str

class Close(Service):
    ...



class AddSheet(Service):
    ...


class DeleteSheet(Service):

    ...


class GetSheet(Service):
    ...
class GetSheets(Service):
    ...


class GetRows(Service):
    ...


class GetCols(Service):
    ...


class DeleteCol(Service):
    col_axis:str


class DeleteRow(Service):
    row_axis:int


class WriteRows(Service):
    rows:Dict


class GetCell(Service):
    axis:str


class SetCell(Service):
    axis:str
    val:Any


class TotalCols(Service):
    sheet_name:str


class SearchCell(Service):

    val:str
    regex:Optional[str]=None


