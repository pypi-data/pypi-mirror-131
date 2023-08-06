from mongoengine import signals
from blinker import Signal
from typing import Tuple
from audit_flask.utils import *

singal_send_args =  Signal('Send args')

class Audit():
    @classmethod
    def post_save(cls, sender, document, **kwargs):
        __audit(document, **kwargs)
    
    @classmethod
    def post_delete(cls, sender, document, **kwargs):
        __audit(document, **kwargs)

def register_signals_model(cls):
    signals.post_save.connect(cls.post_save, sender = cls)
    signals.post_delete.connect(cls.post_delete, sender = cls)

def __audit(document, **kwargs):
    changes = None
    updates, removals = document._delta()
    if 'created' in kwargs:
        method = 'create'
        if kwargs['created'] is False:
            if(type(updates) == Tuple):
                changes = dict((key, value) for key, value in updates)
            else:
                changes = updates
            method = 'update'
    else:
        method = 'delete'
    args = {
        'object_pk': document.pk,
        'content_type': document._collection.name,
        'object_repr': serializar_dict({**document.to_mongo()}),
        'action': method,
        'changes': serializar_dict(changes),
        'remote_addr':remote_addr_validate(),
        'user': user_validate()
    }
    singal_send_args.send(None, **args)