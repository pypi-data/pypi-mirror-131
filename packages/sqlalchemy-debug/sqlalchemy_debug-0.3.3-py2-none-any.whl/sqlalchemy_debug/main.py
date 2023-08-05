from sqlalchemy.orm.query import Query
from sqlalchemy.sql.dml import Insert, Update, Delete
from sqlalchemy.sql.selectable import Select
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.sql.schema import Table
from sqlalchemy.schema import CreateTable

def _compile_statement(smt):
    _smt = smt.compile(compile_kwargs={"literal_binds": True})
    return _smt


def debug_statement(q, need_parameter=True):
    if isinstance(q, DeclarativeMeta):
        if hasattr(q, "__table__"):
            return str(CreateTable(q.__table__))
    elif isinstance(q, Table):
        return str(CreateTable(q))
    elif isinstance(q, Query):
        if need_parameter:
            smt = q.statement
            smt = _compile_statement(smt)
            return str(smt)
    elif isinstance(q, Insert):
        if need_parameter:
            param = q.parameters
            return str(q), param
    elif isinstance(q, (Select, Update, Delete)):
        smt = _compile_statement(q)
        return str(smt)
    else:
        return str(q)