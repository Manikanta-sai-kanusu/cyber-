import socket
import threading
import time
from typing import Callable, Tuple


def safe_handler(handler, conn, addr, name):
    """Prevents one service crash from killing the whole system"""
    try:
        handler(conn, addr)
    except Exception as e:
        print(f"[ERROR] {name} handler crash: {e}")
    finally:
        try:
            conn.close()
        except:
            pass


def start_listener(port: int, handler: Callable, name: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind(("0.0.0.0", port))
    except OSError as e:
        print(f"[ERROR] Could not bind {name} on port {port}: {e}")
        return

    s.listen(5)
    print(f"[*] {name} honeypot listening on port {port}")

    while True:
        try:
            conn, addr = s.accept()

            threading.Thread(
                target=safe_handler,
                args=(handler, conn, addr, name),
                daemon=True
            ).start()

        except Exception as e:
            print(f"[ERROR] Listener {name}: {e}")
            continue


def run_all_services():
    from ssh_service import fake_ssh
    from http_service import fake_http
    from smb_service import fake_smb
    from rdp_service import fake_rdp

    services = [
        (2222, "SSH", fake_ssh),
        (8080, "HTTP", fake_http),
        (4445, "SMB", fake_smb),
        (3389, "RDP", fake_rdp),
    ]

    for port, name, handler in services:
        t = threading.Thread(
            target=start_listener,
            args=(port, handler, name),
            daemon=True
        )
        t.start()
        time.sleep(0.2)  # IMPORTANT: prevents Windows race issues

    print("[*] All honeypot services running. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Shutting down cleanly.")


if __name__ == "__main__":
    run_all_services()