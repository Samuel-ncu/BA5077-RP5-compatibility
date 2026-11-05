from pathlib import Path
import json
import cv2
import numpy as np
from picamera2 import Picamera2

# 10x7 格子會有 9x6 = 54 個內角點。
PATTERN = (9, 6)
MIN_VIEWS = 10
OUTPUT_DIR = Path("calibration-data")
OUTPUT_DIR.mkdir(exist_ok=True)
if any(OUTPUT_DIR.iterdir()):
    raise FileExistsError(
        f"{OUTPUT_DIR} 已有檔案。請先備份舊資料，或在程式中指定新的空資料夾。"
    )

criteria = (
    cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
    30,
    0.001,
)
object_template = np.zeros((PATTERN[0] * PATTERN[1], 3), np.float32)
object_template[:, :2] = np.mgrid[0:PATTERN[0], 0:PATTERN[1]].T.reshape(-1, 2)

object_points = []
image_points = []
saved_frames = []
view_signatures = []
camera = Picamera2()
camera.configure(
    camera.create_preview_configuration(
        main={"size": (1280, 720), "format": "RGB888"}
    )
)

try:
    camera.start()
    print("棋盤請使用 10x7 個方格（9x6 個內角點）。")
    print("逐次改變距離、傾斜角度與畫面位置；不要只連拍同一姿勢。")
    print("空白鍵：保存有效的 54 點畫面；c：計算（至少 10 個視角）；q：結束。")

    while True:
        frame = camera.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found, corners = cv2.findChessboardCorners(
            gray,
            PATTERN,
            cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE,
        )
        preview = frame.copy()
        status = "54 corners found" if found else "Move board into view"
        if found:
            refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            cv2.drawChessboardCorners(preview, PATTERN, refined, found)
        else:
            refined = None
        cv2.putText(
            preview,
            f"{status} | saved views: {len(image_points)}",
            (18, 36),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0) if found else (0, 0, 255),
            2,
        )
        cv2.imshow("Calibration: Space save, C calibrate, Q quit", preview)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        if key == ord(" ") and found:
            points = refined.reshape(-1, 2)
            min_xy = points.min(axis=0)
            max_xy = points.max(axis=0)
            center = points.mean(axis=0) / np.array([gray.shape[1], gray.shape[0]])
            box_size = (max_xy - min_xy) / np.array([gray.shape[1], gray.shape[0]])
            area = float(box_size[0] * box_size[1])
            aspect = float(box_size[0] / max(box_size[1], 1e-6))
            top_edge = points[PATTERN[0] - 1] - points[0]
            angle = float(np.degrees(np.arctan2(top_edge[1], top_edge[0])))
            signature = {
                "center": center,
                "area": area,
                "aspect": aspect,
                "angle": angle,
            }
            diverse = bool(view_signatures)
            for previous in view_signatures:
                center_delta = float(np.linalg.norm(signature["center"] - previous["center"]))
                size_ratio = max(signature["area"], previous["area"]) / max(
                    min(signature["area"], previous["area"]), 1e-6
                )
                aspect_delta = abs(signature["aspect"] - previous["aspect"]) / max(
                    previous["aspect"], 1e-6
                )
                angle_delta = abs((signature["angle"] - previous["angle"] + 180) % 360 - 180)
                if not (
                    center_delta >= 0.06
                    or size_ratio >= 1.15
                    or aspect_delta >= 0.10
                    or angle_delta >= 7.0
                ):
                    diverse = False
                    break
            if not diverse:
                print("視角與已保存資料太接近；請改變棋盤位置、距離或傾斜角度。")
                continue
            index = len(image_points) + 1
            filename = OUTPUT_DIR / f"view-{index:02d}.jpg"
            if not cv2.imwrite(str(filename), frame):
                raise RuntimeError(f"無法保存 {filename}")
            object_points.append(object_template.copy())
            image_points.append(refined.copy())
            saved_frames.append(frame.copy())
            view_signatures.append(signature)
            print(f"saved view {index}: 54/54 corners; distinct view accepted")
        elif key == ord(" ") and not found:
            print("未偵測到完整 54 點；移動棋盤、改善光線後再試。")
        elif key == ord("c"):
            if len(image_points) < MIN_VIEWS:
                print(f"目前只有 {len(image_points)} 個有效視角；至少需要 {MIN_VIEWS} 個。")
                continue
            height, width = gray.shape
            result = cv2.calibrateCameraExtended(
                object_points,
                image_points,
                (width, height),
                None,
                None,
            )
            rms, matrix, distortion, rvecs, tvecs, _, _, per_view_errors = result
            data = {
                "resolution": {"width": width, "height": height},
                "checkerboard": {
                    "squares": [10, 7],
                    "inner_corners": [9, 6],
                    "detected_corners_per_view": 54,
                    "valid_views": len(image_points),
                    "square_size_unit": "one square (relative scale)",
                },
                "camera_matrix": matrix.tolist(),
                "distortion_coefficients": distortion.reshape(-1).tolist(),
                "rms_reprojection_error_pixels": float(rms),
                "per_view_reprojection_error_pixels": [
                    float(value) for value in per_view_errors.reshape(-1)
                ],
            }
            result_path = OUTPUT_DIR / "camera-calibration.json"
            result_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            sample = saved_frames[0]
            undistorted = cv2.undistort(sample, matrix, distortion)
            undistorted_path = OUTPUT_DIR / "undistorted-preview.jpg"
            if not cv2.imwrite(str(undistorted_path), undistorted):
                raise RuntimeError(f"無法保存 {undistorted_path}")
            print("valid views:", len(image_points))
            print("RMS reprojection error (pixels):", float(rms))
            print("saved:", result_path)
            print("saved:", undistorted_path)
            break
finally:
    camera.stop()
    camera.close()
    cv2.destroyAllWindows()
