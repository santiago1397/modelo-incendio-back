import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from flask import Flask, request, jsonify, make_response, request, render_template, session, flash
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv, find_dotenv

load_dotenv()

model = load_model("my_fire_detection_model.keras")

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "https://app-incendio.netlify.app", "methods": ["OPTIONS", "POST"], "allow_headers": ["Content-Type"]}}, supports_credentials=True)
application = app


@app.route("/firecheck", methods=['POST','OPTIONS'])
def fireCheck():
    try:
        if request.method == 'OPTIONS':
            # Respond to preflight requests
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "https://app-incendio.netlify.app")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type")
            response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
            return response


        data = request.json['data']
        numpy_array = np.array(data)
        numpy_array = numpy_array.reshape((1, 320, 320, 3))

        response = jsonify({
            "hello": "hiii"
        })
        response.status_code = 202
        return response


        predictions = model.predict(numpy_array)

        
        if predictions[0][0] > 0.5:
            prediction = "Predicción: Hay Fuego! 🔥"
        else:
            prediction = "Predicción: No hay fuego 🌳"


        print(prediction)

        response = jsonify({
            "hello": prediction
        })
        response.status_code = 202
        return response
    except:
        print("An error occurred.")



if __name__ == '__main__':
    app.run()