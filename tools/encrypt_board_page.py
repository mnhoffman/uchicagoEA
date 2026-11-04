#!/usr/bin/env python3
"""Encrypt board-src/board.html into the published board/index.html.

Usage:
    python3 tools/encrypt_board_page.py            # prompts for the password
    python3 tools/encrypt_board_page.py --password-file path/to/file

The plaintext source (board-src/) is gitignored; only the encrypted page is
published. AES-256-GCM, key derived with PBKDF2-SHA256 (600k iterations).
"""
import argparse
import base64
import getpass
import os
import pathlib

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ROOT = pathlib.Path(__file__).resolve().parent.parent
ITERATIONS = 600_000

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Board | UChicago Effective Altruism</title>
<link rel="icon" href="../assets/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,400;1,9..144,500&family=Nunito+Sans:ital,opsz,wght@0,6..12,400;0,6..12,500;0,6..12,600;0,6..12,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/styles.css?v=9">
</head>
<body class="ed">
<header class="ed-bar">
  <div class="ed-bar__inner">
    <a class="ed-bar__logo" href="../" aria-label="UChicago Effective Altruism home"><img src="../assets/images/logo.png" alt="University of Chicago Effective Altruism"></a>
  </div>
</header>
<main id="board-main">
<section class="sec theme-cream sec--medium"><div class="container container--medium"><div class="rich" style="max-width:420px">
<p class="ed-eyebrow">Board only</p>
<h2>This page is <em>locked.</em></h2>
<p>Enter the board password to continue.</p>
<form id="gate" autocomplete="off">
<input id="pw" type="password" autocomplete="current-password" placeholder="Password" style="font-family:var(--sans);font-size:1rem;padding:0.85em 1em;border:1.5px solid hsla(200,30%,14%,0.25);border-radius:10px;width:100%;background:var(--white);color:var(--ink)">
<p id="err" hidden style="color:hsl(5,65%,45%);font-size:0.92rem;margin-top:0.6rem">That password didn't work. Try again.</p>
<button class="btn" type="submit" style="margin-top:1rem;border:0;cursor:pointer">Unlock</button>
</form>
</div></div></section>
</main>
<script>
const SALT = "__SALT__", IV = "__IV__", CT = "__CT__";
const b64 = s => Uint8Array.from(atob(s), c => c.charCodeAt(0));
async function tryUnlock(pw) {
  const km = await crypto.subtle.importKey("raw", new TextEncoder().encode(pw), "PBKDF2", false, ["deriveKey"]);
  const key = await crypto.subtle.deriveKey(
    { name: "PBKDF2", salt: b64(SALT), iterations: __ITER__, hash: "SHA-256" },
    km, { name: "AES-GCM", length: 256 }, false, ["decrypt"]);
  const pt = await crypto.subtle.decrypt({ name: "AES-GCM", iv: b64(IV) }, key, b64(CT));
  const main = document.getElementById("board-main");
  main.innerHTML = new TextDecoder().decode(pt);
  main.querySelectorAll("script").forEach(s => {
    const n = document.createElement("script");
    n.textContent = s.textContent;
    s.replaceWith(n);
  });
  try { sessionStorage.setItem("uceaBoardPw", pw); } catch (e) {}
}
document.getElementById("gate").addEventListener("submit", async (e) => {
  e.preventDefault();
  try { await tryUnlock(document.getElementById("pw").value); }
  catch (err) { document.getElementById("err").hidden = false; }
});
try {
  const saved = sessionStorage.getItem("uceaBoardPw");
  if (saved) tryUnlock(saved).catch(() => {});
} catch (e) {}
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--password-file", help="file whose first line is the password")
    args = ap.parse_args()

    if args.password_file:
        password = pathlib.Path(args.password_file).read_text().strip().splitlines()[0]
    else:
        password = getpass.getpass("Board password: ")
    if len(password) < 8:
        raise SystemExit("Password must be at least 8 characters.")

    for src, outdir in [("board.html", "board"), ("edit.html", "edit")]:
        src_path = ROOT / "board-src" / src
        if not src_path.exists():
            continue
        plaintext = src_path.read_bytes()
        salt, iv = os.urandom(16), os.urandom(12)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITERATIONS)
        key = kdf.derive(password.encode())
        ct = AESGCM(key).encrypt(iv, plaintext, None)

        page = (TEMPLATE
                .replace("__SALT__", base64.b64encode(salt).decode())
                .replace("__IV__", base64.b64encode(iv).decode())
                .replace("__CT__", base64.b64encode(ct).decode())
                .replace("__ITER__", str(ITERATIONS)))
        out = ROOT / outdir / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(page)
        print(f"wrote {out} ({len(ct)} bytes of ciphertext)")


if __name__ == "__main__":
    main()
