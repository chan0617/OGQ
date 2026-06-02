"""
스티커 시트 분할 스크립트
입력: 4440 × 3314.82px PNG (24개 스티커 포함)
출력: 740 × 640px PNG 24개 (output/ 폴더)
"""

import os
from pathlib import Path
from PIL import Image


INPUT_PATH = "sticker_sheet.png"  # 입력 파일 경로를 여기에 지정
OUTPUT_DIR = "output"

CANVAS_W = 4440
CANVAS_H = 2560
COLS = 6
ROWS = 4
CELL_W = 740   # CANVAS_W / COLS
CELL_H = 640   # CANVAS_H / ROWS


def main():
    src = Path(INPUT_PATH)
    if not src.exists():
        print(f"[오류] 입력 파일을 찾을 수 없습니다: {INPUT_PATH}")
        return

    img = Image.open(src)
    orig_w, orig_h = img.size
    print(f"원본 이미지 크기: {orig_w} × {orig_h}px")

    if orig_w != CANVAS_W:
        print(f"[경고] 원본 너비({orig_w}px)가 {CANVAS_W}px와 다릅니다. 계속 진행합니다.")

    # 세로 중앙 정렬 crop
    crop_x = 0
    crop_y = round((orig_h - CANVAS_H) / 2)
    print(f"crop 시작 좌표: x={crop_x}, y={crop_y}")
    print(f"crop 영역: {CANVAS_W} × {CANVAS_H}px")

    canvas = img.crop((crop_x, crop_y, crop_x + CANVAS_W, crop_y + CANVAS_H))

    if canvas.size != (CANVAS_W, CANVAS_H):
        print(f"[오류] crop 결과 크기 불일치: {canvas.size}")
        return

    out_dir = Path(OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n--- 스티커 분할 시작 ---")
    errors = []

    for row in range(ROWS):
        for col in range(COLS):
            idx = row * COLS + col + 1
            left   = col * CELL_W
            upper  = row * CELL_H
            right  = left + CELL_W
            lower  = upper + CELL_H

            cell = canvas.crop((left, upper, right, lower))

            # RGBA 유지 (알파 채널 보존)
            if cell.mode != "RGBA":
                cell = cell.convert("RGBA")

            out_path = out_dir / f"sticker_{idx:02d}.png"
            cell.save(out_path, format="PNG")

            w, h = cell.size
            status = "OK" if (w == CELL_W and h == CELL_H) else "ERROR"
            if status == "ERROR":
                errors.append(out_path.name)
            print(f"  sticker_{idx:02d}.png  {w} × {h}px  [{status}]")

    print(f"\n--- 완료: {ROWS * COLS}개 파일 저장 → {out_dir.resolve()} ---")
    if errors:
        print(f"[오류] 크기 불일치 파일: {errors}")
    else:
        print("모든 파일 크기 검증 통과 (740 × 640px)")


if __name__ == "__main__":
    main()
