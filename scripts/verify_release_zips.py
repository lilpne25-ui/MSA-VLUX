#!/usr/bin/env python3
"""Offline reproducible verification of release distributions (stdlib only)."""
from pathlib import Path,PurePosixPath
import hashlib, subprocess,sys, tempfile,zipfile,stat,json

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
RELEASES={'5.1.0':'MSA-VLUX-V5.1.0-CODEX-CLAUDE.zip',
          '5.2.0':'MSA-VLUX-V5.2.0-CODEX-CLAUDE.zip',
          '6.0.0':'MSA-VLUX-V6.0.0-CODEX-CLAUDE.zip'}

def sha256(data):return hashlib.sha256(data).hexdigest()

def verify_one(version,filename,manifest):
    archive=DIST/filename
    if manifest.get('dist/'+filename)!=sha256(archive.read_bytes()):raise ValueError('Checksum mismatch: '+filename)
    with tempfile.TemporaryDirectory() as t:
        root=Path(t)
        with zipfile.ZipFile(archive) as z:
            entries=z.infolist()
            if not entries or len(entries)>130:raise ValueError('Archive entries out of range')
            seen=set();total=0
            for entry in entries:
                name=entry.filename;p=PurePosixPath(name)
                if name in seen or p.is_absolute() or '..' in p.parts or not p.parts or p.parts[0]!='msa-vlux':
                    raise ValueError('Unsafe archive entry')
                seen.add(name);total+=entry.file_size
                if total>4_000_000 or entry.file_size>2_000_000:raise ValueError('Archive too large')
                mode=entry.external_attr>>16
                if stat.S_IFMT(mode)==stat.S_IFLNK:raise ValueError('Symlink not allowed')
            if z.testzip():raise ValueError('Corrupt ZIP')
            z.extractall(root)
        package=root/'msa-vlux'
        if (package/'VERSION').read_text().strip()!=version:raise ValueError('Wrong release version')
        def run(*args):
            p=subprocess.run([sys.executable,*args],cwd=package,text=True,capture_output=True)
            if p.returncode:raise ValueError('Test failed '+version+': '+p.stderr[-700:])
            return p
        run('scripts/msa.py','verify-package')
        check=run('-m','unittest','discover','-s','tests','-v')
        return {'version':version,'zip':filename,'integrity':'PASS','tests':check.stderr.strip().splitlines()[-1]}

def main():
    lines=(DIST/'SHA256SUMS.txt').read_text().splitlines();manifest={}
    for line in lines:
        sha,sep,name=line.partition('  ')
        if not sep or name in manifest or len(sha)!=64:raise ValueError('Manifest invalid')
        manifest[name]=sha
    for version,name in RELEASES.items():print(json.dumps(verify_one(version,name,manifest),sort_keys=True))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,zipfile.BadZipFile) as e:
        print('FAILED: '+str(e),file=sys.stderr);sys.exit(1)
