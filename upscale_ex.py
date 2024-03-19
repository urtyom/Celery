import uuid
import os
import cv2
from cv2 import dnn_superres
from flask import Flask
from flask import request
from flask.views import MethodView
from flask import jsonify
from celery import Celery
from celery.result import AsyncResult
from flask import send_file


app_name = 'app'
app = Flask(app_name)
app.config['UPLOAD_FOLDER'] = 'upload'
celery = Celery(
    app_name,
    backend='redis://localhost:6379/3',
    broker='redis://localhost:6379/4',
    broker_connection_retry_on_startup=True
)
celery.conf.update(app.config)

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask


@celery.task
def upscale(input_path: str, output_path: str, model_path: str = 'EDSR_x2.pb') -> None:

    scaler = dnn_superres.DnnSuperResImpl_create()
    scaler.readModel(model_path)
    scaler.setModel("edsr", 2)
    image = cv2.imread(input_path)
    result = scaler.upsample(image)
    cv2.imwrite(output_path, result)


class Upscale_photo(MethodView):

    def get(self, task_id):
        task = AsyncResult(task_id, app=celery)
        return jsonify({'status': task.status,
                        'result': task.result})

    def post(self):
        input_path = request.args.get('input_path')
        output_path = request.args.get('output_path')
        task = upscale.delay(
            input_path=input_path,
            output_path=output_path,
            model_path='EDSR_x2.pb'
        )
        return jsonify(
            {'task_id': task.id}
        )

    def get_file(self):
        file = request.args.get('file')
        processed_file_path = "path/to/processed/files/" + file
        return send_file(processed_file_path, as_attachment=True)


upscale_view = Upscale_photo.as_view('upscale')
app.add_url_rule('/upscale/<string:task_id>', view_func=upscale_view, methods=['GET'])
app.add_url_rule('/upscale/', view_func=upscale_view, methods=['POST'])
app.add_url_rule('/upscale/processed/<path:file>', view_func=upscale_view, methods=['GET'])


if __name__ == '__main__':
    app.run()
