import cv2
import requests
import numpy as np

def split_frame(frame):
    """
    フレームを中央で分割して二つのフレームにする関数
    """
    height, width, _ = frame.shape
    mid_x = width // 2

    frame_left = frame[:, :mid_x]
    frame_right = frame[:, mid_x:]

    return frame_left, frame_right


def stream_video(url):
    # ストリーミングのリクエストを送信
    response = requests.get(url, stream=True)

    if response.status_code != 200:
        print("Failed to connect to the stream")
        return

    # フレームのバッファを初期化
    bytes = b''
    for chunk in response.iter_content(chunk_size=1024):
        bytes += chunk
        a = bytes.find(b'\xff\xd8')  # JPEGの開始マーカー
        b = bytes.find(b'\xff\xd9')  # JPEGの終了マーカー

        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]

            # JPEGデータをデコードしてフレームを表示
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            if frame is not None:

                frame_left, frame_right = split_frame(frame)

                # 分割したフレームを表示
                cv2.imshow('Left Frame', frame_left)
                cv2.imshow('Right Frame', frame_right)

                # 'q' キーを押したらストリーミングを終了
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream_url = "http://localhost:8000/video_feed"  # ストリーミングのURL
    stream_video(stream_url)
