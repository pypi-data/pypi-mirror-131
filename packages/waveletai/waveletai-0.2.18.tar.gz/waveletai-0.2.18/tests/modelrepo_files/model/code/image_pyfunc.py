import cv2
from datetime import datetime
import mlflow.pyfunc as pyfunc
import base64
import io
from hyperlpr import LPR
import numpy as np
import os
from PIL import Image


class model_predict(pyfunc.PythonModel):

    def load_context(self, context):
        self.PR = LPR(context.artifacts["models"])

    def predict(self, context, inputs):
        # 入参格式转换
        print(inputs)
        image_data = base64.b64decode(inputs.iloc[0, 0])
        image_temp = Image.open(io.BytesIO(image_data))
        input_image = cv2.cvtColor(np.array(image_temp), cv2.COLOR_BGR2RGB)

        sub = self.PR.plate_recognition(input_image, minSize=30, charSelectionDeskew=True)[0]
        # [['京AG6156', 0.9784000430788312, [92, 110, 151, 129]]]
        print(sub)
        box = f"BOX({sub[2][0]} {sub[2][1]},{sub[2][2]} {sub[2][3]})"
        result = {"title": sub[0], "confidence": sub[1], "type": "rectangle",
               "shape": box, "title_color": "#AE0000",
               "title_bg_color": "rgba(255,0,0,0)"}
        return result


def log_model():
    code_path = ["hyperlpr.py", "image_pyfunc.py", "table_chs.py"]

    artifacts = {
        "models": "./models",
    }

    pyfunc.log_model("model", code_path=code_path, conda_env="conda.yaml", python_model=model_predict(),
                     artifacts=artifacts)


if __name__ == '__main__':
    # 本地注册模型生成的模型路径

    res = log_model()

    # model_path = "." + "/mlruns/0/5b4ea0e20e6f4b9a88570a8be071584c/artifacts/model"
    # test = pyfunc.load_model("mlruns/0/8f024038af1245739cc6a9cbe99853d9/artifacts/model")
    # # test = mlflow.pyfunc.load_model(model_path)
    # # 模型入参
    # img = open('images.jpg', 'rb')
    # input_x = base64.b64encode(img.read())
    # # # 模型预测
    # predictions = test.predict(input_x)
    # # 输出预测结果
    # print("predictions:", predictions)
    #
    # image_data = base64.b64decode(inputs)
    # image_temp = Image.open(io.BytesIO(image_data))
    # from hyperlpr import LPR
    # img = open('images.jpg', 'rb')
    # input_x = base64.b64encode(img.read())
    # image_data = base64.b64decode(input_x)
    # image_temp = Image.open(io.BytesIO(image_data))
    # input_image = cv2.cvtColor(np.array(image_temp), cv2.COLOR_BGR2RGB)
    # # pr = LPR("models")
    # PR = LPR(os.path.join(os.path.split(os.path.realpath(__file__))[0], "models"))
    # # image = cv2.imread("images.jpg")
    # print(PR.plate_recognition(input_image, minSize=30, charSelectionDeskew=True))
