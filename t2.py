import streamlit as st
from pytube import YouTube
from tqdm import tqdm
from stqdm import stqdm
from time import sleep
import time
import youtube_dl
import os

def download_video(video_url, output_path='.'):
    try:
        # Create a YouTube object
        youtube = YouTube(video_url)

        # Get the highest resolution stream available
        video_stream = youtube.streams.get_highest_resolution()

        total_size = video_stream.filesize

        # Define the progress bar
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading')
        for i in range(1,total_size):
            progress_bar.update()

        # Download the video to the specified output path
        video_stream.download(output_path)
        with st.spinner('Wait for it...'):
            time.sleep(1)
        return True, f"Video downloaded successfully to {output_path}"

    except Exception as e:
        return False, f"An error occurred: {e}"

def download_playlist(vid_list, output_path_playlist):
    if not os.path.exists(output_path_playlist):
        os.makedirs(output_path_playlist)
    for video_link in stqdm(vid_list, desc='Downloading Playlist'):
        success, message = download_video(video_link, output_path_playlist)
        if not success:
            st.error(message)
            break
    st.success(f"Playlist downloaded successfully to {output_path_playlist}")

def get_playlist_video_links(playlist_url):
    ydl_opts = {
        'quiet': True,  # Suppress console output
        'extract_flat': True,  # Extract only the video URLs
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
        video_links = []

        if 'entries' in result:
            for entry in result['entries']:
                video_links.append(entry['url'])

        return video_links

def main():
    st.title("YouTube Video Downloader")

    # Choose between Single Video and Playlist
    download_option = st.radio("Select Download Option", ('Single Video', 'Playlist'))

    if download_option == 'Single Video':
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

    elif download_option == 'Playlist':
        # Get YouTube playlist URL from the user
        playlist_url = st.text_input("Enter the YouTube playlist URL:")

        # Get the output path from the user
        output_path_playlist = st.text_input("Enter the output path for the playlist (default is current directory):", '.')

        # Display a download button for the playlist
        if st.button("Download Playlist"):
            video_links = get_playlist_video_links(playlist_url)
            vid_list = []

            # Display the list of video links
            if video_links:
                st.markdown("List of video links in the playlist:")
                for link in video_links:
                    vid_list.append("https://www.youtube.com/watch?v=" + link)
                    #st.write("https://www.youtube.com/watch?v=" + link)
            else:
                st.error("Unable to fetch video links. Please check the playlist URL.")

            # Download the playlist directly
            download_playlist(vid_list, output_path_playlist)



    st.info("Note: Downloading YouTube videos may violate YouTube's terms of service. Make sure to comply with their policies.")

if __name__ == "__main__":
    main()
