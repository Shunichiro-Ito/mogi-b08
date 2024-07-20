import cv2

# ストリーミング映像のURL
stream_url = 'http://blue-network.eolstudy.com/cam-window'  # ここに実際のストリーミングURLを入力してください

# ビデオキャプチャオブジェクトの作成
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()

while True:
    # フレームを読み込む
    ret, frame = cap.read()

    # フレームが正常に読み込めなかった場合はループを終了
    if not ret:
        print("Error: Could not read frame")
        break

    # フレームのサイズを取得
    height, width, _ = frame.shape

    # テキストの設定
    text = "ストリーミング中"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (255, 255, 255)  # 白
    thickness = 2
    line_type = cv2.LINE_AA

    # テキストサイズの取得
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    # テキストの位置の計算
    x = (width - text_width) // 2
    y = (height + text_height) // 2

    # フレームにテキストを追加
    cv2.putText(frame, text, (x, y), font, font_scale, font_color, thickness, line_type)

    # フレームを表示
    cv2.imshow('Frame', frame)

    # 'q'キーを押したらループを終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソースを解放
cap.release()
cv2.destroyAllWindows()