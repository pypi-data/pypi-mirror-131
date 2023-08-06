import dis


class ClientMetaVerify(type):
    """
    Metaclass for Client Verifying.
    """
    def __init__(self, clsname, bases, clsdict):
        mtdlist = []
        for func in clsdict:
            try:
                func_out = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in func_out:
                    if i.opname == 'LOAD_GLOBAL' and i.argval not in mtdlist:
                        mtdlist.append(i.argval)
        for command in ('accept', 'listen', 'socket'):
            if command in mtdlist:
                raise TypeError('Privat method is not allowed.')
        if 'get_message' not in mtdlist or 'send_message' not in mtdlist:
            raise TypeError('Need socket functions.')
        super().__init__(clsname, bases, clsdict)
