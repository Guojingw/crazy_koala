from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from screens.components import BaseScreen, YellowTitleBar
import os

class ViewMemoriesDetailScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 主布局
        self.main_layout = BoxLayout(orientation="vertical", spacing=20, padding=20)

        # 标题栏
        self.title_bar = YellowTitleBar(
            title_text="",  # 初始值，稍后会更新
            button_text="BACK",
            on_button_press=self.go_back,
        )
        self.main_layout.add_widget(self.title_bar)

        # 内容布局
        content_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.8), spacing=20)

        # Deposit 信息
        deposit_layout = BoxLayout(orientation="vertical", spacing=10)
        deposit_label = Label(
            text="DEPOSIT",
            font_size=48,
            bold=True,
            halign="center",
            valign="middle",
            size_hint=(1, 0.1),
            color=(0, 0, 0, 1),
        )
        deposit_label.bind(size=deposit_label.setter("text_size"))
        deposit_layout.add_widget(deposit_label)

        self.deposit_image = AsyncImage(size_hint=(1, 0.7))
        deposit_layout.add_widget(self.deposit_image)

        self.deposit_time_label = Label(
            text="Select the item you want to check",
            font_size=48,
            halign="center",
            valign="middle",
            size_hint=(1, 0.2),
            color=(0, 0, 0, 1),
        )
        self.deposit_time_label.bind(size=self.deposit_time_label.setter("text_size"))
        deposit_layout.add_widget(self.deposit_time_label)

        content_layout.add_widget(deposit_layout)

        # Taken 信息
        taken_layout = BoxLayout(orientation="vertical", spacing=10)
        taken_label = Label(
            text="TAKE",
            font_size=48,
            bold=True,
            halign="center",
            valign="middle",
            size_hint=(1, 0.1),
            color=(0, 0, 0, 1),
        )
        taken_label.bind(size=taken_label.setter("text_size"))
        taken_layout.add_widget(taken_label)

        self.taken_image = AsyncImage(size_hint=(1, 0.7))
        taken_layout.add_widget(self.taken_image)

        self.taken_time_label = Label(
            text="Select the item you want to check",
            font_size=48,
            halign="center",
            valign="middle",
            size_hint=(1, 0.2),
            color=(0, 0, 0, 1),
        )
        self.taken_time_label.bind(size=self.taken_time_label.setter("text_size"))
        taken_layout.add_widget(self.taken_time_label)

        content_layout.add_widget(taken_layout)
        self.main_layout.add_widget(content_layout)

        # 音频播放按钮布局
        audio_controls = BoxLayout(orientation="horizontal", size_hint=(1, 0.1), spacing=20)
        self.play_deposit_audio_button = Button(
            text="Play Deposit Audio",
            size_hint=(0.5, 1),
            on_press=self.play_deposit_audio,
        )
        audio_controls.add_widget(self.play_deposit_audio_button)

        self.play_taken_audio_button = Button(
            text="Play Taken Audio",
            size_hint=(0.5, 1),
            on_press=self.play_taken_audio,
        )
        audio_controls.add_widget(self.play_taken_audio_button)

        self.main_layout.add_widget(audio_controls)
        self.add_widget(self.main_layout)

    def on_enter(self, *args):
        """进入界面时更新内容"""
        current_item = self.manager.current_item
        if current_item:
            # 更新标题栏
            self.title_bar.update_title(current_item.get("name", "No Name Available"))

            # 更新存储信息
            self.deposit_image.source = current_item.get("deposit_photo_path", "")
            self.deposit_time_label.text = f"Deposit Time: {current_item.get('deposit_time', 'Not Available')}"

            # 更新取走信息
            self.taken_image.source = current_item.get("taken_photo_path", "")
            self.taken_time_label.text = f"Taken Time: {current_item.get('taken_time', 'Not Available')}"
        else:
            print("No item to display!")

    def play_deposit_audio(self, instance):
        """播放存储音频"""
        current_item = self.manager.current_item
        audio_path = current_item.get("deposit_audio_path", "") if current_item else ""
        if audio_path and os.path.exists(audio_path):
            from pydub import AudioSegment
            from pydub.playback import play

            try:
                audio = AudioSegment.from_file(audio_path)
                play(audio)
            except Exception as e:
                print(f"Error playing deposit audio: {e}")
        else:
            print("Deposit audio not found!")

    def play_taken_audio(self, instance):
        """播放取走音频"""
        current_item = self.manager.current_item
        audio_path = current_item.get("taken_audio_path", "") if current_item else ""
        if audio_path and os.path.exists(audio_path):
            from pydub import AudioSegment
            from pydub.playback import play

            try:
                audio = AudioSegment.from_file(audio_path)
                play(audio)
            except Exception as e:
                print(f"Error playing taken audio: {e}")
        else:
            print("Taken audio not found!")

    def go_back(self, instance):
        """返回到上一个界面"""
        self.manager.current = "happy_memories_screen"
