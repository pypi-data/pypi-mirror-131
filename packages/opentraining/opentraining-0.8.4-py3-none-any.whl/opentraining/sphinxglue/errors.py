from ..core.errors import OpenTrainingError, CompoundError

class SoupAlreadyFailed(OpenTrainingError):
    '''A sentinel error for all those places which try to build a
    soup. When that process has failed once, it will fail again, and
    it does not make any sense to retry the whole process.

    '''
    def __init__(self):
        super().__init__('', None)

def remove_nodes(doctree, type):
    for n in doctree.traverse(type):
        n.replace_self([])

def log_and_swallow_error(error, logger):
    if isinstance(error, SoupAlreadyFailed):
        return
    elif isinstance(error, CompoundError):
        for e in error:
            logger.warning(str(e), location=e.userdata)
    elif isinstance(error, OpenTrainingError):
        logger.warning(str(error), location=error.userdata)
    else:
        assert False, 'called with something not from here:' + str(error)
