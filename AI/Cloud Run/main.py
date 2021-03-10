from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import gpt_2_simple as gpt2
import tensorflow as tf
import os
import uvicorn

RUN_NAME = str(os.environ.get("ENVRUN", "run1"))


tf.reset_default_graph()
sess = gpt2.start_tf_sess(threads=4)
gpt2.load_gpt2(sess, run_name=RUN_NAME)
# generate_count = 0

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.api_route("/", methods=["GET", "POST"])
async def root():
    return "GPT2 based on discord data - GET with query string parameter on /generate for response"


@app.get("/generate", response_class=HTMLResponse)
async def generate(input: str = ""):
    global sess

    result = gpt2.generate(
        sess,
        run_name=RUN_NAME,
        length=250,
        temperature=0.9,
        prefix=input,
        top_p=100,
        nsamples=1,
        batch_size=1,
        include_prefix=False,
        return_as_list=True,
    )[0]

    # if generate_count == 12:
    #     # Prevent OOM
    #     tf.reset_default_graph()
    #     sess.close()
    #     sess = gpt2.start_tf_sess(threads=1)
    #     gpt2.load_gpt2(sess, run_name=RUN_NAME)
    #     generate_count = 0

    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
