import streamlit as st
from pytube import YouTube

def download_video(video_url, output_path='.'):
    try:
        # Create a YouTube object
        youtube = YouTube(video_url)

        # Get the highest resolution stream available
        video_stream = youtube.streams.get_highest_resolution()

        # Download the video to the specified output path
        video_stream.download(output_path)

        return True, f"Video downloaded successfully to {output_path}"

    except Exception as e:
        return False, f"An error occurred: {e}"

def main():
    st.title("YouTube Video Downloader")

    # Get YouTube video URL from the user
    video_url = st.text_input("Enter the YouTube video URL:")

    # Get the output path from the user
    output_path = st.text_input("Enter the output path (default is current directory):", '.')

    # Display a download button
    if st.button("Download Video"):
        if video_url:
            # Disable the download button to prevent multiple clicks
            st.button("Downloading...", key="download_button")

            # Download the video
            success, message = download_video(video_url, output_path)

            # Display the result
            if success:
                st.success(message)
            else:
                st.error(message)

    st.info("Note: Downloading YouTube videos may violate YouTube's terms of service. Make sure to comply with their policies.")

if __name__ == "__main__":
    main()
