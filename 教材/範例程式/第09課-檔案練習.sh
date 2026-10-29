#!/bin/sh
set -eu

# 在系統暫存目錄建立獨立資料夾，不使用既有的練習資料。
practice_dir=$(mktemp -d "${TMPDIR:-/tmp}/ba5077-lesson09.XXXXXX")
cd "$practice_dir"
printf 'Hello, AIoT!\n' > welcome.txt
mkdir samples
cp welcome.txt samples/copy.txt

printf '原始內容: '
cat welcome.txt
printf '檔案大小（bytes）: '
wc -c < welcome.txt
if cmp -s welcome.txt samples/copy.txt; then
    printf '複製結果: 內容一致\n'
else
    printf '複製結果: 內容不同\n'
    exit 1
fi
printf '練習檔案:\n'
find . -type f -print | LC_ALL=C sort
printf '練習目錄: %s\n' "$practice_dir"
