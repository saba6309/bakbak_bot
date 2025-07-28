import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
from typing import Optional, Dict, Any

DARES = [
    {"prompt": "Record yourself saying a tongue twister!", "type": "audio"},
    {"prompt": "Upload a photo of your favorite food!", "type": "image"},
    {"prompt": "Write a caption in your local slang!", "type": "text"},
    {"prompt": "Create a meme using one of your photos!", "type": "meme"},
]

def get_dare_prompt() -> Dict[str, str]:
    import random
    return random.choice(DARES)

def create_meme(image_file, caption: str) -> Optional[io.BytesIO]:
    try:
        image = Image.open(image_file).convert("RGB")
        draw = ImageDraw.Draw(image)
        # Try to use a truetype font, fallback to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", size=40)
        except Exception:
            font = ImageFont.load_default()
        w, h = image.size
        # Calculate text size
        text_w, text_h = draw.textsize(caption, font=font)
        x = max(10, (w - text_w) // 2)
        y = h - text_h - 20
        # Draw text with outline for visibility
        draw.text((x, y), caption, font=font, fill="white", stroke_width=2, stroke_fill="black")
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        return buf
    except Exception as e:
        st.error(f"Meme creation error: {e}")
        return None

def handle_dare(dare: Dict[str, str]) -> Optional[Dict[str, Any]]:
    entry = {"prompt": dare["prompt"], "type": dare["type"]}
    submitted = False

    if dare["type"] == "audio":
        st.info("Record and upload your audio file (mp3, wav, m4a)")
        audio_file = st.file_uploader("Upload audio:", type=["mp3", "wav", "m4a"])
        if audio_file:
            st.audio(audio_file)
            entry["file_obj"] = audio_file
            entry["file_type"] = "audio"
            submitted = st.button("Submit Dare")
    elif dare["type"] == "image":
        image_file = st.file_uploader("Upload image:", type=["png", "jpg", "jpeg"])
        if image_file:
            st.image(image_file)
            entry["file_obj"] = image_file
            entry["file_type"] = "image"
            submitted = st.button("Submit Dare")
    elif dare["type"] == "text":
        caption = st.text_input("Enter your slang caption:")
        if st.button("Submit Caption"):
            if caption:
                entry["caption"] = caption
                submitted = True
            else:
                st.error("Please enter a caption.")
    elif dare["type"] == "meme":
        meme_img = st.file_uploader("Upload image for meme:", type=["png", "jpg", "jpeg"])
        meme_caption = st.text_input("Meme caption:")
        create_meme_button = st.button("Create Meme")
        if create_meme_button:
            if meme_img and meme_caption:
                meme_buf = create_meme(meme_img, meme_caption)
                if meme_buf:
                    st.image(meme_buf)
                    entry["file_obj"] = meme_buf
                    entry["file_type"] = "meme"
                    entry["caption"] = meme_caption
                    submitted = st.button("Submit Meme")
                else:
                    st.error("Meme creation failed.")
            else:
                st.error("Upload image and enter meme caption.")
    return entry if submitted else None