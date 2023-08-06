from pynvn.excel.list import lnumbercolumnbyrangstr
from pynvn.stringnvn.slist import returnseplistintbbystr
from pynvn.excel.del_row import delrowbyrange
from pynvn.excel.rows import startrow_endrow

class del_row(object):
    """ 
    handling range for sheet\n
    rmrange: Range to handling string: \n
    ex: A1, A1:B3,A
    ws: worksheet corresponds to the rmrange \n
    """
    def __init__(self,f):
        self.f = f
    def __call__(self,*args,**kwargs):
        self.__ws,rmrange = args
        for rangea in rmrange:
            self.__cols=lnumbercolumnbyrangstr(rstr=rangea)
            self.__rows=returnseplistintbbystr(strint=rangea)
            self.del_fun(**kwargs)

    def del_fun(self,**kwargs):
        a,b = startrow_endrow(ws=self.__ws,
                              rows=self.__rows,
                              cols=self.__cols
                              )
        for col in self.__cols:
            self.f(index_col_del=col,
                   ws=self.__ws,
                   startrow=a,
                   endrow=b,
                   **kwargs
                   )