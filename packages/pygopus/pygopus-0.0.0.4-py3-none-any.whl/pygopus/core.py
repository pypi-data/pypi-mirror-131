from dataclasses import dataclass
from typing import Any,List
from random import randint

from .service import *
from path import Path
import pkg_resources
import subprocess
import platform
import httpx
import os


HOST = "http://127.0.0.1"
FOLDER = platform.system()
if not FOLDER:
    raise Exception("Unknown OS")

BIN = pkg_resources.resource_filename("pygopus",Path(f"/bin/{FOLDER}/pygobin"))

service_pool = {}

if platform.system() == "Windows":
    BIN = pkg_resources.resource_filename("pygopus",Path(f"/bin/{FOLDER}/pygobin.exe"))

if platform.system() == "Linux":
    ...


def check_path(path:str):
    p = Path(path)
    if not p.exists():
        raise Exception(f"{ path } is not exists.Please check carefully") 



def create_workbook(path:str):
    import shutil
    tpl = pkg_resources.resource_filename("pygopus",Path("/bin/tpl.xlsx"))
    shutil.copyfile(tpl,Path(path))


@dataclass
class XlInfo:
    pid:int
    port:int
    file_name:str


class WorkBook:

    @classmethod
    def open(cls,paths:List[str]):
        return [cls(p) for p in paths]

    def __init__(self,path:str,write_mode="",debug=False) -> None:
        # check file here
        if write_mode != "w+":
            # means user want open, so you gotta if file exists. 
            check_path(path)
        # else:
        #     create_workbook(path)
        #     print(f"{path} file created.")


        port = randint(45555,55588)
        pygo_bin = Path(BIN)
        mode = os.stat(pygo_bin).st_mode | 0o100

        if os.environ.get("code_platform") != "linux":
            pygo_bin.chmod(mode)

        cmd = f"{BIN} -path {path} -port {port}".split()

        # p = subprocess.Popen(args=cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        kwd = {}
        if debug:
            ...
        else:
            kwd = dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE)


        p = subprocess.Popen(args=cmd,**kwd)
        self._pid = p.pid
        self.file_name = str(Path(path).abspath())

        info = XlInfo(pid=p.pid,port=port,file_name=self.file_name)
        service_pool.update({self.file_name:info})

        while True:
            try:
                res = Hello(file_name=self.file_name).get()
                break
            except httpx.ConnectError as e: 
                if debug:
                    print("Waiting for starting server.")

    def __repr__(self):
        return f"<pygopus.WorkBook at='{self.file_name}'>"

    def __len__(self):
        # return len(self.sheets)
        ...

    def __getitem__(self,k):
        sheets = {sh.name:sh for sh in self.sheets}
        return sheets[k]

    def __setitem__(self,k:str,v:'Sheet'):
        ...
        

    def get_sheet(self,name:str):
        return self[name]

    def add(self,name:str):
        res = AddSheet(
            file_name=self.file_name,
            sheet_name=name

        ).get()
        return "ok"


    def delete(self,name:str):
        DeleteSheet(
            file_name=self.file_name,
            sheet_name=name

        ).get()
        return "ok"

    @property
    def sheets(self):
        res = GetSheets(file_name=self.file_name).get()
        return [Sheet(index,name,self.file_name) for index,name in res.items()]

    def save(self):
        Save(file_name=self.file_name).get()

    def save_as(self,path:str):
        SaveAs(file_name=self.file_name,path=path).get()

    def close(self):
        import psutil
        Close(file_name=self.file_name).get()
        ps = psutil.Process(self._pid)
        ps.terminate()



class Sheet:

    def __init__(self,index:int,name:str,belong:str) -> None:
        self._index = index
        self._belong=belong
        self.name = name
    
    def __setitem__(self,k,v):
        return self.set(k,v)

    def __getitem__(self,k):
        ...
    def __repr__(self):
        return f"<pygopus.Sheet name='{self.name}'>"

    @property
    def rows(self):
        res = GetRows(sheet_name=self.name,file_name=self._belong).get()
        return res

    @property
    def cols(self):
        res = GetCols(
            sheet_name=self.name,
            file_name=self._belong
        ).get()

        return res

    def get(self,axis:str):

        res = GetCell(
            file_name=self._belong,
            sheet_name=self.name,
            axis=axis
        ).get()
        return res


    def set(self,axis:str,val:Any):

        res = SetCell(
            sheet_name=self.name,
            file_name=self._belong,
            axis=axis,val=val).get()
        return res

    def batch_set(self,*args,data:List):

        for index,axis in enumerate(args):
            res = SetCell(
                sheet_name=self.name,
                file_name=self._belong,
                axis=axis,
                val=data[index]).get()
        return "ok"

    def write_rows(self,data:List,start_at="A"):
        rows = {f"{start_at}{index+1}":d for index,d in enumerate(data)}
        res = WriteRows(
            file_name=self._belong,
            sheet_name=self.name,
            rows=rows).post()
        return res

    def delete_row(self,row_axis:int):
        res = DeleteRow(
            sheet_name=self.name,
            file_name=self._belong,
            row_axis=row_axis
        ).get()
    def append_col(self,col:List,force=False):
        if force:
            added_rows = [row+[str(col[index])] for index,row in enumerate(self.rows)]
            res = self.write_rows(added_rows)
            return

        res = TotalCols(
            sheet_name=self.name,
            file_name=self._belong

        ).get()

        assert isinstance(res,dict)
        next_key = res["nextkey"]

        for index,val in enumerate(col):
            axis = f"{next_key}{index+1}"
            self.set(axis=axis,val=val)


        return 

    def test_col(self):
        res = TotalCols(
            sheet_name=self.name,
            file_name=self._belong

        ).get()
        return res

    # contains gt lt eq
    def find(self,val:str="",regex:str=""):
        ...


    def option(self):
        ...


class Operator:
    ...

class RowHelper:
    ...
