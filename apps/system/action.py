import time
import re
import subprocess
import threading
from sys import platform
from locale import getdefaultlocale
from apps.equipo.models import Equipo, Test


class service(threading.Thread):
    def __init__(self, group=None, target=None, name=None, equipo=None,
		args=None, kwargs=None, *, daemon=True):
        self.equipo=equipo
        
        self._stop_event = threading.Event()

        super().__init__(group=group, target=target, name=name, daemon=daemon)
    def stop(self):
        self._stop_event.set()
    def stopped(self):
        return self._stop_event.is_set()
    
    def run(self):
 
        # registros = Equipo.objects.get(pk_publica=self.pk)
        data = self.ping(self.equipo.direccion, self.equipo.paquetes)
        if data[0]:
            data[1]['responde']=True
        
        

        data[1]["equipo"]=self.equipo
        test = Test(**data[1])
        test.save()
        self.equipo.servicio = 'Inactivo'
        self.equipo.save()

    def tokenizea(self, string):
        data = {}
        if platform == "linux":
            token_specification = [
                    ('data',   r'{0}'.format('rtt min/avg/max/mdev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)')),
                    ('enviados',   r'{0}'.format('enviados = \d+(\.\d*)?')), 
            ]
            
        else:
    
            token_specification = [
                    ('media',   r'{0}'.format('Media' + ' = \d+(\.\d*)?')), 
                    ('minimo',   r'{0}'.format('nimo = \d+(\.\d*)?')), 
                    ('maximo',   r'{0}'.format('ximo = \d+(\.\d*)?')), 
                    ('enviados',   r'{0}'.format('enviados = \d+(\.\d*)?')), 
                    ('recibidos',   r'{0}'.format('recibidos = \d+(\.\d*)?')), 
                    ('perdidos',   r'{0}'.format('\d+(\.\d*)?% perdidos')), 
            ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        line_num = 1
        line_start = 0
        for mo in re.finditer(tok_regex, string):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            if kind == 'data':
                data_raw = value.split("=")[1]
                data_ar = data_raw.split("/")
                data['minimo']=data_ar[0]
                data['media']=data_ar[1]
                data['maxima']=data_ar[2]
                

            if kind == 'perdidos':
                value = int(value.split("%")[0])
            else:
                value = int(value.split("=")[1])
            data[kind] = value
        return data
    
    def ping(self, ip, paquetes=3):
                
        if platform == "linux" :
            command=["ping", "-c", "3", str(paquetes), "0.2", ip]
            timeout=2
        else:
            command=["ping", "-n", str(paquetes) , ip]
            timeout=2
        proc=subprocess.Popen(command, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        try:
            out=proc.communicate(timeout=timeout)
            if proc.returncode == 0:
                if platform == "linux":
                    avgRTT=re.search("rtt min/avg/max/mdev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)", str(out)).group(2)
                else:
                    
                    valor= self.tokenizea(out[0].decode(getdefaultlocale()[1]))
                    return (True, valor)
            else:
                return (False,{    'enviados': 0, 
                            'recibidos': 0, 
                            'perdidos': 0, 
                            'minimo': 0, 
                            'maximo': 0, 
                            'media': 0})
        except subprocess.TimeoutExpired:
            proc.kill()
            return (False,{    'enviados': 0, 
                            'recibidos': 0, 
                            'perdidos': 0, 
                            'minimo': 0, 
                            'maximo': 0, 
                            'media': 0})
           


# b = service(ip="www.google.com") 
# b.start()


# print("ssd")
# print(getdefaultlocale())
# b.join()


