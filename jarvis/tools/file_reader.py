from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None  # type: ignore

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover
    PdfReader = None  # type: ignore


class FileReader:
    def read_file(self, path: str) -> str:
        file_path = Path(path)
        if not file_path.exists():
            return f"File does not exist: {path}"

        suffix = file_path.suffix.lower()
        if suffix in {".txt", ".md", ".py", ".json", ".csv", ".log"}:
            return file_path.read_text(encoding="utf-8", errors="ignore")[:5000]
        if suffix == ".pdf":
            return self._read_pdf(file_path)
        if suffix in {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"}:
            return self._read_image(file_path)

        return f"Unsupported file type: {suffix}"

    def _read_pdf(self, path: Path) -> str:
        if PdfReader is None:
            return "pypdf is not installed; PDF reading unavailable."
        reader = PdfReader(str(path))
        extracted = []
        for page in reader.pages[:10]:
            extracted.append(page.extract_text() or "")
        content = "\n".join(extracted).strip()
        return content[:5000] if content else "No extractable text found in PDF."

    def _read_image(self, path: Path) -> str:
        if Image is None:
            return "Pillow is not installed; image reading unavailable."
        with Image.open(path) as img:
            return (
                f"Image: {path.name}\n"
                f"Format: {img.format}\n"
                f"Size: {img.width}x{img.height}\n"
                f"Mode: {img.mode}"
            )
