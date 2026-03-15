"""
Jalankan script ini di folder yang sama dengan app.py untuk fix error config:
  python fix_config.py
"""
import re, shutil, os

path = 'app.py'
if not os.path.exists(path):
    print("ERROR: app.py tidak ditemukan di folder ini!")
    exit(1)

shutil.copy(path, path + '.backup')
print(f"Backup dibuat: {path}.backup")

content = open(path, encoding='utf-8').read()
original_size = len(content)

# ── Fix semua config.* references ─────────────────────────────
replacements = {
    'config.TELEGRAM_BOT_TOKEN':  '""',
    'config.TELEGRAM_CHAT_ID':    '""',
    'config.WHATSAPP_PHONE':      '""',
    'config.WHATSAPP_API_KEY':    '""',
    'config.DEFAULT_TICKERS[:10]':'["BBCA","BBRI","BMRI","TLKM","ASII","UNVR","KLBF","ADRO","ANTM","MDKA"]',
    'config.AUTO_REFRESH_INTERVAL':'300',
}
for old, new in replacements.items():
    count = content.count(old)
    if count:
        content = content.replace(old, new)
        print(f"  Fixed {count}x: {old}")

# ── Remove import config ───────────────────────────────────────
before = content.count('\nimport config')
content = re.sub(r'\nimport config\b.*', '', content)
if before: print(f"  Removed: import config")

# ── Remove from notifier import ───────────────────────────────
before = content.count('from notifier')
content = re.sub(r'^from notifier\b.*\n', '', content, flags=re.MULTILINE)
# Handle multi-line notifier import
content = re.sub(r'^from notifier.*?(?=\n\S)', '', content, flags=re.MULTILINE|re.DOTALL)
if before: print(f"  Removed: from notifier import")

# ── Write fixed file ──────────────────────────────────────────
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nDone! {original_size} → {len(content)} chars")
print("Restart Streamlit untuk apply perubahan.")

# Verify
import subprocess
r = subprocess.run(['python3', '-m', 'py_compile', path], capture_output=True, text=True)
print(f"Syntax check: {'✅ OK' if r.returncode==0 else '❌ ' + r.stderr[:200]}")
