# -*- coding: utf-8 -*-
import os
import copy

import cv2
import numpy as np
import onnxruntime


class YoutuReID(object):
    def __init__(
        self,
        fps=30,
        model_path='person_reid_youtu_2021nov.onnx',
        input_shape=(256, 128),
        score_th=0.25,
        providers=['CPUExecutionProvider'],
    ):
        # 入力サイズ
        self.input_shape = input_shape

        # 閾値
        self.score_th = score_th

        # モデルダウンロード
        if os.path.exists(model_path) is False:
            import gdown
            url = 'https://drive.google.com/uc?id=1U3lEDW9pyliNMd8TFBrsCYoqbsJj62N6'
            gdown.download(url, model_path, quiet=False)

        # モデル読み込み
        self.onnx_session = onnxruntime.InferenceSession(
            model_path,
            providers=providers,
        )

        self.input_name = self.onnx_session.get_inputs()[0].name
        self.output_shape = self.onnx_session.get_outputs()[0].shape

        # 特徴ベクトルリスト
        self.feature_vectors = None
        self.cam_ids = []
        # カメラをまたいだ同一人物の情報を保持
        # これは例外にして、すでにある方のidを採用したいという考えから
        self.except_ids = []

    def __call__(self, image, box, cam_id):
        image_height, image_width = image.shape[0], image.shape[1]

        # 人物切り抜き
        # xmin = int(np.clip(box[0], 0, image_width - 1))
        # ymin = int(np.clip(box[1], 0, image_height - 1))
        # xmax = int(np.clip(box[2], 0, image_width - 1))
        # ymax = int(np.clip(box[3], 0, image_height - 1))
        xmin, ymin, xmax, ymax = map(int, box)
        person_image = copy.deepcopy(image[ymin:ymax, xmin:xmax])

        # 前処理
        input_image = cv2.resize(
            person_image,
            dsize=(self.input_shape[1], self.input_shape[0]),
        )
        input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]
        input_image = (input_image / 255 - mean) / std
        input_image = input_image.transpose(2, 0, 1)
        input_image = input_image.astype('float32')
        input_image = np.expand_dims(input_image, axis=0)

        # 推論実施
        result = self.onnx_session.run(
            None,
            {self.input_name: input_image},
        )
        result = np.array(result[0][0])
        result = result.T[0][0]
        added = False
        # 初回推論時のデータ登録
        if self.feature_vectors is None:
            self.feature_vectors = copy.deepcopy(np.array([result]))
            self.cam_ids.append(cam_id)
            added = True

        # COS類似度計算
        cos_results = self._cos_similarity(result, self.feature_vectors)
        max_index = np.argmax(cos_results)
        max_value = cos_results[max_index]
        track_id = self.cam_ids[max_index]

        if max_value < self.score_th:
            # スコア閾値以下であれば特徴ベクトルリストに追加
            print(f'***********未発見************** {max_value} < {self.score_th} ***********************')
            if cam_id not in self.cam_ids and cam_id not in self.except_ids:
                self.feature_vectors = np.vstack([
                    self.feature_vectors,
                    result,
                ])
                self.cam_ids.append(cam_id)
                added = True

            return False, cam_id, [], 0, added
        else:
            # スコア閾値以上であればトラッキング情報を返す
            # ここでカメラidが違うときにカメラ間id紐づけ
            print(f'*********発見**************** {max_value} > {self.score_th} ***********************')
            if track_id.split('-')[0] != cam_id.split('-')[0]:
                self.except_ids.append(cam_id)
            
            return True, track_id, [xmin, ymin, xmax, ymax], max_value, added
            
    def _cos_similarity(self, X, Y):
        Y = Y.T

        # (768,) x (n, 768) = (n,)
        result = np.dot(X, Y) / (np.linalg.norm(X) * np.linalg.norm(Y, axis=0))

        return result
