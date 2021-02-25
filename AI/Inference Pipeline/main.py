import tensorflow as tf
import gpt_2_simple as gpt2

from flask import Flask, request

from flask_ngrok import run_with_ngrok


sess = gpt2.start_tf_sess(threads=1)
gpt2.load_gpt2(sess, run_name="run1")

app = Flask(__name__)


run_with_ngrok(app)  # starts ngrok when the app is run


@app.route("/generate", methods=["GET"])
def generate():
    global sess

    if request.method == "GET":
        input = str(request.args.get("input"))
        result = gpt2.generate(
            sess,
            length=50,
            temperature=0.9,
            prefix=input,
            top_k=200,
            nsamples=1,
            batch_size=1,
            include_prefix=False,
            return_as_list=True,
        )[0]

        print(result)

    return result


app.run()
