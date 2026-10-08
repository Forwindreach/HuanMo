from __future__ import annotations

import base64
from io import BytesIO

import cv2
import numpy as np

from md2pdf_app.app import PdfReader, app, process_scanned_image


def _encode_jpeg(image: np.ndarray) -> bytes:
    ok, encoded = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 98])
    assert ok
    return encoded.tobytes()


def _color_landscape_document() -> bytes:
    image = np.full((720, 1280, 3), 245, dtype=np.uint8)
    cv2.rectangle(image, (60, 70), (380, 650), (40, 40, 230), -1)
    cv2.rectangle(image, (480, 70), (800, 650), (40, 210, 40), -1)
    cv2.rectangle(image, (900, 70), (1220, 650), (230, 80, 30), -1)
    return _encode_jpeg(image)


def _perspective_document() -> bytes:
    page = np.full((1500, 1050, 3), (235, 245, 250), dtype=np.uint8)
    cv2.rectangle(page, (20, 20), (1030, 1480), (20, 30, 40), 7)
    cv2.putText(
        page,
        "HUANMO SCAN",
        (150, 190),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.8,
        (170, 40, 30),
        5,
    )
    for y in range(330, 1300, 100):
        cv2.line(page, (120, y), (900, y), (60, 70, 80), 8)

    canvas = np.full((1800, 1500, 3), 80, dtype=np.uint8)
    source = np.float32([[0, 0], [1049, 0], [1049, 1499], [0, 1499]])
    target = np.float32([[240, 140], [1280, 280], [1180, 1650], [120, 1510]])
    matrix = cv2.getPerspectiveTransform(source, target)
    photo = cv2.warpPerspective(
        page,
        matrix,
        (1500, 1800),
        dst=canvas,
        borderMode=cv2.BORDER_TRANSPARENT,
    )
    return _encode_jpeg(photo)


def test_scan_styles_preserve_expected_appearance() -> None:
    raw = _color_landscape_document()
    results = {}

    for style in ("original", "color", "bw"):
        processed, metadata = process_scanned_image(raw, style=style)
        decoded = cv2.imdecode(np.frombuffer(processed, np.uint8), cv2.IMREAD_UNCHANGED)
        results[style] = decoded
        assert metadata["style"] == style
        assert metadata["perspective_corrected"] is False

    original = results["original"]
    color = results["color"]
    black_white = results["bw"]

    assert original.shape[1] > original.shape[0]
    assert color.shape[1] > color.shape[0]
    assert original.ndim == 3
    assert color.ndim == 3
    assert cv2.cvtColor(original, cv2.COLOR_BGR2HSV)[:, :, 1].mean() > 70
    assert cv2.cvtColor(color, cv2.COLOR_BGR2HSV)[:, :, 1].mean() > 60
    assert black_white.ndim == 2


def test_perspective_detection_works_for_all_styles() -> None:
    raw = _perspective_document()

    for style in ("original", "color", "bw"):
        _, metadata = process_scanned_image(raw, style=style)
        assert metadata["perspective_corrected"] is True
        assert metadata["height"] > metadata["width"]


def test_rotation_and_pdf_export_keep_color(tmp_path) -> None:
    raw = _color_landscape_document()
    client = app.test_client()

    response = client.post(
        "/analyze-image",
        json={
            "name": "color-document.jpg",
            "content": base64.b64encode(raw).decode("ascii"),
            "style": "original",
        },
    )
    assert response.status_code == 200
    scan = response.get_json()
    token = scan["token"]

    response = client.post(f"/rotate-scan/{token}", json={"direction": "right"})
    assert response.status_code == 200
    preview = client.get(f"/scan-preview/{token}").data
    rotated = cv2.imdecode(np.frombuffer(preview, np.uint8), cv2.IMREAD_COLOR)
    assert cv2.cvtColor(rotated, cv2.COLOR_BGR2HSV)[:, :, 1].mean() > 70

    response = client.post(
        "/scan-pdf",
        json={"pages": [{"token": token}], "output_dir": str(tmp_path)},
    )
    assert response.status_code == 200
    result = response.get_json()
    pdf_bytes = (tmp_path / result["filename"]).read_bytes()
    reader = PdfReader(BytesIO(pdf_bytes))
    assert len(reader.pages) == 1

    xobjects = reader.pages[0]["/Resources"]["/XObject"].get_object()
    color_spaces = {str(item.get_object().get("/ColorSpace")) for item in xobjects.values()}
    assert "/DeviceRGB" in color_spaces
