import json,shutil,socket,sys
from pathlib import Path
SCRIPT_DIR=Path(__file__).resolve().parent
d=json.loads((SCRIPT_DIR/'preflight_manifest.json').read_text(encoding='utf-8-sig'))
b=[]
need=int(d.get('min_free_bytes',2*1024**3));free=shutil.disk_usage(SCRIPT_DIR.anchor or SCRIPT_DIR).free
if free<need:b.append('LOW_DISK_SPACE: '+str(free)+' free, '+str(need)+' required')
av=[]
for p in d.get('ports',[]):

 try:
  with socket.socket() as s:s.bind(('127.0.0.1',int(p)));av.append(p)
 except OSError:pass
if d.get('ports') and not av:b.append('NO_FREE_PORT: '+','.join(map(str,d['ports'])))
if b:
 print('[SPACE/PORT CHECK] FAILED');print('\n'.join(' - '+x for x in b));sys.exit(1)
print('[SPACE/PORT CHECK] OK; free ports: '+','.join(map(str,av)));sys.exit(0)
