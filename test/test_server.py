import pytest
import requests
import time
import threading
from os.path import abspath, dirname, join

GAMESERVER_URL = "http://localhost:5000"

@pytest.mark.parametrize("n, threshold", [(1, 1), (10, 1), (100, 1), (1000, 1)])
def test_latency(n, threshold):
    """
    Test latency of requests
    """

    threads = []
    for i in range(n):
        threads.append(GameThread(i))
        threads[-1].start()

    avg_latency = 0
    max_latency = 0
    min_latency = float("inf")
    count = 0

    for thread in threads:
        thread.join()
        count += len(thread.latencies)
        avg_latency += sum(thread.latencies)
        max_latency = max(thread.latencies) if max(thread.latencies) > max_latency else max_latency
        min_latency = min(thread.latencies) if min(thread.latencies) < min_latency else min_latency

    avg_latency = avg_latency / count

    print(f"n: {n}, threshold: {threshold}, avg: {avg_latency}, max: {max_latency}, min: {min_latency}")

    path = dirname(abspath(__file__))
    filename = join(path, f"latencies.txt")
    with open(filename, "a") as f:
        f.write(f"n: {n}, threshold: {threshold}, avg: {avg_latency}, max: {max_latency}, min: {min_latency}\n")

    assert avg_latency < threshold, f"Too high average latency {avg_latency} > {threshold}"


def test_end_game():
    """
    Check that game ends properly when both players have ended the game
    """
    # Create game
    resp = requests.get(GAMESERVER_URL + f"/creategame")
    data = resp.json()
    assert resp.status_code == 200
    assert "game_id" in data
    assert "token" in data

    game_id = data["game_id"]
    token1 = data["token"]

    # Join game
    resp = requests.post(GAMESERVER_URL + f"/{game_id}/joingame")
    data = resp.json()
    assert resp.status_code == 200
    assert "token" in data

    token2 = data["token"]

    # Try to end two games at the same time
    url = GAMESERVER_URL + f"/{game_id}/endgame"
    t1 = SendRequestThread("post", url, json={"token": token1})
    t2 = SendRequestThread("post", url, json={"token": token2})

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    data1 = t1.data
    data2 = t2.data

    assert data1["message"] == "Game deleted" or data2["message"] == "Game deleted"
    assert data1["message"] == "Player removed from game" or data2["message"] == "Player removed from game"


class GameThread(threading.Thread):

    def __init__(self, number):
        super().__init__(target=self.play_game, kwargs={"number": number})


    def play_game(self, number):
        """
        Play game and measure latencies of each request
        """
        self.latencies = []

        start = time.time()
        resp = requests.get(GAMESERVER_URL + f"/creategame")
        end = time.time()
        self.latencies.append(end - start)
        data = resp.json()
        assert resp.status_code == 200, f"Game {number} failed"
        assert "game_id" in data, f"Game {number} failed"
        assert "token" in data, f"Game {number} failed"

        game_id = data["game_id"]
        token1 = data["token"]

        start = time.time()
        resp = requests.post(GAMESERVER_URL + f"/{game_id}/joingame")
        end = time.time()
        self.latencies.append(end - start)
        data = resp.json()
        assert resp.status_code == 200, f"Game {number} failed"
        assert "token" in data, f"Game {number} failed"

        token2 = data["token"]

        start = time.time()
        resp = requests.post(GAMESERVER_URL + f"/{game_id}/play", json={"token": token1, "x": 0, "y": 0})
        end = time.time()
        self.latencies.append(end - start)
        data = resp.json()
        assert resp.status_code == 200, f"Game {number} failed"
        assert "status" in data, f"Game {number} failed"
        assert "board" in data, f"Game {number} failed"
        assert "turn" in data, f"Game {number} failed"
        assert data["status"] == 1, f"Game {number} failed"

        start = time.time()
        resp = requests.post(GAMESERVER_URL + f"/{game_id}/play", json={"token": token2, "x": 0, "y": 1})
        end = time.time()
        self.latencies.append(end - start)
        data = resp.json()
        assert resp.status_code == 200, f"Game {number} failed"
        assert "status" in data, f"Game {number} failed"
        assert "board" in data, f"Game {number} failed"
        assert "turn" in data, f"Game {number} failed"
        assert data["status"] == 1, f"Game {number} failed"

        start = time.time()
        resp = requests.post(GAMESERVER_URL + f"/{game_id}/play", json={"token": token1, "x": 1, "y": 1})
        end = time.time()
        self.latencies.append(end - start)
        data = resp.json()
        assert resp.status_code == 200, f"Game {number} failed"
        assert "status" in data, f"Game {number} failed"
        assert "board" in data, f"Game {number} failed"
        assert "turn" in data, f"Game {number} failed"
        assert data["status"] == 1, f"Game {number} failed"

        start = time.time()
        resp = requests.post(GAMESERVER_URL + f"/{game_id}/play", json={"token": token2, "x": 0, "y": 2})
        end = time.time()
        self.latencies.append(end - start)
        data = resp.json()
        assert resp.status_code == 200, f"Game {number} failed"
        assert "status" in data, f"Game {number} failed"
        assert "board" in data, f"Game {number} failed"
        assert "turn" in data, f"Game {number} failed"
        assert data["status"] == 1, f"Game {number} failed"

        start = time.time()
        resp = requests.post(GAMESERVER_URL + f"/{game_id}/play", json={"token": token1, "x": 2, "y": 2})
        end = time.time()
        self.latencies.append(end - start)
        data = resp.json()
        assert resp.status_code == 200, f"Game {number} failed"
        assert "status" in data, f"Game {number} failed"
        assert "board" in data, f"Game {number} failed"
        assert "turn" in data, f"Game {number} failed"

        resp = requests.post(GAMESERVER_URL + f"/{game_id}/endgame", json={"token": token1})
        assert resp.status_code == 200, f"Game {number} failed"
        resp = requests.post(GAMESERVER_URL + f"/{game_id}/endgame", json={"token": token2})
        assert resp.status_code == 200, f"Game {number} failed"


class SendRequestThread(threading.Thread):
    def __init__(self, method, url, json=None):
        super().__init__(target=self.send_request, kwargs={"method": method, "url": url, "json": json})
        self.data = None

    def send_request(self, method, url, json=None):
        if method == "get":
            resp = requests.get(url)
            self.data = resp.json()
        elif method == "post":
            resp = requests.post(url, json=json)
            self.data = resp.json()
