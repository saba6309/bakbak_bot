import streamlit as st
from dare_prompts import get_dare_prompt, handle_dare
from truth_prompts import get_truth_prompt, handle_truth
from firebase_utils import save_user_info, save_truth, save_dare, upload_file

st.set_page_config(page_title="Truth & Dare Chatbot", page_icon="🎲", layout="centered")
st.title("Truth & Dare Chatbot 🎲")

st.sidebar.header("User Info")
name = st.sidebar.text_input("Full Name")
nickname = st.sidebar.text_input("Nickname")
age = st.sidebar.text_input("Age")
country = st.sidebar.text_input("Country")
favorite_color = st.sidebar.text_input("Favorite Color")
email = st.sidebar.text_input("Email")

if not (name and age and email):
    st.warning("Fill in your name, age, and email to continue.")
    st.stop()

user_id = f"{name}_{age}_{email}".replace(" ", "_")
user_info = {
    "name": name, "nickname": nickname, "age": age,
    "country": country, "favorite_color": favorite_color,
    "email": email
}
try:
    save_user_info(user_id, user_info)
except Exception as e:
    st.error(f"User info save error: {e}")
    st.stop()

option = st.radio("Choose your challenge:", ["Truth", "Dare"])

if option == "Truth":
    question = get_truth_prompt()
    st.write(f"📝 {question}")
    answer = st.text_area("Type your answer here:")
    if st.button("Submit Truth"):
        truth_entry = handle_truth(question, answer)
        try:
            save_truth(user_id, truth_entry)
            st.success("Truth submitted!")
        except Exception as e:
            st.error(f"Truth save error: {e}")

elif option == "Dare":
    dare = get_dare_prompt()
    st.write(f"🎯 {dare['prompt']}")
    dare_entry = handle_dare(dare)
    if dare_entry:
        # If there is an uploaded file, save to Firebase Storage
        file_url = None
        if "file_obj" in dare_entry:
            file_obj = dare_entry["file_obj"]
            file_name = f"{user_id}_{dare_entry['type']}_{dare_entry.get('caption', '')}.png" if dare_entry["type"] == "meme" else getattr(file_obj, "name", "upload.bin")
            try:
                file_bytes = file_obj.read() if hasattr(file_obj, "read") else file_obj.getvalue()
                file_url = upload_file(file_bytes, file_name)
                dare_entry["file_url"] = file_url
            except Exception as e:
                st.error(f"File upload error: {e}")
        dare_entry.pop("file_obj", None)
        try:
            save_dare(user_id, dare_entry)
            st.success("Dare submitted!")
            if file_url:
                st.markdown(f"[View uploaded file]({file_url})")
        except Exception as e:
            st.error(f"Dare save error: {e}")