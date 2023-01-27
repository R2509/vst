import sys

class _Param:
    def __init__(self, name, length, start, byte_int):
        self.name = name
        self.length = length
        self.start = start
        if type(length) is int: self.end = self.start + self.length
        self.bint = byte_int
    
    def __call__(self, idx: int, tempi: int, tempb: bytes):
        byte_int = self.bint
        prm = []
        end = False
        if type(self.length) is str and self.length == 'vlq':
            if byte_int < 0x80: end = True
        elif idx == self.end: end = True
        if end:
            tempi = int.from_bytes(tempb, 'big')
            prm = [self.name, tempi]
            tempi = 0
            tempb = b''

        return prm, tempi, tempb, end

class Midi:
    def __init__(self, filepath):
        self.ppqn = None
        self.cprm: _Param = None

        filepath = f'{sys.path[0]}/{filepath}'
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

        tracknum: int = -1
        newtrack: bool = False
        inc_track_num: bool = False
        track_idx: int = 0
        tracks: list = []
        i: int = 0
        find: bool = False

        event_i: int = 0

        start: bool = False

        delta: bool = False
        status: bool = False
        length = False
        data: bool = False
        start: bool = True

        end: bool = False

        for idx, byte_int in enumerate(list(self.file)):
            if idx == 30:break
            byte = int.to_bytes(byte_int, 1, 'big')
            if self.cprm is not None:
                p, tempi, tempb, end = self.cprm(idx, tempi, tempb)
                if p:
                    if head: o = head_params
                    if track: o = tracks[tracknum]
                    o[p[0]] = p[1]

                    self.cprm = None
            
            if idx == 0:
                head = True
                chunk = True
            if head:
                tempb += byte
                if chunk:
                    if tempb == b'MThd':
                        chunk = False
                        tempb = b''
                    if chunk and idx == 3: raise TypeError('header chunk not found')
                
                if idx == 4:
                        self.cprm = _Param('head_length', 4, idx, byte_int)
                if idx == 8:
                    self.cprm = _Param('head_format', 2, idx, byte_int)
                if idx == 10:
                    self.cprm = _Param('head_ntracks', 2, idx, byte_int)
                if idx == 12:
                    self.cprm = _Param('head_ppqn', 2, idx, byte_int)
                if 'head_ntracks' in head_params:
                    for i in range(head_params['head_ntracks']): tracks.append({})
                if 'head_length' in head_params and idx == (head_params['head_length'] + 8):
                    head = False
                    track = True
                    newtrack = True
                    inc_track_num = True
                    tempb = b''
                    tempi = 0
            
            if track:
                tempb += byte
                if newtrack:
                    if inc_track_num:
                        tracknum += 1
                        track_idx = 0
                    inc_track_num = False

                    if track_idx == 0:
                        chunk = True
                    if chunk:
                        if tempb == b'MTrk':
                            chunk = False
                            tempb = b''
                            i = track_idx + 1
                            find = True
                        if chunk and track_idx == 3: raise TypeError('track chunk not found')
                    if track_idx == i and find:
                        self.cprm = _Param('track_length', 4, idx, byte_int)
                        find = False

                        delta = True
                        status = False
                        length = False
                        data = False
                        start = True
                    if not find:
                        if delta and start:
                                self.cprm = _Param(f'event_{event_i}_delta', 'vlq', idx, byte_int)
                        event_i += 1
                    
                track_idx += 1


                
        
        print(head_params, tracks)
            

m = Midi('../Flourish.mid')
m.parse()