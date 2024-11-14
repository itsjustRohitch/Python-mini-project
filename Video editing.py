import tkinter as tk
from tkinter import filedialog, messagebox, Menu
from tkinter import ttk  # Import ttk for the Notebook (tabbed interface)
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

# Initialize the main window
root = tk.Tk()
root.title("Basic Video Editor")
root.geometry("1920x1080")

# Global variables to hold the video clip and other settings
video = None
videos_to_merge = []

# Create the Notebook widget (for tabs)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Function to load a video file
def load_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
    if file_path:
        global video
        video = VideoFileClip(file_path)
        messagebox.showinfo("Loaded", "Video loaded successfully!")
    else:
        messagebox.showwarning("Warning", "No video file selected.")

# Trim Video Tab
trim_tab = ttk.Frame(notebook)
notebook.add(trim_tab, text="Trim Video")

def trim_video():
    if video is None:
        messagebox.showwarning("Warning", "Please load a video first.")
        return
    start_time = float(start_time_entry.get())
    end_time = float(end_time_entry.get())
    trimmed_clip = video.subclip(start_time, end_time)
    save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if save_path:
        trimmed_clip.write_videofile(save_path)
        messagebox.showinfo("Saved", "Trimmed video saved successfully!")

tk.Label(trim_tab, text="Start Time (s):").pack()
start_time_entry = tk.Entry(trim_tab)
start_time_entry.pack()

tk.Label(trim_tab, text="End Time (s):").pack()
end_time_entry = tk.Entry(trim_tab)
end_time_entry.pack()
trim_button = tk.Button(trim_tab, text="Trim Video", command=trim_video)
trim_button.pack(pady=10)

# Add Text Overlay Tab
text_tab = ttk.Frame(notebook)
notebook.add(text_tab, text="Add Text Overlay")

def add_text_overlay():
    if video is None:
        messagebox.showwarning("Warning", "Please load a video first.")
        return
    text = text_entry.get()
    start_time = float(text_time_entry.get())
    duration = float(text_duration_entry.get())
    
    # Create a TextClip and CompositeVideoClip to overlay text
    text_clip = TextClip(text, fontsize=30, color='white').set_position('center').set_duration(duration)
    text_clip = text_clip.set_start(start_time)
    final_clip = CompositeVideoClip([video, text_clip])
    
    save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if save_path:
        final_clip.write_videofile(save_path)
        messagebox.showinfo("Saved", "Text overlay added and saved successfully!")

tk.Label(text_tab, text="Text:").pack()
text_entry = tk.Entry(text_tab)
text_entry.pack()

tk.Label(text_tab, text="Start Time (s):").pack()
text_time_entry = tk.Entry(text_tab)
text_time_entry.pack()

tk.Label(text_tab, text="Duration (s):").pack()
text_duration_entry = tk.Entry(text_tab)
text_duration_entry.pack()

text_button = tk.Button(text_tab, text="Add Text Overlay", command=add_text_overlay)
text_button.pack(pady=10)

# Merge Videos Tab
merge_tab = ttk.Frame(notebook)
notebook.add(merge_tab, text="Merge Videos")

def add_to_merge():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
    if file_path:
        videos_to_merge.append(VideoFileClip(file_path))
        messagebox.showinfo("Added", "Video added to merge list!")

def merge_videos():
    if len(videos_to_merge) > 1:
        final_clip = concatenate_videoclips(videos_to_merge)
        save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        if save_path:
            final_clip.write_videofile(save_path)
            messagebox.showinfo("Saved", "Merged video saved successfully!")
    else:
        messagebox.showwarning("Warning", "Add at least two videos to merge!")

add_button = tk.Button(merge_tab, text="Add Video to Merge", command=add_to_merge)
add_button.pack(pady=5)
merge_button = tk.Button(merge_tab, text="Merge Videos", command=merge_videos)
merge_button.pack(pady=10)

# Adding the Menu bar for better navigation
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Load Video", command=load_video)
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add menu bar to the window
root.config(menu=menu_bar)

root.mainloop()
