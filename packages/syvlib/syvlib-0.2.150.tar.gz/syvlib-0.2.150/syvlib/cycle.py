import base64
import requests
import time
from math import ceil
from io import IOBase, BytesIO

from .codec import decode, encode
from .drop import Drop


class Cycle:

    chunk_size = 16777216

    def __init__(self, session, open_data):
        self.session = session
        self.error = None
        self.client_config = None
        self.progress = None
        self.is_committed = None
        self.records = None
        self.uid = None
        self.drop_uids = None
        self.ask_arrays = None
        self.client_config_template = None
        self.public_config = None
        self.load(open_data.get('cycle'))

    def load(self, cycle_data):
        self.error = cycle_data.get('error')
        self.client_config = cycle_data.get('client_config')
        self.progress = cycle_data.get('progress')
        self.is_committed = cycle_data.get('is_committed')
        self.records = cycle_data.get('records')
        self.uid = cycle_data.get('uid')
        self.drop_uids = cycle_data.get('drop_uids')
        self.ask_arrays = cycle_data.get('ask_arrays')
        self.client_config_template = cycle_data.get('client_config_template')
        self.public_config = cycle_data.get('public_config')

    def pull_drops(self, pipe, drop_uids):
        if pipe not in self.drop_uids:
            raise Exception('Invalid pipe name.')
        if not set(drop_uids).issubset(set(self.drop_uids.get(pipe))):
            raise Exception('Invalid drop uids.')

        cycle_url = self.session.get_url(
            'cycle/%s/drop?face_mode=raw&drop_uids=%s' % (
                self.uid,
                ','.join([str(x) for x in drop_uids])
            )
        )
        cycle_res = requests.get(
            cycle_url,
            headers=self.session.get_headers()
        )
        cycle_res.raise_for_status()
        cycle_data = cycle_res.json()
        drop_list = [Drop(
            self,
            {
                y: decode(
                    base64.b64decode(
                        x.get('arrays').get(y).get('data').get('data')
                    ),
                    self.session.byteorder
                )
                for y in x.get('arrays')
            },
            uid=x.get('uid')
        ) for x in cycle_data.get('drops')]
        return drop_list

    def push_drops(self, pipe, drop_list):
        if pipe not in self.ask_arrays:
            raise Exception('Invalid pipe name.')
        assert type(drop_list) is list
        cycle_data = {'drops':{pipe:[]}}

        for drop in drop_list:
            assert type(drop) is Drop
            drop_data = {
                'arrays': {
                    x: {
                        'data': {
                             'data': base64.b64encode(encode(drop.arrays.get(x))).decode()
                        }
                    } for x in drop.arrays
                }
            }
            if type(drop.uid) is int:
                drop_data['mapped_uid'] = drop.uid
            cycle_data['drops'][pipe].append(drop_data)

        cycle_url = self.session.get_url('cycle/%s?face_mode=raw' % self.uid)
        cycle_res = requests.put(
            cycle_url,
            json=cycle_data,
            headers=self.session.get_headers()
        )
        cycle_res.raise_for_status()

    def pull_record(self, name, stream):
        record = next(iter([
            x for x in self.records
            if x.get('name') == name
            and x.get('is_input') is False
        ]), None)
        if record is None:
            raise Exception('Invalid record name.')
        assert isinstance(stream, IOBase)

        file_size = record.get('byte_count')
        chunk_count = ceil(file_size / Cycle.chunk_size)

        for chunk_idx in range(chunk_count):
            offset = Cycle.chunk_size * chunk_idx
            length = min(Cycle.chunk_size, file_size - offset)

            record_url = self.session.get_url('record/%s?offset=%s&length=%s' % (
                record.get('uid'),
                offset,
                length
            ))
            record_res = requests.get(
                record_url,
                headers=self.session.get_headers()
            )
            record_res.raise_for_status()

            stream.write(record_res.content)


    def push_record(self, name, stream):
        assert isinstance(stream, IOBase)

        stream.seek(0, 2)
        file_size = stream.tell()
        chunk_count = ceil(file_size / Cycle.chunk_size)
        stream.seek(0)

        cycle_url = self.session.get_url('cycle/%s' % self.uid)

        for chunk_idx in range(chunk_count):
            offset = Cycle.chunk_size * chunk_idx
            length = min(Cycle.chunk_size, file_size - offset)

            buf = BytesIO()
            buf.write(stream.read(length))
            buf.seek(0)

            headers=self.session.get_headers()
            headers['Content-Range'] = 'bytes %s-%s/%s' % (
                offset,
                (offset+length)-1,
                file_size
            )

            cycle_res = requests.put(
                cycle_url,
                data = {'offset': offset, 'length': length},
                files = {name: buf},
                headers = headers
            )
            cycle_res.raise_for_status()


    def commit(self):
        cycle_url = self.session.get_url('cycle/%s/commit' % self.uid)
        cycle_res = requests.put(
            cycle_url,
            headers=self.session.get_headers()
        )
        cycle_res.raise_for_status()
        cycle_data = cycle_res.json()
        self.load(cycle_data.get('cycle'))

    def commit_and_wait(self, interval=1):
        self.commit()
        while self.progress < 100 and self.error is None:
            time.sleep(interval)
            self.refresh()

    def cancel(self):
        cycle_url = self.session.get_url('cycle/%s/cancel' % self.uid)
        cycle_res = requests.put(
            cycle_url,
            headers=self.session.get_headers()
        )
        cycle_res.raise_for_status()
        cycle_data = cycle_res.json()
        self.load(cycle_data.get('cycle'))

    def refresh(self):
        cycle_url = self.session.get_url('cycle/%s' % self.uid)
        cycle_res = requests.get(
            cycle_url,
            headers=self.session.get_headers()
        )
        cycle_res.raise_for_status()
        cycle_data = cycle_res.json()
        self.load(cycle_data.get('cycle'))
