# -*- coding: utf-8 -*-
# @Author   = Apexopco
# @Time     = 2021/12/3 19:00

from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from werkzeug.utils import secure_filename
import os
import cv2

from datetime import timedelta
from inference_realesrgan_new import funtion_main
# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/image_enhance', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
        user_input = request.form.get("name")
        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        save_path = os.path.join(basepath, 'static/enhance_images', secure_filename(f.filename))
        f.save(upload_path)

        img1=cv2.imread(upload_path, cv2.IMREAD_UNCHANGED)
        image = funtion_main(img1)
        cv2.imwrite(save_path, image)
        image_data = open(save_path, "rb").read()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response
    return render_template('upload.html')

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=12907, debug=True)
