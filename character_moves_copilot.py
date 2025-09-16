from pico2d import *
import math

open_canvas()

# 리소스 로드
character = load_image('character.png')

# 캐릭터 기준점
BASE_X, BASE_Y = 400, 30

def draw_rectangle_path(t):
    """사각형 경로: 캔버스를 거의 꽉 채우는 사각형"""
    # 사각형의 네 모서리 좌표 (여백 50픽셀)
    corners = [(100, 100), (700, 100), (700, 500), (100, 500)]

    # 각 변의 길이에 따른 t 구간 분할
    total_length = 600 + 400 + 600 + 400  # 사각형 둘레
    segment_lengths = [600, 400, 600, 400]

    # 현재 t가 어느 변에 있는지 찾기
    current_t = t * total_length
    accumulated = 0

    for i, length in enumerate(segment_lengths):
        if current_t <= accumulated + length:
            # 현재 변에서의 진행도
            segment_t = (current_t - accumulated) / length
            start = corners[i]
            end = corners[(i + 1) % 4]

            x = start[0] + (end[0] - start[0]) * segment_t
            y = start[1] + (end[1] - start[1]) * segment_t

            # (400, 30)을 지나가도록 조정
            if i == 0:  # 하단 변
                if abs(x - BASE_X) < 10:
                    y = BASE_Y

            return x, y
        accumulated += length

    return corners[0]

def draw_triangle_path(t):
    """삼각형 경로: 이등변삼각형 (대각선 2개)"""
    # 삼각형의 세 꼭짓점 (캔버스를 거의 꽉 채움)
    vertices = [(400, 550), (100, 100), (700, 100)]  # 위쪽 꼭짓점, 왼쪽 아래, 오른쪽 아래

    # 각 변의 길이 계산
    def distance(p1, p2):
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

    side_lengths = [
        distance(vertices[0], vertices[1]),  # 왼쪽 변
        distance(vertices[1], vertices[2]),  # 아래 변
        distance(vertices[2], vertices[0])   # 오른쪽 변
    ]

    total_length = sum(side_lengths)
    current_t = t * total_length
    accumulated = 0

    for i, length in enumerate(side_lengths):
        if current_t <= accumulated + length:
            segment_t = (current_t - accumulated) / length
            start = vertices[i]
            end = vertices[(i + 1) % 3]

            x = start[0] + (end[0] - start[0]) * segment_t
            y = start[1] + (end[1] - start[1]) * segment_t

            # (400, 30)을 지나가도록 조정
            if i == 1:  # 아래 변
                if abs(x - BASE_X) < 10:
                    y = BASE_Y

            return x, y
        accumulated += length

    return vertices[0]

def draw_circle_path(t):
    """원 경로: 캔버스를 거의 꽉 채우는 원"""
    center_x, center_y = 400, 300
    radius = 250  # 캔버스를 거의 꽉 채우는 반지름

    # 원 위의 점 계산 (시계방향으로 회전)
    angle = t * 2 * math.pi
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)

    # (400, 30)을 지나가도록 조정 (가장 아래쪽 부분에서)
    if abs(angle - math.pi/2) < 0.1:  # 아래쪽에서
        y = BASE_Y

    return x, y

# 메인 루프
frame = 0
running = True

while running:
    clear_canvas()

    # 현재 시간 계산 (0~3 사이를 반복)
    cycle_time = (frame // 100) % 3  # 100프레임마다 도형 변경
    t = (frame % 100) / 99.0  # 0~1 사이의 값

    # 현재 도형에 따라 위치 계산
    if cycle_time == 0:  # 사각형
        x, y = draw_rectangle_path(t)
    elif cycle_time == 1:  # 삼각형
        x, y = draw_triangle_path(t)
    else:  # 원
        x, y = draw_circle_path(t)

    # 캐릭터 그리기
    character.draw(x, y)

    update_canvas()
    delay(0.05)
    frame += 1

    # ESC 키로 종료
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False

close_canvas()
