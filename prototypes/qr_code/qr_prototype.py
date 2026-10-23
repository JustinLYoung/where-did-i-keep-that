
"""Generate a QR code linked to a storage location."""

import argparse
from pathlib import Path
from urllib.parse import urlparse

import qrcode


def generate_qr(location_url: str, output_path: Path) -> Path:
    """Generate and save a QR code as a PNG file."""
    parsed = urlparse(location_url)

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("Location URL must begin with http:// or https://")

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    qr.add_data(location_url)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")
    image.save(output_path)

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a sample QR label")
    parser.add_argument("url", help="URL of the storage location")
    parser.add_argument("--output", default="sample_location_qr.png")
    args = parser.parse_args()

    try:
        output = generate_qr(args.url, Path(args.output))
    except ValueError as exc:
        parser.error(str(exc))

    print(f"Created: {output}")
    print(f"Encoded URL: {args.url}")


if __name__ == "__main__":
    main()
