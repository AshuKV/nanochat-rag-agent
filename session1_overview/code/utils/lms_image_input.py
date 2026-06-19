import os
import lmstudio as lms

model = lms.llm()


def image_chat(image_path, prompt):
    chat = lms.Chat()
    image_handle = lms.prepare_image(image_path)
    chat.add_user_message(prompt, images=[image_handle])
    prediction = model.respond(chat)
    return prediction.content


if __name__ == '__main__':
    DATAPATH = r"/Users/ashutoshkumv/Documents/gAi/session1Images"
    name = "Diff"
    text = "Explain the content of the image"
    # schema = {
    #     "table": bool,
    #     "json": dict
    # }
    fname = os.path.join(DATAPATH, name + ".png")
    print(fname)
    preds = image_chat(fname, text)
    print(preds)
    