from ..core.soup import Soup
from ..core.element import Element
from ..core.topic import Topic
from ..core.exercise import Exercise
from ..core.task import Task
from ..core.group import Group
from ..core.errors import OpenTrainingError, CompoundError
from .errors import SoupAlreadyFailed

from sphinx.util import logging
_logger = logging.getLogger(__name__)


def _prepare_app(app):
    if hasattr(app, '_ot_soup'):
        raise OpenTrainingError('Soup already created, cannot add one more element')
    if hasattr(app, '_ot_soup_failed'):
        raise OpenTrainingError('Soup created already failed once, not retrying')
    if not hasattr(app.env, 'ot_elements'):
        app.env.ot_elements = set()
    app.__class__.soup = create_soup

def sphinx_add_element(app, element):
    _prepare_app(app)
    assert isinstance(element, Element)
    app.env.ot_elements.add(element)    

def sphinx_purge_doc(app, env, docname):
    if hasattr(env, 'ot_elements'):
        env.ot_elements -= {e for e in env.ot_elements if e.docname == docname}

def create_soup(app):
    try:
        return app._ot_soup
    except AttributeError:
        pass

    if hasattr(app, '_ot_soup_failed'):  # do not repeatedly try
        raise SoupAlreadyFailed()

    try:
        app._ot_soup = Soup(app.env.ot_elements)
        return app._ot_soup
    except CompoundError as e:
        app._ot_soup_failed = True
        for err in e:
            _logger.warning(str(err), location=err.userdata)
        raise
    except OpenTrainingError as e:
        app._ot_soup_failed = True
        _logger.warning(str(e), location=e.userdata)
        raise

