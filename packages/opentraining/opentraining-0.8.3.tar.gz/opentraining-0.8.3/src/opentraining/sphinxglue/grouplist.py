from . import utils
from . import soup
from .errors import log_and_swallow_error, remove_nodes
from ..core.errors import OpenTrainingError
from ..core.topic import Topic
from ..core.group import Group
from ..core.errors import OpenTrainingError

from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import set_source_info
from sphinx.util import logging
from docutils import nodes

from networkx.algorithms.dag import topological_sort

_logger = logging.getLogger(__name__)


def setup(app):
    app.add_directive('ot-grouplist', _GroupListDirective)
    app.connect('doctree-resolved', _ev_doctree_resolved__expand_grouplist_nodes)

def _ev_doctree_resolved__expand_grouplist_nodes(app, doctree, docname):
    try:
        expander = _GroupListExpander(app=app, docname=docname)
        for n in doctree.traverse(_GroupListNode):
            n.replace_self(expander.expand(n))
    except OpenTrainingError as e:
        remove_nodes(doctree, _GroupListNode)
        log_and_swallow_error(e, _logger)

class _GroupListNode(nodes.Element):
    def __init__(self, path):
        super().__init__(self)
        self.path = path

class _GroupListDirective(SphinxDirective):
    required_arguments = 1   # path

    def run(self):
        path = utils.element_path(self.arguments[0].strip())

        l = _GroupListNode(path=path)
        l.document = self.state.document
        set_source_info(self, l)

        return [l]

class _GroupListExpander:
    def __init__(self, app, docname):
        self._app = app
        self._docname = docname

    def expand(self, node):
        group = self._app.soup().element_by_path(node.path, userdata=node)
        topics = group.iter_recursive(cls=Topic)
        graph = self._app.soup().worldgraph().subgraph(topics)
        topo = topological_sort(graph)

        bl = nodes.bullet_list()
        for topic in reversed(list(topo)):
            if not isinstance(topic, Topic):
                continue
            li = nodes.list_item()
            li += self._topic_paragraph(topic.path, userdata=node)
            bl += li
        return bl

    def _topic_paragraph(self, path, userdata):
        topic = self._app.soup().element_by_path(path, userdata=userdata)
        assert isinstance(topic, Topic), f'dependency on non-topic {path}?'
        p = nodes.paragraph()
        p += self._topic_headline_elems(path, userdata=userdata)
        return p

    def _topic_headline_elems(self, path, userdata):
        topic = self._app.soup().element_by_path(path, userdata=userdata)
        elems = []
        elems.append(nodes.Text(f'{topic.title} ('))

        ref = nodes.reference()
        ref['refuri'] = self._app.builder.get_relative_uri(
            from_=self._docname, to=topic.docname)
        ref += nodes.Text('.'.join(topic.path))
        elems.append(ref)
        elems.append(nodes.Text(')'))
        
        return elems
