"""Smoke test for /api/v1/predict/airline using FastAPI TestClient.
Runs locally (no server) and prints the response JSON.
"""
import asyncio
from app import predict_airline


def main():
    payload = {
        'month': 7,
        'day': 15,
        'crs_dep_time': 900,
        'crs_arr_time': 1100,
        'crs_elapsed': 120,
        'distance': 800,
        'origin': 'IAD',
        'dest': 'TPA',
        'carrier': 'WN'
    }

    res = asyncio.run(predict_airline(payload))
    print('RESULT:', res)


if __name__ == '__main__':
    main()
