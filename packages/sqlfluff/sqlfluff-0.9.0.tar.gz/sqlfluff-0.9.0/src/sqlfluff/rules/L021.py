"""Implementation of Rule L021."""
from typing import Optional

from sqlfluff.core.rules.base import BaseRule, LintResult, RuleContext


class Rule_L021(BaseRule):
    """Ambiguous use of DISTINCT in select statement with GROUP BY.

    | **Anti-pattern**
    | DISTINCT and GROUP BY are conflicting.

    .. code-block:: sql

        SELECT DISTINCT
            a
        FROM foo
        GROUP BY a

    | **Best practice**
    | Remove DISTINCT or GROUP BY. In our case, removing GROUP BY is better.

    .. code-block:: sql

        SELECT DISTINCT
            a
        FROM foo
    """

    def _eval(self, context: RuleContext) -> Optional[LintResult]:
        """Ambiguous use of DISTINCT in select statement with GROUP BY."""
        if context.segment.is_type("select_statement"):
            # Do we have a group by clause
            group_clause = context.segment.get_child("groupby_clause")
            if not group_clause:
                return None

            # Do we have the "DISTINCT" keyword in the select clause
            select_clause = context.segment.get_child("select_clause")
            select_modifier = select_clause.get_child("select_clause_modifier")
            if not select_modifier:
                return None
            select_keywords = select_modifier.get_children("keyword")
            for kw in select_keywords:
                if kw.name == "distinct":
                    return LintResult(anchor=kw)
        return None
