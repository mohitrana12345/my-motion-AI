import streamlit as st
import fal_client
import requests
import os

st.set_page_config(
    page_title="My Motion AI",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 My Motion AI")
st.subheader("Create AI Videos with Motion Control")

api_key = st.text_input(
    "Enter your fal.ai API Key",
    type="password"
)

st.info("Upload one photo and one reference video.")

image = st.file_uploader(
    "📸 Upload Your Photo",
    type=["png", "jpg", "jpeg"]
)

video = st.file_uploader(
    "🎥 Upload Reference Video",
    type=["mp4", "mov"]
)

prompt = st.text_area(
    "Describe your video (optional)",
    placeholder="A woman dancing naturally..."
)

orientation = st.selectbox(
    "Character Orientation",
    ["video", "image"]
)

keep_sound = st.checkbox(
    "Keep original video sound",
    value=True
)

if st.button("🎬 Generate Motion Video", type="primary"):

    if not api_key:
        st.error("Please enter your fal.ai API key.")

    elif not image or not video:
        st.warning("Please upload both photo and video.")

    else:
        try:
            os.environ["FAL_KEY"] = api_key

            with st.spinner("Uploading files..."):
                image_url = fal_client.upload(
                    image.getvalue(),
                    image.type,
                    image.name
                )

                video_url = fal_client.upload(
                    video.getvalue(),
                    video.type,
                    video.name
                )

            arguments = {
                "image_url": image_url,
                "video_url": video_url,
                "character_orientation": orientation,
                "keep_original_sound": keep_sound
            }

            if prompt.strip():
                arguments["prompt"] = prompt.strip()

            with st.spinner("AI is generating your video..."):
                result = fal_client.subscribe(
                    "fal-ai/kling-video/v3/standard/motion-control",
                    arguments=arguments
                )

            video_result = result["video"]["url"]

            st.success("Your AI video is ready!")

            st.video(video_result)

            response = requests.get(
                video_result,
                timeout=120
            )
            response.raise_for_status()

            st.download_button(
                "⬇️ Download Video",
                data=response.content,
                file_name="my_motion_video.mp4",
                mime="video/mp4"
            )

        except Exception as e:
            st.error(f"Error: {e}")