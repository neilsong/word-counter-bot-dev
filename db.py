import motor.motor_asyncio
import asyncio
import random

queue = asyncio.Queue()
workers = []


async def create_db():
    from main import bot
    import config

    # Create db in MongoDB if it doesn't already exist.
    print("\nCreating or Fetching DB")
    bot.collection = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO)["users-db"][
        "users"
    ]
    bot.userWords = {}
    bot.userLastMsg = {}

    async for i in bot.collection.find({}, {"_id": 0}):
        bot.userWords.update({i.get("__id"): dict(i)})

    bot.serverCollection = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO)[
        "servers-db"
    ]["servers"]
    bot.serverWords = {}
    bot.prefixes = {"__id": "prefixes"}
    bot.blacklist = {"__id": "blacklist"}
    bot.filter = {"__id": "filter"}
    async for i in bot.serverCollection.find({}, {"_id": 0}):
        if i.get("__id") == "prefixes":
            bot.prefixes.update(dict(i))
            continue
        if i.get("__id") == "blacklist":
            bot.blacklist.update(dict(i))
            continue
        if i.get("__id") == "filter":
            bot.filter.update(dict(i))
            continue
        bot.serverWords.update({i.get("__id"): dict(i)})
    print(
        "\nNumber of Users: "
        + str(len(bot.userWords))
        + "\nNumber of Servers: "
        + str(len(bot.serverWords) - 1)
    )


async def worker(queue):
    from main import bot

    while True:
        task = await queue.get()
        print("Working on task: ", task)
        state = task[0]
        if state == 0:
            await bot.serverCollection.update_one(
                {"__id": "prefixes"},
                {"$set": {task[1]["id"]: bot.prefixes[task[1]["id"]]}},
                True,
            )
        elif state == 1:
            await bot.serverCollection.update_one(
                {"__id": "blacklist"},
                {"$set": {task[1]["id"]: bot.blacklist[task[1]["id"]]}},
                True,
            )
        elif state == 2:
            await bot.serverCollection.update_one(
                {"__id": "filter"},
                {"$set": {task[1]["id"]: bot.filter[task[1]["id"]]}},
                True,
            )
        elif state == 3:
            await bot.collection.update_one(
                {"__id": task[1]["id"]},
                {
                    "$set": {
                        task[1]["word"]: bot.userWords[task[1]["id"]][task[1]["word"]]
                    }
                },
                True,
            )
        elif state == 4:
            await bot.serverCollection.update_one(
                {"__id": task[1]["id"]},
                {
                    "$set": {
                        task[1]["word"]: bot.serverWords[task[1]["id"]][task[1]["word"]]
                    }
                },
                True,
            )
        queue.task_done()
        print("Task finished")


async def start_workers():
    global queue, workers
    print("\nCreating Queue Workers")

    # start the workers
    workers = [asyncio.create_task(worker(queue)) for _ in range(10)]
    print("\nCreated Queue Workers\n")


async def cancel_workers():
    print("Waiting for workers to complete remaining tasks...")
    await queue.join()

    # Kill the workers, which are now idle
    print("Killing workers...")
    for w in workers:
        w.cancel()
    print("Workers killed.")
