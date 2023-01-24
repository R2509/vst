class _Param:
    def __init__(self, name, length, start):
        self.name = name
        self.length = length
        self.start = start
        self.end = self.start + self.length

class Midi:
    def __init__(self, filepath):
        self.ppqn = None
        self.cprm: _Param = None

        with open(filepath, 'rb') as f: self.file = f.read()

    def parse(self):
        chunk: bool = False
        head: bool = False
        track: bool = False
        event: bool = False

        headFound: bool = False

        tempb: bytes = b''
        tempi: int = 0

        param_length: int = 0

        head_params: dict = {}

        for idx, byte_int in enumerate(list(self.file)):
            byte = int.to_bytes(byte_int, 1, 'big')
            if self.cprm is not None:
                if idx == self.cprm.end:
                    tempi = int.from_bytes(tempb, 'big')
                    if head: head_params[self.cprm.name] = tempi
                    tempi = 0
                    tempb = b''
            
            if idx == 0:
                head = True
                chunk = True
            if head:
                tempb += byte
                if tempb == b'MThd':
                    chunk = False
                    tempb = b''
                if chunk and idx == 3: raise TypeError('header chunk not found')
                if idx == 4:
                    self.cprm = _Param('head_length', 4, idx)
        
        print(head_params)
            

m = Midi('Flourish.mid')
m.parse()