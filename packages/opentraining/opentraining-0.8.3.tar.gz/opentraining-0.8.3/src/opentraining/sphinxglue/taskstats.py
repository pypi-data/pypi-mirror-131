from . import utils
from . import soup
from .errors import log_and_swallow_error, remove_nodes
from ..core.task import Task
from ..core.errors import OpenTrainingError

from sphinx.util.nodes import set_source_info
from sphinx.util.docutils import SphinxDirective
from docutils import nodes

import itertools
import collections


from sphinx.util import logging
_logger = logging.getLogger(__name__)


def setup(app):
    app.add_directive('ot-taskstats', _TaskStatsDirective)
    app.connect('doctree-resolved', _ev_doctree_resolved__expand_taskstats_nodes)

def _ev_doctree_resolved__expand_taskstats_nodes(app, doctree, docname):
    try:
        for n in doctree.traverse(_TaskStatsNode):
            task = app.soup().element_by_path(n.path, userdata=n)

            if not isinstance(task, Task):
                _logger.warning(f'{task} is not a task', location=n)
                continue

            table = nodes.table()
            tgroup = nodes.tgroup(cols=4)
            table += tgroup
            tgroup += nodes.colspec(colwidth=1)
            tgroup += nodes.colspec(colwidth=1)
            tgroup += nodes.colspec(colwidth=1)
            tgroup += nodes.colspec(colwidth=1)

            if 'thead':
                thead = nodes.thead()
                tgroup += thead

                row1 = nodes.row()
                thead += row1
                row2 = nodes.row()
                thead += row2
                row1 += nodes.entry()
                row2 += nodes.entry()

                entry = nodes.entry()
                row1 += entry
                entry += nodes.Text(f'Implementation')
                entry = nodes.entry()
                row2 += entry
                entry += nodes.Text(f'(Points: {task.implementation_points})')

                entry = nodes.entry()
                row1 += entry
                entry += nodes.Text(f'Documentation')
                entry = nodes.entry()
                row2 += entry
                entry += nodes.Text(f'(Points: {task.documentation_points})')

                entry = nodes.entry()
                row1 += entry
                entry += nodes.Text(f'Integration')
                entry = nodes.entry()
                row2 += entry
                entry += nodes.Text(f'(Points: {task.integration_points})')

            if 'tbody':
                tbody = nodes.tbody()
                tgroup += tbody

                worker_shares = collections.defaultdict(lambda: [0,0,0])
                for person, share in task.implementors:
                    worker_shares[person][0] += share
                for person, share in task.documenters:
                    worker_shares[person][1] += share
                for person, share in task.integrators:
                    worker_shares[person][2] += share

                for person in sorted(worker_shares.keys(), key=lambda p: (p.lastname, p.firstname)):
                    row = nodes.row()
                    tbody += row

                    entry = nodes.entry()
                    row += entry
                    p = nodes.paragraph()
                    entry += p
                    if person.firstname and person.lastname:
                        text = f' {person.lastname} {person.firstname}'
                    else:
                        text = person.title
                    p += utils.make_reference(text=text, from_docname=docname, to_docname=person.docname, app=app)

                    # implementation
                    entry = nodes.entry()
                    row += entry
                    share = worker_shares[person][0]
                    if share != 0:
                        entry += nodes.Text(f'{share}%')

                    # documentation
                    entry = nodes.entry()
                    row += entry
                    share = worker_shares[person][1]
                    if share != 0:
                        entry += nodes.Text(f'{share}%')

                    # integration
                    entry = nodes.entry()
                    row += entry
                    share = worker_shares[person][2]
                    if share != 0:
                        entry += nodes.Text(f'{share}%')

            n.replace_self(table)
    except OpenTrainingError as e:
        remove_nodes(doctree, _TaskStatsNode)
        log_and_swallow_error(e, _logger)
 
class _TaskStatsNode(nodes.Element):
    def __init__(self, path):
        super().__init__(self)
        self.path = path

class _TaskStatsDirective(SphinxDirective):
    required_arguments = 1   # path

    def run(self):
        path = utils.element_path(self.arguments[0].strip())

        l = _TaskStatsNode(path=path)
        l.document = self.state.document
        set_source_info(self, l)

        return [l]

