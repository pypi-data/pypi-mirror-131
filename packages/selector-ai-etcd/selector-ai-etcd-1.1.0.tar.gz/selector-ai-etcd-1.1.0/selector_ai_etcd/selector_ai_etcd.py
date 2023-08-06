'''
Etcd Interface
'''
import etcd3
import os
import subprocess
import time

class Etcd:
    '''
    Etcd interface functionality.
    '''
    def __init__(self, host='localhost', port=2379):
        self.host = host
        self.port = port
        
        self.etcdc = etcd3.client(host=self.host, port=self.port)
        while True:
            if self.isConnected() is True:
                return

    def isConnected(self):
        status = True
        try:
            _ = self.etcdc.status()
        except etcd3.Etcd3Exception:
            status = False
            print("etcd: not connected")
            time.sleep(5)
        return status

    def put(self, k, v):
        try: 
            _ = self.etcdc.put(k, str(v))
        except etcd3.exceptions.ConnectionFailedError:
            print("etcd: put failed with ConnectionFailedError")
        return

    def put_dict(self, prefix, d : dict):
        for k, v in d.items():
            key = prefix + '/' + k
            self.put(key, v)
        return

    def get(self, k):
        text = self.etcdc.get(k)
        return text[0]

    def get_prefix(self, prefix):
        text = self.etcdc.get_prefix(prefix)
        return text

    def get_dict(self, prefix):
        d = {}
        prefix = prefix + '/'
        data = self.get_prefix(prefix)
        for val, meta in data:
            k = meta.key[len(prefix):]
            d[k.decode()] = val.decode()
        return d

    def get_prefix_curr_prev(self, prefix):
        '''
        Return current and previous values for all keys matching a prefix.

        Get the current value of each key matching the prefix. 
        Using the meta data, get the revision when this key was modified.
        
        Get the previous value of each key based using a revision older 
        than when it was modified.

        Since etcd client api does not support older version, 
        subprocess command to launch etcdctl is used.
        '''
        results_curr = {}
        results_prev = {}

        prefix = prefix + '/'
        data = self.get_prefix(prefix)

        for val, meta in data:
            key = meta.key[len(prefix):]
            results_curr[key.decode()] = val.decode()
            prev_revision = meta.mod_revision - 1
            command = f'ETCDCTL_API=3 etcdctl get "{meta.key.decode()}" --rev={prev_revision} --print-value-only'
            data_prev = subprocess.run([command], shell=True, stdout=subprocess.PIPE)
            results_prev[key.decode()] = data_prev.stdout.decode().replace("\n", "")

        return results_curr, results_prev

    def find_value(self, prefix, val):
        data = self.get_prefix(prefix)
        print(type(val))
        for v, m in data:
            if v.decode() == val:
                return m.key
        return None