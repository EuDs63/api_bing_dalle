from fastapi import FastAPI
import os
import random
from BingImageCreator import ImageGen
from fastapi.responses import FileResponse

app = FastAPI()


async def generate_dalle_image(path, bing_cookie, prompt):
    i = ImageGen(bing_cookie)
    try:
        images = i.get_images(prompt)
        i.save_images(images, path)
        return True
    except Exception as e:
        print("encounter error {} when generate bing photo".format(e))
        return False


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/image/{bing_cookie}/{prompt}")
async def say_hello(bing_cookie: str, prompt: str):
    path = "dalle_images"
    if not os.path.exists(path):
        os.mkdir(path)

    path = os.path.join(path, str(prompt))
    if not os.path.exists(path):
        os.mkdir(path)

    # 先判断是否已有图片
    images_count = len(list(os.listdir(path)))

    if images_count == 0:
        # 若无，则生成
        result = await generate_dalle_image(path, bing_cookie, prompt)
        if not result:
            return {"message": "fail"}
    else:
        pass
    # 生成成功，随机选择一个图像发送
    images_count = len(list(os.listdir(path)))
    index = random.randint(0, images_count - 1)
    image_path = os.path.join(path, str(index)) + ".jpeg"

    # 使用FileResponse发送图像
    return FileResponse(image_path, media_type="image/jpeg")
