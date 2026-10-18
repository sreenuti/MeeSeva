from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from app.config import Settings

ScanStatus = Literal["pending", "clean", "infected", "failed"]

# Standard EICAR test string used for synthetic malware testing (not a real virus).
EICAR = b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"


@dataclass
class ScanResult:
    status: ScanStatus
    detail: str | None = None


class MalwareScanner:
    def scan(self, content: bytes, *, filename: str) -> ScanResult:
        raise NotImplementedError


class StubMalwareScanner(MalwareScanner):
    """Fail-closed stub: marks EICAR as infected; otherwise clean.

    Replace with ClamAV/external scanner in production. Documents remain
    non-downloadable until status is clean.
    """

    def scan(self, content: bytes, *, filename: str) -> ScanResult:
        if EICAR in content or content.startswith(EICAR[:20]):
            return ScanResult(status="infected", detail="EICAR test signature detected")
        # PDF/image polyglot heuristic: reject executable MZ header disguised uploads
        if content.startswith(b"MZ"):
            return ScanResult(status="infected", detail="Executable content detected")
        return ScanResult(status="clean", detail="stub_scanner")


class ClamAVScanner(MalwareScanner):
    def __init__(self, host: str, port: int, fail_closed: bool = True):
        self.host = host
        self.port = port
        self.fail_closed = fail_closed

    def scan(self, content: bytes, *, filename: str) -> ScanResult:
        try:
            import socket

            with socket.create_connection((self.host, self.port), timeout=10) as sock:
                sock.sendall(b"zINSTREAM\0")
                chunk_size = 2048
                for i in range(0, len(content), chunk_size):
                    chunk = content[i : i + chunk_size]
                    sock.sendall(len(chunk).to_bytes(4, "big") + chunk)
                sock.sendall((0).to_bytes(4, "big"))
                response = sock.recv(4096).decode("utf-8", errors="replace")
            if "OK" in response and "FOUND" not in response:
                return ScanResult(status="clean", detail=response.strip())
            if "FOUND" in response:
                return ScanResult(status="infected", detail=response.strip())
            if self.fail_closed:
                return ScanResult(status="failed", detail=response.strip())
            return ScanResult(status="failed", detail=response.strip())
        except Exception as exc:
            if self.fail_closed:
                return ScanResult(status="failed", detail=f"scan_error:{exc.__class__.__name__}")
            return ScanResult(status="failed", detail=f"scan_error:{exc.__class__.__name__}")


def build_scanner(settings: Settings) -> MalwareScanner:
    if settings.malware_scanner == "clamav":
        return ClamAVScanner(settings.clamav_host, settings.clamav_port, settings.fail_closed_on_scan_error)
    return StubMalwareScanner()
