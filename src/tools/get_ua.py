import asyncio
import socket
from threading import Thread

from curl_cffi import requests


def get_ua(impersonate: str) -> str:
    ua = ""

    async def handler(r, w):
        nonlocal ua
        data = await r.readuntil(b"\r\n\r\n")
        ua = next(
            (
                line.split(b":", 1)[1].decode().strip()
                for line in data.split(b"\r\n")
                if line.lower().startswith(b"user-agent:")
            ),
            "",
        )
        w.write(b"HTTP/1.1 200 OK\r\n\r\n")
        w.close()

    async def run():
        srv = await asyncio.start_server(handler, "127.0.0.1", 0)
        port = srv.sockets[0].getsockname()[1]
        await asyncio.to_thread(
            requests.get, f"http://127.0.0.1:{port}", impersonate=impersonate
        )
        srv.close()
        await srv.wait_closed()

    asyncio.run(run())
    return ua


def get_ua_sync(impersonate: str) -> str:
    with socket.socket() as server:
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        port = server.getsockname()[1]

        thread = Thread(
            target=requests.get,
            args=(f"http://127.0.0.1:{port}",),
            kwargs={"impersonate": impersonate},
        )
        thread.start()

        conn, _ = server.accept()
        with conn:
            data = b""
            while b"\r\n\r\n" not in data:
                data += conn.recv(4096)
            conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

        thread.join()

    return next(
        (
            line.split(b":", 1)[1].decode().strip()
            for line in data.split(b"\r\n")
            if line.lower().startswith(b"user-agent:")
        ),
        "",
    )


if __name__ == "__main__":
    print(get_ua("chrome146"))
    print(get_ua_sync("chrome146"))
