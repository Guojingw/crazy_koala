
# from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
# from kivy.uix.button import Button
from screens.components import BaseScreen, RoundedButton
# from kivy.uix.gridlayout import GridLayout
# from database.db_operations import insert_deposit

# import cv2
# import sounddevice as sd
# import wave
# import os
# from datetime import datetime
from kivy.uix.image import Image
# from kivy.clock import Clock
# from kivy.graphics.texture import Texture
# from kivy.animation import Animation

class OpenDoorScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mode = None

        # 主布局
        main_layout = BoxLayout(
            orientation="horizontal",
            spacing=50,
            padding=[100, 100, 100, 100],
        )
        
        # 左侧：图像部分
        left_col = BoxLayout(
            orientation="vertical",
            size_hint=(0.6, 1),
            padding=20
        )
        self.image = Image(
            source="assets\image copy 4.png",  # 默认仓门关闭图片
            size_hint=(1, 1)
        )
        left_col.add_widget(self.image)

        # 右侧：说明部分
        right_col = BoxLayout(
            orientation="vertical",
            size_hint=(0.4, 1),
            padding=20
        )
        self.instruction_label = Label(
            text="Open the door to store item",
            font_size=48,
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1),
            size_hint=(1, 0.8)
        )
        
        self.instruction_label.bind(size=self.instruction_label.setter('text_size'))
        right_col.add_widget(self.instruction_label)

        # 底部按钮
        button_layout = BoxLayout(
            orientation="horizontal",
            spacing=20,
            size_hint=(1, 0.1)
        )
        # back_button = RoundedButton(
        #     text="BACK",
        #     font_size=32,
        #     size_hint=(0.4, 1),
        #     custom_color=(0.5, 0.7, 1, 1)
        # )
        # back_button.bind(on_press=self.go_back)
        # button_layout.add_widget(back_button)

        next_button = RoundedButton(
            text="NEXT",
            font_size=48,
            size_hint=(0.4, 1),
            custom_color=(1, 0.8, 0.3, 1)
        )
        next_button.bind(on_press=self.go_next)
        button_layout.add_widget(next_button)

        right_col.add_widget(button_layout)

        # 添加到主布局
        main_layout.add_widget(left_col)
        main_layout.add_widget(right_col)

        self.add_widget(main_layout)

    def toggle_door(self):
        """模拟打开或关闭仓门"""
        if self.image.source == "/Users/guojing/comp/HRI2025/crazy_koala/assets/image.png":
            self.image.source = "/Users/guojing/comp/HRI2025/crazy_koala/assets/image copy 4.png"
            self.instruction_label.text = "The door is open. Place your item."
        else:
            self.image.source = "/Users/guojing/comp/HRI2025/crazy_koala/assets/image.png"
            self.instruction_label.text = "Close the door after storing the item."

    # def go_back(self, instance):
    #     """返回上一界面"""
    #     self.manager.current = "photo_audio_screen"
    
    def set_mode(self, mode):
        self.mode = mode

    def go_next(self, instance):
        """根据模式决定下一步逻辑"""
        if self.mode == "take_item":

            # 获取 PhotoAudioScreen 实例
            photo_audio_screen = self.manager.get_screen("photo_audio_screen")
            # 设置模式为 take_item
            photo_audio_screen.set_mode("take_item")
            # 导航到 PhotoAudioScreen
            self.manager.current = "photo_audio_screen"
        else:
           self.manager.current = "choose_interact_type"
