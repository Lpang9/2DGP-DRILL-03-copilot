from pico2d import *
import math

open_canvas()

# 리소스 로드
character = load_image('character.png')

# 캐릭터 기준점
BASE_X, BASE_Y = 400, 30

def draw_rectangle_path(t):
    """사각형 경로: 캔버스를 거의 꽉 채우는 사각형"""
    # 사각형의 네 모서리 좌표 - (400,30)에서 시작해서 오른쪽->위쪽->왼쪽->아래쪽->다시 (400,30)으로
    corners = [(BASE_X, BASE_Y), (780, BASE_Y), (780, 550), (20, 550), (20, BASE_Y), (BASE_X, BASE_Y)]

    # 각 변의 길이 계산
    def distance(p1, p2):
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

    segment_lengths = []
    for i in range(len(corners) - 1):
        segment_lengths.append(distance(corners[i], corners[i + 1]))

    total_length = sum(segment_lengths)
    current_t = t * total_length
    accumulated = 0

    for i, length in enumerate(segment_lengths):
        if current_t <= accumulated + length:
            segment_t = (current_t - accumulated) / length
            start = corners[i]
            end = corners[i + 1]

            x = start[0] + (end[0] - start[0]) * segment_t
            y = start[1] + (end[1] - start[1]) * segment_t

            return x, y
        accumulated += length

    return corners[-1]  # 마지막 점 반환

def draw_triangle_path(t):
    """삼각형 경로: (400,30)에서 시작해서 끝나는 이등변삼각형"""
    # 삼각형의 꼭짓점들 - (400,30) -> 오른쪽 밑 -> 위쪽 꼭짓점 -> 왼쪽 밑 -> (400,30)
    vertices = [(BASE_X, BASE_Y), (780, BASE_Y), (400, 550), (20, BASE_Y), (BASE_X, BASE_Y)]

    def distance(p1, p2):
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

    segment_lengths = []
    for i in range(len(vertices) - 1):
        segment_lengths.append(distance(vertices[i], vertices[i + 1]))

    total_length = sum(segment_lengths)
    current_t = t * total_length
    accumulated = 0

    for i, length in enumerate(segment_lengths):
        if current_t <= accumulated + length:
            segment_t = (current_t - accumulated) / length
            start = vertices[i]
            end = vertices[i + 1]

            x = start[0] + (end[0] - start[0]) * segment_t
            y = start[1] + (end[1] - start[1]) * segment_t

            return x, y
        accumulated += length

    return vertices[-1]

def draw_circle_path(t):
    """원 경로: (400, 30)에서 시작해서 한 바퀴 돌고 다시 (400, 30)으로"""
    center_x, center_y = 400, 300
    # (400, 30)이 원 위에 있도록 반지름 계산
    radius = abs(center_y - BASE_Y)  # 270

    # (400, 30)에서 시작하는 각도 계산
    start_angle = -math.pi / 2  # 아래쪽에서 시작

    # 시계방향으로 한 바퀴
    angle = start_angle + t * 2 * math.pi
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)

    return x, y

# 메인 루프
frame = 0
running = True

while running:
    clear_canvas()

    # 전체 사이클을 더 길게 설정 (각 도형당 150프레임)
    cycle_length = 150
    total_cycle_time = cycle_length * 3  # 사각형, 삼각형, 원

    # 현재 위치 계산 - 부드러운 전환을 위해 수정
    current_frame = frame % total_cycle_time

    if current_frame < cycle_length:  # 사각형
        t = current_frame / cycle_length  # cycle_length - 1 대신 cycle_length 사용
        x, y = draw_rectangle_path(t)
    elif current_frame < cycle_length * 2:  # 삼각형
        t = (current_frame - cycle_length) / cycle_length  # cycle_length - 1 대신 cycle_length 사용
        x, y = draw_triangle_path(t)
    else:  # 원
        t = (current_frame - cycle_length * 2) / cycle_length  # cycle_length - 1 대신 cycle_length 사용
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
