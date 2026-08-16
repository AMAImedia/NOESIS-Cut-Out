import hashlib,json,sys
from pathlib import Path
SCRIPT_DIR=Path(__file__).resolve().parent
R=SCRIPT_DIR.parent
M=SCRIPT_DIR/'preflight_manifest.json'
def main():
 if not M.is_file(): print('[PREFLIGHT] manifest missing'); return 2
 try:d=json.loads(M.read_text(encoding='utf-8-sig'))
 except Exception as e: print('[PREFLIGHT] manifest unreadable:',e); return 2
 bad=[]
 for x in d.get('required',[]):
  p=R/x
  if not p.is_file() or p.stat().st_size==0:bad.append('MISSING_OR_EMPTY: '+x)
 for x,w in d.get('sha256',{}).items():
  p=R/x
  if not p.is_file():bad.append('MISSING_HASH_FILE: '+x);continue
  h=hashlib.sha256(p.read_bytes()).hexdigest()
  if h.lower()!=w.lower():bad.append('HASH_MISMATCH: '+x)
 if bad:
  print('[PREFLIGHT] FAILED')
  print('\n'.join(' - '+x for x in bad))
  return 1
 print('[PREFLIGHT] OK')
 return 0
if __name__=='__main__':sys.exit(main())
