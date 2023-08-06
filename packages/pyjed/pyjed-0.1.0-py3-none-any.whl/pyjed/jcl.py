from collections import UserList
from dataclasses import dataclass, field, fields, make_dataclass


@dataclass
class Base:
    def to_string(self, statement):
        for parm in fields(self):
            if (parm.name != 'name' and
               getattr(self, parm.name) is not None and
               parm.name not in self._attrs):
                name, value = parm.name.upper().replace('_', ''), getattr(self, parm.name)
                if isinstance(value, str) and (
                   ' ' in value or [c for c in value if c.islower()]):
                    value = f"'{value}'"
                if len(statement[-1]) + len(f'{name}={value},') > 78:
                    statement.append('//      ')
                statement[-1] = statement[-1] + f'{name}={value},'
        print(statement)
        statement[-1] = statement[-1][:-1]
        return statement


@dataclass
class DISP:
    status: str = ''
    normal: str = ''
    abnormal: str = ''


@dataclass
class DD(Base):
    name: str
    stream: str = field(default=None, repr=False)
    accode: str = field(default=None, repr=False)
    amp: str = field(default=None, repr=False)
    avgrec: str = field(default=None, repr=False)
    blksize: str = field(default=None, repr=False)
    blkszlim: str = field(default=None, repr=False)
    burst: str = field(default=None, repr=False)
    ccsid: str = field(default=None, repr=False)
    chars: str = field(default=None, repr=False)
    chkpt: str = field(default=None, repr=False)
    cntl: str = field(default=None, repr=False)
    copies: str = field(default=None, repr=False)
    data: str = field(default=None, repr=False)
    dataclas: str = field(default=None, repr=False)
    dcb: str = field(default=None, repr=False)
    ddname: str = field(default=None, repr=False)
    dest: str = field(default=None, repr=False)
    disp: str = field(default=None)
    dlm: str = field(default=None, repr=False)
    dsid: str = field(default=None, repr=False)
    dsname: str = field(default=None)
    dsntype: str = field(default=None, repr=False)
    dummy: str = field(default=None, repr=False)
    dynam: str = field(default=None, repr=False)
    eattr: str = field(default=None, repr=False)
    expdt: str = field(default=None, repr=False)
    fcb: str = field(default=None, repr=False)
    filedata: str = field(default=None, repr=False)
    flash: str = field(default=None, repr=False)
    free: str = field(default=None, repr=False)
    freevol: str = field(default=None, repr=False)
    gdgorder: str = field(default=None, repr=False)
    hold: str = field(default=None, repr=False)
    keylabl1: str = field(default=None, repr=False)
    keylabl2: str = field(default=None, repr=False)
    keyencd1: str = field(default=None, repr=False)
    keyencd2: str = field(default=None, repr=False)
    keylen: str = field(default=None, repr=False)
    keyoff: str = field(default=None, repr=False)
    label: str = field(default=None, repr=False)
    lgstream: str = field(default=None, repr=False)
    like: str = field(default=None, repr=False)
    lrecl: str = field(default=None, repr=False)
    maxgens: str = field(default=None, repr=False)
    mgmtclas: str = field(default=None, repr=False)
    modify: str = field(default=None, repr=False)
    outlim: str = field(default=None, repr=False)
    output: str = field(default=None, repr=False)
    path: str = field(default=None)
    pathdisp: str = field(default=None, repr=False)
    pathmode: str = field(default=None, repr=False)
    pathopts: str = field(default=None, repr=False)
    protect: str = field(default=None, repr=False)
    recfm: str = field(default=None, repr=False)
    recorg: str = field(default=None, repr=False)
    refdd: str = field(default=None, repr=False)
    retpd: str = field(default=None, repr=False)
    rls: str = field(default=None, repr=False)
    secmodel: str = field(default=None, repr=False)
    segment: str = field(default=None, repr=False)
    space: str = field(default=None, repr=False)
    spin: str = field(default=None, repr=False)
    storclas: str = field(default=None, repr=False)
    subsys: str = field(default=None, repr=False)
    symbols: str = field(default=None, repr=False)
    symlist: str = field(default=None, repr=False)
    sysout: str = field(default=None)
    term: str = field(default=None, repr=False)
    ucs: str = field(default=None, repr=False)
    unit: str = field(default=None, repr=False)
    volume: str = field(default=None)

    _attrs = ('stream')
    _alias = {'VOLUME': 'VOL'}

    def to_string(self):
        if self.stream:
            stream = super().to_string([f'//{self.name} DD * '])
            stream.append(self.stream)
            return stream
        else:
            return super().to_string([f'//{self.name} DD '])


@dataclass
class COMMENT:
    text: str = ''


@dataclass
class STEP(Base):
    name: str
    dd: list = field(default_factory=list)
    _attrs = ('dd')

    def to_string(self):
        string = super().to_string([f'//{self.name} EXEC '])
        for dd in self.dd:
            string = string + dd.to_string()
        print(string)
        print('KIKO IKIKO IKIKO IKOKI')
        return string


class EXEC():

    @dataclass
    class EXEC(STEP):
        acct: str = field(default=None, repr=False)
        addrspc: str = field(default=None, repr=False)
        ccsid: str = field(default=None, repr=False)
        cond: str = field(default=None, repr=False)
        dynamnbr: str = field(default=None, repr=False)
        memlimit: str = field(default=None, repr=False)
        parm: str = field(default=None)
        parmdd: str = field(default=None, repr=False)
        perform: str = field(default=None, repr=False)
        pgm: str = field(default=None)
        proc: str = field(default=None)
        rd: str = field(default=None, repr=False)
        region: str = field(default=None, repr=False)
        rlstmout: str = field(default=None, repr=False)
        time: str = field(default=None, repr=False)
        steplib: DD = field(default=None)

    def __new__(self, *args, **kwargs):
        if len(args) == 2 or 'procname' in kwargs:
            name = args[1] if len(args) == 2 else kwargs.pop('procname')
            proc_parms = [(parm, str, field(default=None)) for parm in kwargs]
            proc_class = make_dataclass(name, proc_parms, bases=(STEP,))
            return proc_class(name, **kwargs)
        else:
            return EXEC.EXEC(*args, **kwargs)


@dataclass()
class JOB(UserList, Base):
    name: str
    _class: str = None
    msgclass: str = None
    notify: str = None
    user: str = None
    joblib: DD = None
    typrun: str = None
    time: str = None
    restart: str = None
    password: str = None
    prty: int = field(default=None, repr=False)
    perform: str = field(default=None, repr=False)
    schenv: str = field(default=None, repr=False)
    sysaff: str = field(default=None, repr=False)
    ujobcorr: str = field(default=None, repr=False)
    seclabel: str = field(default=None, repr=False)
    rd: str = field(default=None, repr=False)
    pages: str = field(default=None, repr=False)
    lines: str = field(default=None, repr=False)
    jobrc: str = field(default=None, repr=False)
    jeslog: str = field(default=None, repr=False)
    group: str = field(default=None, repr=False)
    dsenqshr: str = field(default=None, repr=False)
    cond: str = field(default=None, repr=False)
    ccsid: str = field(default=None, repr=False)
    cards: str = field(default=None, repr=False)
    bytes: str = field(default=None, repr=False)
    addrspc: str = field(default=None, repr=False)

    _attrs = ('steps')

    def __post_init__(self):
        super().__init__()

    def to_string(self):
        stream = super().to_string([f'//{self.name} JOB '])
        for statement in self.data:
            stream.extend(statement.to_string())
        print(stream)
        return '\n'.join(stream)
