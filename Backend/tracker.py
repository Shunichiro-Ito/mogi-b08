import json
import os
from youtureid.youtureid import YoutuReID

class MultiObjectTracker(object):
    def __init__(
        self,
        tracker_name='motpy',
        fps=30,
        use_gpu=False,
    ):
        self.fps = round(fps, 2)
        self.tracker_name = tracker_name
        self.tracker = None
        self.config = None
        self.use_gpu = use_gpu

        # youtureidを適用する        

        if self.use_gpu:
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
        else:
            providers = ['CPUExecutionProvider']

        with open('./youtureid/config.json') as fp:
            self.config = json.load(fp)

        if self.config is not None:
            self.tracker = YoutuReID(
                fps=self.fps,
                model_path=self.config['model_path'],
                input_shape=[
                    int(i) for i in self.config['input_shape'].split(',')
                ],
                score_th=self.config['score_th'],
                providers=providers,
            )
        
    def __call__(self, image, box, cam_id):
        if self.tracker is not None:
            results = self.tracker(
                image,
                box,
                cam_id,
            )
        else:
            raise ValueError('Tracker is None')

        # 0:Tracker ID, 1:Bounding Box, 2:Score, 3:Class ID
        return results[0], results[1], results[2], results[3], results[4]

    def print_info(self):
        from pprint import pprint

        print('Tracker:', self.tracker_name)
        print('FPS:', self.fps)
        print('GPU:', self.use_gpu)
        pprint(self.config, indent=4)
        print()
