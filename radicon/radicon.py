# encoding=utf-8

import time
import random
import dill

import cv2
import numpy as np

# -------------------------------
# ---------- CONSTANTS ----------
# -------------------------------
# screen size
SH, SW = 900-45, 1600
# camera capture frame size
FRAME_H, FRAME_W = 600, 800
# corners : [(top left), (top right), (bottom left), (bottom right)] : (x,y)
CORNER = [[172, 115], [674, 117], [214, 346], [630, 351]]
SCREEN = [[0, 0], [SW, 0], [0, SH], [SW, SH]]
pts1 = np.float32(CORNER)
pts2 = np.float32(SCREEN)
M = cv2.getPerspectiveTransform(pts1,pts2)

# threshold
TH = 130

# color
RED, GREEN, BLUE = (0, 0, 255), (0, 255, 0), (255, 0, 0)
MAGENTA, CYAN, YELLOW = (255, 0, 255), (255, 255, 0), (0, 255, 255)
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

# circle
R = 80 # 円の半径(直径？)

# Window name
GAME = 'Project O.M.R'

# FONT
#FONT = cv2.FONT_HERSHEY_PLAIN
FONT = cv2.FONT_HERSHEY_COMPLEX
FONT_SIZE = 1

# TIME
GAME_TIME = 30
LIFESPAN = 6 # [sec]
APPEAR_SPAN = 5 # [frame]
SPECIAL_SPAN = 23 # [frame]

# POINT
POINT = [1, 10]
COLOR = [YELLOW, CYAN]

# READY COUNT DOWN
READY_COUNT_DOWN = 5 # [sec]

# RANKING
# save file
RANKING_FILE = './data/ranking.pickle'
# num
RANKING_NUM = 10
# RANK_UNIT
RANK_UINT = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th']
RANK_COLOR = [RED, BLUE, MAGENTA, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK]
RANK_SIZE = [2, 1.6, 1.3, 1, 1, 1, 1, 1, 1, 1]


# -------------------------------
# ---------- VARIABLES ----------
# -------------------------------
get_point = 0 # 取得ポイントn
cnt = 0 # フレームカウント
point_circles = [] # 出現している得点円

meanX, meanY = -1, -1

# -----------------------------
# ---------- METHODS ----------
# -----------------------------

# --------------------------
# ---------- MAIN ----------
# --------------------------
# カメラキャプチャ
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

while True:
    ### INIT
    get_point = 0
    meanX, meanY = -1, -1

    ### ゲーム説明
    # 描画用スクリーン
    screen = np.ones((SH, SW, 3))*255

    # 時間経過の表示
    cv2.circle(screen, (SW-80, 80), 50, GREEN, 2)
    cv2.ellipse(screen, (SW-80, 80), (50, 50), 0, 270+200, 270+360, GREEN, -1)
    cv2.putText(screen, "remaining time", (SW-400, 150), FONT, 1, GREEN, 2)

    # 取得ポイントの表示
    #cv2.putText(effect, "%d"%get_point, (SW-200, SH-50), FONT, 2, GREEN, 3)
    cv2.rectangle(screen, (40, 20), (80, SH-20), GREEN, 2)
    h = get_point*3
    cv2.rectangle(screen, (40, SH-20-30), (80, SH-20), GREEN, -1)
    cv2.putText(screen, "point you get", (100, SH-60), FONT, 1, GREEN, 2)

    # 得点円の説明
    cv2.circle(screen, (500, 200), R, YELLOW, 10)
    cv2.ellipse(screen, (500, 200), (R,R), 0, 270+230, 270+360, YELLOW, -1)
    cv2.putText(screen, "1 point circle", (600, 200), FONT, 1, YELLOW, 2)

    cv2.circle(screen, (500, 400), R, CYAN, 10)
    cv2.ellipse(screen, (500, 400), (R,R), 0, 270+240, 270+360, CYAN, -1)
    cv2.putText(screen, "10 point circle", (600, 400), FONT, 1, CYAN, 2)

    # 表示
    cv2.imshow(GAME, screen)
    cv2.waitKey(0)


    ### ゲーム開始カウントダウン
    start = time.time()
    while True:
        elapsed_time = time.time() - start
        if elapsed_time > READY_COUNT_DOWN:
            break

        # 描画用スクリーン
        screen = np.ones((SH, SW, 3))*255

        # 時間経過の表示
        cv2.circle(screen, (SW-80, 80), 50, GREEN, 2)
        cv2.ellipse(screen, (SW-80, 80), (50, 50), 0, 270, 270+360, GREEN, -1)

        # 取得ポイントの表示
        #cv2.putText(effect, "%d"%get_point, (SW-200, SH-50), FONT, 2, GREEN, 3)
        cv2.rectangle(screen, (40, 20), (80, SH-20), GREEN, 2)

        # カウントダウン
        cv2.circle(screen, (SW//2, SH//2), 300, BLACK, 10)
        a = elapsed_time * 360 / READY_COUNT_DOWN
        cv2.ellipse(screen, (SW//2, SH//2), (300, 300), 0, 270+a, 270+360, BLACK, -1)

        # 表示
        cv2.imshow(GAME, screen)
        cv2.waitKey(1)


    ### ゲーム本編
    start = time.time()
    cnt = 0
    point_circles = []
    while True:
        # 経過時間
        elapsed_time = time.time() - start
        if elapsed_time > GAME_TIME:
            break

        ret, frame = cap.read() # 読み込み
        frame = cv2.warpPerspective(frame, M, (SW, SH)) # 投影部分の抽出

        # ラジコン検出
        det = np.array((frame[:, :, 0] < TH) * (frame[:, :, 1] < TH) * (frame[:, :, 2] < TH))
        detY, detX = np.where(det)
        if len(detY) == 0 or len(detX) == 0:
            # 検出なし
            meanX, meanY = -1, -1
        else:
            # 検出あり
            # 重心の計算
            meanX = int(round(np.average(detX)))
            meanY = int(round(np.average(detY)))

        # 描画用フレーム
        effect = np.ones((SH, SW, 3))*255

        # 得点円の追加
        if cnt % APPEAR_SPAN == 0: # 1 point
            x = random.randrange(SW)
            y = random.randrange(SH)
            point_circles.append((x, y, elapsed_time, 0))
        if cnt % SPECIAL_SPAN == 0: # 10 point
            x = random.randrange(SW)
            y = random.randrange(SH)
            point_circles.append((x, y, elapsed_time, 1))
        cnt += 1
        delete_circle = []
        for pc in point_circles:
            life = elapsed_time - pc[2]
            if life > LIFESPAN:
                # 寿命
                delete_circle.append(pc)
            else:
                # 表示
                cv2.circle(effect, (pc[0], pc[1]), R, COLOR[pc[3]], 10)
                a = life * 360 / LIFESPAN
                cv2.ellipse(effect, (pc[0], pc[1]), (R,R), 0, 270+a, 270+360, COLOR[pc[3]], -1)
                # 当たり判定
                if meanX == -1 or meanY == -1:
                    pass
                else:
                    if (meanX-pc[0])**2 + (meanY-pc[1])**2 < (2*R)**2:
                        get_point += POINT[pc[3]]
                        delete_circle.append(pc)

        # 得点円の削除
        for d in delete_circle:
            point_circles.remove(d)
        
        # ラジコン範囲の描画
        if meanX != -1 and meanY != -1:
            cv2.circle(effect, (meanX, meanY), R, GREEN, -1)

        # 時間経過の表示
        a = elapsed_time * 360 / GAME_TIME
        cv2.circle(effect, (SW-80, 80), 50, GREEN, 2)
        cv2.ellipse(effect, (SW-80, 80), (50, 50), 0, 270+a, 270+360, GREEN, -1)

        # 取得ポイントの表示
        #cv2.putText(effect, "%d"%get_point, (SW-200, SH-50), FONT, 2, GREEN, 3)
        cv2.rectangle(effect, (40, 20), (80, SH-20), GREEN, 2)
        h = get_point*3
        if h > 0:
            cv2.rectangle(effect, (40, SH-20-h), (80, SH-20), GREEN, -1)

        # 表示
        cv2.imshow(GAME, effect)
        cv2.waitKey(1)


    ### 終了画面
    # load ranking
    ranking = dill.load(open(RANKING_FILE, 'rb'))
    # ランキング
    # ランキング更新
    a = -1
    for i, rank in enumerate(ranking):
        if get_point > rank[0]:
            a = i
            break
    if a >= 0:
        # 描画用フレーム
        screen = np.ones((SH, SW, 3))*255
        cv2.putText(screen, "Rank in!!", (300, 200), FONT, 5, RED, 5)
        cv2.putText(screen, "Congraturation!!", (300, 400), FONT, 3, RED, 3)
        cv2.putText(screen, "Please tell me your name", (400, 600), FONT, 1, BLACK, 1)

        cv2.imshow(GAME, screen)
        cv2.waitKey(1)

        print("Please tell me your name")
        your_name = input('>> ')
        ranking.insert(a, (get_point, your_name))
        ranking = ranking[:RANKING_NUM]

    # 描画用フレーム
    screen = np.ones((SH, SW, 3))*255

    # 今回の得点
    cv2.putText(screen, "your score", (SW-500, 300), FONT, 2, GREEN, 3)
    cv2.putText(screen, str(get_point), (SW-400, 500), FONT, 4, GREEN, 6)


    # ランキング
    # 表示
    for i, rank in enumerate(ranking):
        cv2.putText(screen, RANK_UINT[i], (130, 120+70*i), FONT, RANK_SIZE[i], RANK_COLOR[i], 2) # rank
        cv2.putText(screen, str(rank[0]), (330, 120+70*i), FONT, RANK_SIZE[i], RANK_COLOR[i], 2) # score
        cv2.putText(screen, str(rank[1]), (530, 120+70*i), FONT, RANK_SIZE[i], RANK_COLOR[i], 2) # name
        if a == i:
            cv2.put

    # 表示
    cv2.imshow(GAME, screen)
    cv2.waitKey(0)

    # ランキング保存
    dill.dump(ranking, open(RANKING_FILE, 'wb'))


# 終了
cv2.destroyAllWindows()
cap.release()
