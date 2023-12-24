from moviepy.editor import VideoFileClip
import os
import tkinter as tk
from tkinter import filedialog, Entry, Button, Label, VERTICAL, END

class VideoSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Splitter")

        # Widgets for selecting the unsplit videos directory
        self.label = Label(root, text="Unsplit Videos Directory:")
        self.label.grid(row=0, column=0, sticky="w")
        self.unsplit_videos_entry = Entry(root)
        self.unsplit_videos_entry.grid(row=0, column=1)
        self.browse_button = Button(root, text="Browse", command=self.browse_unsplit_videos_directory)
        self.browse_button.grid(row=0, column=2)

        # Button to initiate video splitting
        self.split_videos_button = Button(root, text="Split Videos", command=self.split_videos)
        self.split_videos_button.grid(row=1, column=0, columnspan=3)

        # Log Text Area
        self.log_label = Label(root, text="Progress Log:")
        self.log_label.grid(row=2, column=0, sticky="w")

        self.log_text = tk.Text(root, height=5, width=50)
        self.log_text.grid(row=3, column=0, columnspan=3)

    def browse_unsplit_videos_directory(self):
        self.unsplit_videos_directory = filedialog.askdirectory()
        self.unsplit_videos_entry.delete(0, 'end')
        self.unsplit_videos_entry.insert(0, self.unsplit_videos_directory)

    def log_message(self, message):
        self.log_text.insert(END, message + "\n")
        self.log_text.yview(END)

    def split_videos(self):
        input_videos_folder = self.unsplit_videos_entry.get()
        if not input_videos_folder:
            self.log_message("Please select the unsplit videos directory.")
            return

        files = [file_name for file_name in os.listdir(input_videos_folder) if file_name.endswith(".mp4")]

        for file_name in files:
            self.process_video(file_name)

    def process_video(self, file_name):
        input_video_path = os.path.join(self.unsplit_videos_entry.get(), file_name)

        clip = VideoFileClip(input_video_path)
        current_duration = clip.duration
        divide_into_count = 2  # You can adjust this value as needed
        single_duration = current_duration / divide_into_count

        while current_duration > single_duration:
            # Split the video into two equal halves
            subclip = clip.subclip(current_duration - single_duration, current_duration)

            # Save each subclip with the original filename and appropriate suffix
            file_base_name, file_extension = os.path.splitext(file_name)
            first_half_filename = os.path.join(self.unsplit_videos_entry.get(), f"{file_base_name}_part1{file_extension}")
            second_half_filename = os.path.join(self.unsplit_videos_entry.get(), f"{file_base_name}_part2{file_extension}")

            subclip.to_videofile(first_half_filename, codec="libx264", audio_codec="aac")
            subclip.close()  # Close the subclip before creating the second one

            # Create the second subclip
            subclip = clip.subclip(current_duration - 2 * single_duration, current_duration - single_duration)
            subclip.to_videofile(second_half_filename, codec="libx264", audio_codec="aac")

            # Close the second subclip
            subclip.close()

            # Update current_duration for the next iteration
            current_duration -= single_duration

            self.log_message(f"Video split and saved: {first_half_filename} and {second_half_filename}")

        # Remove the original video
        os.remove(input_video_path)

# Create and run the Tkinter application
root = tk.Tk()
app = VideoSplitterGUI(root)
root.mainloop()
