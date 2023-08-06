from sqlalchemy import inspect
from sqlalchemy import event
from blinker import Signal
from audit_flask.utils import *

singal_send_args =  Signal('Send args')

def keep_logs_models(cls):

    @event.listens_for(cls, 'after_insert')
    def after_insert(mapper, connection, target):
        __audit((cls, target),'create', None)

    @event.listens_for(cls, 'before_update')
    def before_update(mapper, connection, target):
        state = inspect(target)
        changes = {}
        for attr in state.attrs:
            hist = attr.load_history()
            if not hist.has_changes():
                continue
            changes[attr.key] = hist.added
        __audit((cls, target),'update', changes)

    @event.listens_for(cls, 'after_delete')
    def after_delete(mapper, connection, target):
        __audit((cls, target),'delete', None)

    def __audit(cls_target, method, changes: dict):
        if changes is not None:
            changes = {key: value[0] for key, value in changes.items()}

        cls, target = cls_target
        
        args ={
            'object_pk' : getattr(target, cls.__mapper__.primary_key[0].name),
            'content_type' : cls.__tablename__,
            'object_repr' : serializar_dict(target.__dict__),
            'action' : method,
            'changes' : serializar_dict(changes),
            'remote_addr' : remote_addr_validate(),
            'user' : user_validate()
        }
        args['object_repr'].pop('_sa_instance_state', None)
        singal_send_args.send(None, **args)
