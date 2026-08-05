#!/usr/bin/env python3
"""index.html에 실제로 쓰이는 글자만 남겨 fonts/geumeunbohwa.woff2 를 생성한다.

본문에 새 글자를 추가했다면 다시 실행할 것:
    python3 tools/subset-font.py
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "fonts" / "geumeunbohwa.ttf"
OUT = ROOT / "fonts" / "geumeunbohwa.woff2"

# index.html 안의 모든 문자 + 여유분(ASCII 전체, 호환용 자모, 폰트가 가진 기호들)
EXTRA = (
    [chr(c) for c in range(0x20, 0x7F)]
    + [chr(c) for c in range(0x3131, 0x3164)]
    + list("‘’“”※←→★☆♡♥♩♪♬")
)


def main():
    text = (ROOT / "index.html").read_text(encoding="utf-8")
    chars = sorted(set(text) | set(EXTRA))
    unicodes = ",".join(f"U+{ord(c):04X}" for c in chars)

    subprocess.run(
        [
            sys.executable, "-m", "fontTools.subset", str(SRC),
            f"--unicodes={unicodes}",
            "--layout-features=*",
            "--flavor=woff2",
            f"--output-file={OUT}",
        ],
        check=True,
    )
    print(f"{len(chars)} chars -> {OUT.name} ({OUT.stat().st_size / 1024:.1f} KB, "
          f"원본 {SRC.stat().st_size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    main()
