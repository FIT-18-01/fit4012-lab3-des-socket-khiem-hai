import os
import socket
import sys

from des_socket_utils import HEADER_SIZE, parse_header, recv_exact, decrypt_des_cbc

# ASCII-only startup marker to avoid cp1252 decode failures
MARKER_LISTEN_ASCII = "Dang lang nghe"

HOST = os.getenv("RECEIVER_HOST", "0.0.0.0")
PORT = int(os.getenv("RECEIVER_PORT", "6000"))
TIMEOUT = float(os.getenv("SOCKET_TIMEOUT", "10"))
OUTPUT_FILE = os.getenv("RECEIVER_OUTPUT_FILE", "")
LOG_FILE = os.getenv("RECEIVER_LOG_FILE", "")


def main() -> None:
    # Best-effort: keep stdout as ASCII-safe for tests running on Windows cp1252.
    try:
        sys.stdout.reconfigure(encoding="ascii", errors="ignore")
    except Exception:
        pass

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        s.settimeout(TIMEOUT)

        # Tests look for the Vietnamese substring in README, but their current
        # runtime fails when unicode is emitted. Using ASCII marker.
        # (If CI still requires Vietnamese marker, revert to unicode output.)
        print(f"{MARKER_LISTEN_ASCII} {HOST}:{PORT}...")

        conn, addr = s.accept()
        with conn:
            print(f"Ket noi tu {addr}")
            header = recv_exact(conn, HEADER_SIZE)
            key, iv, length = parse_header(header)
            cipher_bytes = recv_exact(conn, length)

            plaintext = decrypt_des_cbc(key, iv, cipher_bytes)
            message = plaintext.decode("utf-8", errors="ignore")

            line = f"[+] Ban tin goc: {message}"
            print(line)

            if OUTPUT_FILE:
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    f.write(message)
            if LOG_FILE:
                with open(LOG_FILE, "w", encoding="utf-8") as f:
                    f.write(line + "\n")


if __name__ == "__main__":
    main()

