from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import gpt_2_simple as gpt2
import tensorflow as tf
import psutil
import codecs
import os
import uvicorn
from config import AUTH_KEY

f = codecs.open("pid", "w+", "utf-8")
f.truncate(0)
f.close()
f = codecs.open("pid", "w", "utf-8")
f.write(str(os.getpid()))
f.close()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tf.reset_default_graph()
sess = gpt2.start_tf_sess(threads=8)
gpt2.load_gpt2(sess, run_name="run1")
generate_count = 0


@app.api_route("/", methods=["GET", "POST"])
async def root():
    return "GPT2 based on discord data - GET with query string parameter on /generate for response"


@app.get("/generate", response_class=HTMLResponse)
async def generate(input: str = "", auth: str = ""):
    global sess, generate_count

    if auth != AUTH_KEY:
        return "Invalid auth token provided"

    result = gpt2.generate(
        sess,
        run_name="run1",
        length=300,
        temperature=0.9,
        prefix=input,
        top_p=100,
        nsamples=1,
        batch_size=1,
        include_prefix=False,
        return_as_list=True,
    )[0]

    generate_count += 1

    if generate_count == 12:
        # Reload model to prevent Graph/Session from going OOM
        tf.reset_default_graph()
        sess.close()
        sess = gpt2.start_tf_sess(threads=8)
        gpt2.load_gpt2(sess, run_name="run1")
        generate_count = 0

    return result


uvicorn.run(app, port=8000)
