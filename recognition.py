# -*- coding: utf-8 -*-
import cv2
from ultralytics import YOLO

# YOLOv8の軽量モデルをロード
model = YOLO('yolov8n.pt')

# ビデオキャプチャの設定（0はデフォルトカメラ）
#cap = cv2.VideoCapture('.\YOLO\傘3.mp4')
cap = cv2.VideoCapture(0)

frame_skip = 2  # フレームをスキップする間隔
frame_count = 0

while cap.isOpened():
   ret, frame = cap.read()
   if not ret:
      break

   frame_count += 1
   if frame_count % frame_skip != 0:
      continue

   # YOLOv8で推論を実行
   results = model(frame)
   
   bike_S=[]
   umb_S=[]
   # 検出結果をフレームに描画
   for box in results[0].boxes:
      
      class_id = int(box.cls[0])
      if(results[0].names[class_id]=="bicycle"):
         x1, y1, x2, y2 = map(int, box.xyxy[0])
         bike_S.append([x1,y1,x2,y2])
         cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
         cv2.putText(frame, "bike", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
      elif(results[0].names[class_id]=="umbrella"):
         x1, y1, x2, y2 = map(int, box.xyxy[0])
         umb_S.append([x1,y1,x2,y2])
         cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
         cv2.putText(frame, "umb", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

      """
      if(results[0].names[class_id]=="bicycle" or results[0].names[class_id]=="umbrella"):
         x1, y1, x2, y2 = map(int, box.xyxy[0])
         class_id = int(box.cls[0])
         label = f'{results[0].names[class_id]} {box.conf[0]:.2f}'
         #print(results[0].names[class_id])
         cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
         cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
      """
   print("umb_S")
   print(umb_S)
   print("bike_S")
   print(bike_S)
   hozon=False
   for i in umb_S:
      for j in bike_S:
         if(i[0]<j[2] and j[0]<i[2] and 3*min(j[2]-i[0],i[2]-j[0])>i[2]-i[0]):
            print(box)
            x1, y1, x2, y2 = map(int,i)
            X1, Y1, X2, Y2 = map(int,j)
            cv2.rectangle(frame, (min(x1,X1), min(y1,Y1)), (max(x2,X2), max(y2,Y2)), (0, 0, 255), 2)
            cv2.putText(frame, "bike", (min(x1,X1), min(y1,Y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            hozon=True

    # フレームを表示
   cv2.imshow('YOLOv8 Real-Time Detection', frame)

   if(hozon):
      # フレームを保存
      output_path = f'output/frame_{frame_count}.jpg'  # 保存するパスとファイル名
      cv2.imwrite(output_path, frame)

    # 'q' キーで終了
   if cv2.waitKey(1) & 0xFF == ord('q'):
        break