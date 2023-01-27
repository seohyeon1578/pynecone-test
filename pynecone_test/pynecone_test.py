"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config

import pynecone as pc
import openai

openai.api_key = "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"

class State(pc.State):
    """The app state."""

    prompt: str = ""
    image_url: str = ""
    image_processing: bool = False
    image_made: bool = False

    def process_image(self):
        """ 이미지 처리중. """
        self.image_processing = True
        self.image_made = False
    def get_image(self):
        """ 이미지 만들기 """
        try:
            response = openai.Image.create(prompt=self.prompt, n=1, size="1024x1024")
            self.image_url = response["data"][0]["url"]
            self.image_processing = False
            self.image_made = True
        except:
            self.image_processing = False
            return pc.window_alert("Error")

def index():
    return pc.center(
        pc.vstack(
            pc.heading("DALL-E TEST", font_size="1.5em"),
            pc.input(on_blur=State.set_prompt),
            pc.button(
                "make Image",
                on_click=[State.process_image, State.get_image],
                width="100%",
            ),
            pc.divider(),
            pc.cond(
                State.image_processing,
                pc.circular_progress(is_indeterminate=True),
                pc.cond(
                    State.image_made,
                    pc.image(
                        src=State.image_url,
                        width="25em",
                        height="25em",
                    ),
                ),
            ),
            bg="white",
            padding="2em",
            shadow="lg",
            border_radius="lg",
        ),
        width="100vw",
        height="100vh",
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
