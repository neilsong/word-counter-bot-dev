# bot-word-counter
Python Discord Bot for counting words

**A Discord bot that analyzes the word choice of users on the server**

A bot that will analyze syntax/word choice of everyone in this server

  1. Provide insight and analytics into the unique language of this server
        - Leaderboard of most common words in the server
        - Your own personal leaderboard of most common words

  2. (Possibly) Create an AI model that will mimic your style to send a message you would probably send on command

  3. (Very far off/might not even happen) Create a web app that serves a dashboard with insights, charts, and analytics 



Updating
Unhandled exception in internal background task 'update_db'.
Traceback (most recent call last):
  File "C:\Users\Antho\AppData\Local\Programs\Python\Python38-32\lib\site-packages\discord\ext\tasks\__init__.py", line 101, in _loop
    await self.coro(*args, **kwargs)
  File "c:\Users\Antho\vsProjects\bot-word-counter\main.py", line 153, in update_db
    await bot.collection.update_one({"__id": data}, {'$set': bot.words[data]}, True)
  File "C:\Users\Antho\AppData\Local\Programs\Python\Python38-32\lib\concurrent\futures\thread.py", line 57, in run
    result = self.fn(*self.args, **self.kwargs)
  File "C:\Users\Antho\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\collection.py", line 1019, in update_one
    self._update_retryable(
  File "C:\Users\Antho\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\collection.py", line 868, in _update_retryable
    return self.__database.client._retryable_write(
  File "C:\Users\Antho\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\mongo_client.py", line 1498, in _retryable_write
    return self._retry_with_session(retryable, func, s, None)
  File "C:\Users\Antho\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\mongo_client.py", line 1384, in _retry_with_session
    return self._retry_internal(retryable, func, session, bulk)
  File "C:\Users\Antho\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\mongo_client.py", line 1416, in _retry_internal
    return func(session, sock_info, retryable)
  File "C:\Users\Antho\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\collection.py", line 860, in _update
    return self._update(
  File "C:\Users\Antho\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\collection.py", line 837, in _update
    _check_write_command_response(result)
  File "C:\Users\Antho\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\helpers.py", line 222, in _check_write_command_response
    _raise_last_write_error(write_errors)
  File "C:\Users\Antho\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\helpers.py", line 204, in _raise_last_write_error
    raise WriteError(error.get("errmsg"), error.get("code"), error)
pymongo.errors.WriteError: The dollar ($) prefixed field '$daily' in '$daily' is not valid for storage., full error: {'index': 0, 'code': 52, 'errmsg': "The dollar ($) prefixed field '$daily' in '$daily' is not valid for storage."}
