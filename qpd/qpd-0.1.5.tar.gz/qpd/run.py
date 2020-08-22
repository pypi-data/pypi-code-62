from qpd._parser.sql import QPDSql
from qpd._parser.utils import VisitorContext
from qpd._parser.visitors import StatementVisitor
from qpd.qpd_engine import QPDEngine
from qpd.workflow import QPDWorkflow, QPDWorkflowContext
from typing import Any


def run_sql(engine: QPDEngine, sql: str, **dfs: Any) -> Any:
    qsql = QPDSql(sql, "singleStatement")
    ctx = QPDWorkflowContext(engine, dfs)
    wf = QPDWorkflow(ctx)
    v = StatementVisitor(VisitorContext(sql=qsql, workflow=wf, dfs=wf.dfs,))
    wf.assemble_output(v.visit(qsql.tree))
    wf.run()
    return ctx.result
