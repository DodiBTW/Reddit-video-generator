import os
import numpy as np

import random
import video.subtitles as subtitles
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, VideoClip
from moviepy.video.fx.Crop import Crop
from pydub import AudioSegment
from moviepy import AudioFileClip, AudioClip, AudioArrayClip, concatenate_audioclips
class Video:
    def __init__(self, output_name , title , body, video_length = 0, audio_delay = 0):
        self.save_path = os.path.join('output', output_name + '.mp4')
        body_audio_path = os.path.join('temp', 'temporary_body_audio.mp3')
        title_audio_path = os.path.join('temp', 'temporary_title_audio.mp3')
        self.output_name = output_name
        self.audio_delay = audio_delay
        self.body_mp3 = AudioFileClip(body_audio_path)
        self.title_mp3 = AudioFileClip(title_audio_path)
        self.text = body
        self.title = title

    def choose_random_video(self):
        background_videos_path = os.path.join('assets' , 'videos')
        files = [f for f in os.listdir(background_videos_path) if os.path.isfile(os.path.join(background_videos_path, f))]
        if '.gitkeep' in files:
            files.remove('.gitkeep')
        if files:
            return random.choice(files)
        else:
            raise Exception("Files not found in assets/videos/ folder.")
        
    def add_audios(self,comment_audio = None):
        fps = self.title_mp3.fps

        silence_frames = int(self.audio_delay * fps)
        if silence_frames > 0:
            silence = AudioArrayClip(np.zeros((silence_frames, 2)), fps=fps) # Silence is an audio clip which lasts x seconds in between audio segments
        else:
            silence = AudioArrayClip(np.zeros((1, 2)), fps=fps)

        final = concatenate_audioclips([ self.title_mp3, silence, self.body_mp3])
        if comment_audio is not None:
            return concatenate_audioclips([final, silence, comment_audio])
        else:
            return final

    def crop_video(self, video):
        # crops a video down to a phone's aspect ration
        video_width, video_height = video.size
        crop_width = video_height * 9 / 16
        return video.cropped(width=crop_width, height=video_height, x_center=video_width / 2, y_center=video_height / 2)

    def trim_video(self,video,audio):
        duration = video.duration
        audio_duration = audio.duration
        start_timeframe = random.randint(0, int(duration - audio_duration))
        return video.subclipped(start_timeframe, start_timeframe + (audio_duration+3))

    def is_desktop_aspect_ratio(self, video):
        video_width, video_height = video.size
        aspect_ratio = video_width / video_height
        return aspect_ratio == 16 / 9

    def add_subtitles(self, video, subtitles, font='Poppins', fontsize=36, max_width=400, stroke_width=3, color='white', text_outline='black'):
        font = "assets/fonts/" + font + ".ttf"
        clips = [TextClip(font,subtitle[1], stroke_width=stroke_width,stroke_color=text_outline, color=color ,font_size=fontsize, size=(max_width, None)).with_position(('center', 'center')).with_duration(subtitle[0]).with_start(subtitle[2]) for subtitle in subtitles]
        return CompositeVideoClip([video] + clips)
    def create_video(self, random_video = True, path="", fade_duration = 1.5):
        """
            This function is supposed to add text onto a random/specified background video, then layer the audio correctly.
        """
        if random_video:
            video_name = self.choose_random_video()
        else:
            video_name = path

        final_audio = self.add_audios()
        video_path = os.path.join('assets', 'videos', video_name)

        ## Cropping to 9:16 and adjusting video duration
        background_video = VideoFileClip(video_path)
        trimmed_clip = self.trim_video(background_video,final_audio)
        if self.is_desktop_aspect_ratio(trimmed_clip):
            cropped_clip = self.crop_video(trimmed_clip)
        else:
            cropped_clip = trimmed_clip

        # Subtitles and audio
        audio_on_video = cropped_clip.with_audio(final_audio)
        subtitle_manager = subtitles.Subtitles(self.title, self.text)
        title_speak_time = subtitle_manager.get_speaking_duration(self.title) + 0.5
        body_clips = subtitle_manager.get_subtitle_array_into_subtitles(subtitle_manager.get_divided_body(), title_speak_time)
        title_clip = [(title_speak_time, subtitles.Subtitles.add_line_breaks(self.title), 0.2)]
        for i in range(len(body_clips)):
            body_clips[i] = (body_clips[i][0], subtitles.Subtitles.add_line_breaks(body_clips[i][1]), body_clips[i][2])
        subtitles_clips =   title_clip + body_clips
        subtitled_video = self.add_subtitles(audio_on_video, subtitles_clips, color="white")
        subtitled_video.write_videofile(self.save_path,codec="libx264")
        background_video.close()
        cropped_clip.close()
        trimmed_clip.close()