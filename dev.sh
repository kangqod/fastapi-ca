#!/bin/bash

# Docker Compose 프로젝트 디렉토리로 이동 (필요에 따라 수정)
PROJECT_DIR="$(pwd)"

# 컨테이너 이름
CONTAINER_NAME="mysql-local"

# Docker Compose 파일 경로 설정
DOCKER_COMPOSE_FILE="-f docker-compose.dev.yml"

# 도움말 출력 함수
print_help() {
    echo "Usage: $0 {u|d|r|l|p|b|s|c}"
    echo "Commands:"
    echo "  u       - Start the containers in the background (up)"
    echo "  d       - Stop the containers and remove them (down)"
    echo "  r       - Restart the containers (restart)"
    echo "  l       - View logs from the containers (logs)"
    echo "  p       - List running containers (ps)"
    echo "  b       - Build the services (build)"
    echo "  s       - Show the status of the services (status)"
    echo "  c       - Clean up containers, volumes, and networks (clean)"
}

# 'u' (up) 명령어 - 백그라운드에서 컨테이너 실행
u() {
    echo "Starting containers..."
    docker-compose $DOCKER_COMPOSE_FILE up -d
}

# 'd' (down) 명령어 - 컨테이너 중지 및 삭제
d() {
    echo "Stopping and removing containers..."
    docker-compose $DOCKER_COMPOSE_FILE down
}

# 'r' (restart) 명령어 - 컨테이너 재시작
r() {
    echo "Restarting containers..."
    docker-compose $DOCKER_COMPOSE_FILE down
    docker-compose $DOCKER_COMPOSE_FILE up -d
}

# 'l' (logs) 명령어 - 컨테이너 로그 확인
l() {
    echo "Viewing logs..."
    docker-compose $DOCKER_COMPOSE_FILE logs
}

# 'p' (ps) 명령어 - 실행 중인 컨테이너 목록
p() {
    echo "Listing containers..."
    docker-compose $DOCKER_COMPOSE_FILE ps
}

# 'b' (build) 명령어 - 서비스 빌드
b() {
    echo "Building services..."
    docker-compose $DOCKER_COMPOSE_FILE build
}

# 's' (status) 명령어 - 서비스 상태 확인
s() {
    docker-compose $DOCKER_COMPOSE_FILE ps
}

# 'c' (clean) 명령어 - 컨테이너, 네트워크, 볼륨 모두 제거
c() {
    echo "Cleaning up containers, volumes, and networks..."
    docker-compose $DOCKER_COMPOSE_FILE down -v --remove-orphans
}

# 명령어 인수 처리
if [ $# -eq 0 ]; then
    print_help
    exit 1
fi

case "$1" in
    u)
        u
        ;;
    d)
        d
        ;;
    r)
        r
        ;;
    l)
        l
        ;;
    p)
        p
        ;;
    b)
        b
        ;;
    s)
        s
        ;;
    c)
        c
        ;;
    *)
        print_help
        exit 1
        ;;
esac
