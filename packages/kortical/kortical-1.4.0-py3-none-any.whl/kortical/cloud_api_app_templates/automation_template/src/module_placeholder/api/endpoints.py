from flask import Response, request
import pandas as pd
from io import StringIO
import logging
# uwsgi is only loaded when run in uwsgi
try:
    from uwsgidecorators import thread
except:
    def thread(func):
        return func

from module_placeholder.authentication import safe_api_call
from module_placeholder.workflows import train, predict, common

logger = logging.getLogger(__name__)


# runs asynchronously
@thread
def train_workflow(df):
    df_train, df_calibrate, df_test = common.create_train_calibrate_and_test_datasets(df)
    train.train(df_train, df_calibrate, df_test)


def register_routes(app):

    @app.route('/train', methods=['post'])
    @safe_api_call
    def post_train():
        # Get dataframe from request
        file = request.files['file']
        df = pd.read_csv(file)

        # create background process
        # kick off train workflow
        train_workflow(df)

        return Response("Success!")

    @app.route('/predict.csv', methods=['post'])
    @safe_api_call
    def post_predict():
        # Get dataframe from request
        file = request.files['file']
        df = pd.read_csv(file)

        # kick off predict workflow
        df = predict.predict(df)
        s = StringIO()
        df.to_csv(s, index=False)

        logger.debug('Predict done')
        return Response(s.getvalue(), mimetype="text/csv")