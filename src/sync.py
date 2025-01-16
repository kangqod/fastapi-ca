import asyncio
import threading
import time
from datetime import datetime

from fastapi import APIRouter

router = APIRouter(prefix="/sync-test", tags=["sync-test"])


async def async_task(num: int):
    print("sync_task : ", num)
    if num == 100:
        raise ValueError(f"Error in task {num}")
    await asyncio.sleep(3)
    return num


# 실행할 함수 정의
def print_numbers():
    for i in range(1, 6):
        print(f"Number: {i}")
        time.sleep(1)  # 1초 대기


def print_letters():
    for letter in ["A", "B", "C", "D", "E"]:
        print(f"Letter: {letter}")
        time.sleep(3)  # 1초 대기


@router.get("")
async def async_example():
    now = datetime.now()
    tasks = [async_task(i) for i in range(1, 101)]  # 1부터 100까지의 작업 리스트 생성
    results = await asyncio.gather(*tasks)  # 모든 작업을 비동기로 실행

    print(datetime.now() - now)

    return {"results": results}


@router.get("/threading")
def processing_example():
    # 두 개의 쓰레드 생성
    thread1 = threading.Thread(target=print_numbers)
    thread2 = threading.Thread(target=print_letters)

    # 쓰레드 시작
    thread1.start()
    thread2.start()

    # 쓰레드가 종료될 때까지 기다리기
    thread1.join()
    thread2.join()

    return {"results": "good"}
