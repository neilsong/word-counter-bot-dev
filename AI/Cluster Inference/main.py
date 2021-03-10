from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import gpt_2_simple as gpt2
import tensorflow as tf
from config import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tf.reset_default_graph()
sess = gpt2.start_tf_sess(threads=1)
gpt2.load_gpt2(sess, run_name="run1")
generate_count = 0


@app.api_route("/", methods=["GET", "POST"])
async def root():
    return "GPT2 based on discord data - GET with query string parameter on /generate for response"


@app.get("/generate", response_class=HTMLResponse)
async def generate(input: str = ""):
    global sess, generate_count

    result = gpt2.generate(
        sess,
        run_name="run1",
        length=420,
        temperature=0.9,
        prefix=input,
        top_p=100,
        nsamples=1,
        batch_size=1,
        include_prefix=False,
        return_as_list=True,
    )[0]

    generate_count += 1

    if generate_count == 8:
        # Reload model to prevent Graph/Session from going OOM
        tf.reset_default_graph()
        sess.close()
        sess = gpt2.start_tf_sess(threads=1)
        gpt2.load_gpt2(sess, run_name="run1")
        generate_count = 0

    return result


import nest_asyncio
from pyngrok import ngrok
import uvicorn

ngrok.set_auth_token(NGROK_AUTH_TOKEN)
ngrok_tunnel = ngrok.connect(8000)
print("Public URL:", ngrok_tunnel.public_url)
nest_asyncio.apply()
uvicorn.run(app, port=8000)
