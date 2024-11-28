from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from screens.components import BaseScreen, RoundedButton, YellowBar, YellowTitleBar
from playsound import playsound
import os


class ViewMemoriesDetailScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 主布局
        layout = BoxLayout(
            orientation="vertical",
            spacing=20,
        )

        main_layout = BoxLayout(
            orientation="vertical",
            spacing=20,
            padding=[100, 20, 100, 20],  # Padding: [left, top, right, bottom]
        )

        # 添加 YellowBar
        self.title_bar = YellowTitleBar(
            title_text="Item Name",  # Placeholder text, will update on_enter
            button_text="BACK",
            on_button_press=self.go_back,
        )
        layout.add_widget(self.title_bar)

        # 内容布局
        content_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.8), spacing=20)

        # Deposit 信息
        deposit_layout = BoxLayout(orientation="vertical", spacing=10)
        deposit_label = Label(
            text="DEPOSIT",
            font_size=36,
            bold=True,
            halign="center",
            valign="middle",
            size_hint=(1, 0.1),
            color=(0, 0, 0, 1),
            font_name="assets/fonts/Poppins/Poppins-Bold.ttf"
        )
        deposit_label.bind(size=deposit_label.setter("text_size"))
        deposit_layout.add_widget(deposit_label)

        self.deposit_image = AsyncImage(size_hint=(1, 0.7))
        deposit_layout.add_widget(self.deposit_image)

        self.deposit_time_label = Label(
            text="deposit_time",
            font_size=36,
            halign="center",
            valign="middle",
            size_hint=(1, 0.2),
            color=(0, 0, 0, 1),
            font_name="assets/fonts/Poppins/Poppins-Medium.ttf"
        )
        self.deposit_time_label.bind(size=self.deposit_time_label.setter("text_size"))
        deposit_layout.add_widget(self.deposit_time_label)

        content_layout.add_widget(deposit_layout)

        # Taken 信息
        taken_layout = BoxLayout(orientation="vertical", spacing=10)
        taken_label = Label(
            text="TAKE",
            font_size=36,
            bold=True,
            halign="center",
            valign="middle",
            size_hint=(1, 0.1),
            color=(0, 0, 0, 1),
            font_name="assets/fonts/Poppins/Poppins-Bold.ttf"
        )
        taken_label.bind(size=taken_label.setter("text_size"))
        taken_layout.add_widget(taken_label)

        self.taken_image = AsyncImage(size_hint=(1, 0.7))
        taken_layout.add_widget(self.taken_image)

        self.taken_time_label = Label(
            text="taken_time",
            font_size=36,
            halign="center",
            valign="middle",
            size_hint=(1, 0.2),
            color=(0, 0, 0, 1),
            font_name="assets/fonts/Poppins/Poppins-Medium.ttf"
        )
        self.taken_time_label.bind(size=self.taken_time_label.setter("text_size"))
        taken_layout.add_widget(self.taken_time_label)

        content_layout.add_widget(taken_layout)
        main_layout.add_widget(content_layout)

        # 音频播放按钮布局
        audio_controls = BoxLayout(orientation="horizontal", size_hint=(1, 0.1), spacing=20)

        self.play_deposit_audio_button = RoundedButton(
            text="Play Deposit Audio",
            font_size=36,
            size_hint=(0.5, 1),
            custom_color=(0, 0, 0, 1),
            font_name="assets/fonts/Poppins/Poppins-Bold.ttf",
            on_press=lambda instance: self.play_audio("deposit_audio_path")
        )
        audio_controls.add_widget(self.play_deposit_audio_button)
        
        self.play_taken_audio_button = RoundedButton(
            text="Play Taken Audio",
            font_size=36,
            size_hint=(0.5, 1),
            custom_color=(0, 0, 0, 1),
            font_name="assets/fonts/Poppins/Poppins-Bold.ttf",
            on_press=lambda instance: self.play_audio("taken_audio_path")
        )
        audio_controls.add_widget(self.play_taken_audio_button)

        main_layout.add_widget(audio_controls)
        layout.add_widget(main_layout)
        
        end_bar = YellowBar(
            title_text="",
        )
        layout.add_widget(end_bar)
        self.add_widget(layout)

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

    def play_audio(self, audio_type):
        """播放音频"""
        current_item = self.manager.current_item
        audio_path = current_item.get(audio_type, "") if current_item else ""
        if audio_path and os.path.exists(audio_path):
            try:
                playsound(audio_path)
                print(f"Finished playing {audio_type} audio.")
            except Exception as e:
                print(f"Error playing {audio_type} audio: {e}")
        else:
            print(f"{audio_type.replace('_', ' ').title()} not found!")

    def go_back(self, instance):
        """返回到上一个界面"""
        self.manager.current = "happy_memories_screen"
