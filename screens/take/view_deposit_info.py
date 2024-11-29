# from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from screens.components import BaseScreen, RoundedButton, YellowBar, YellowTitleBar
import os
from playsound import playsound

class ViewDepositInfoScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            spacing=20,
        )

        main_layout = BoxLayout(
            orientation="vertical",
            spacing=20,
            padding=[100, 20, 100, 20],
        )

        # 添加 YellowBar
        self.title_bar = YellowBar(
            title_text="",
        )
        layout.add_widget(self.title_bar)

        # 图片展示
        self.image_display = AsyncImage(
            source="",
            size_hint=(1, 0.5),
            allow_stretch=True,
            keep_ratio=True
        )
        main_layout.add_widget(self.image_display)

        # 信息布局
        info_layout = BoxLayout(orientation="horizontal", spacing=10, size_hint=(1, 0.3))

        # 名字标签
        self.name_label = Label(
            text="Item Name: Not Available",
            font_size=36,
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
            size_hint=(1, 0.5)
        )


        # 音频播放按钮
        audio_controls = BoxLayout(orientation="horizontal", size_hint=(0.5, 0.5), spacing=20)
        self.play_button = RoundedButton(
            text="PLAY AUDIO",
            font_size=24,
            size_hint=(None, 0.8),
            width=200,
            font_name="assets/fonts/Poppins/Poppins-Bold.ttf",
            on_press=self.play_audio
        )
        audio_controls.add_widget(self.play_button)

        self.audio_label = Label(
            text="Audio: Not Playing",
            font_size=24,
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
            size_hint=(0.6, 1),
            font_name="assets/fonts/Poppins/Poppins-Medium.ttf"
        )
        self.audio_label.bind(size=self.audio_label.setter("text_size"))
        audio_controls.add_widget(self.audio_label)
        info_layout.add_widget(audio_controls)
        
        spacer = BoxLayout(size_hint=(0.2, 1))
        info_layout.add_widget(spacer)
        
        # 存放时间标签
        self.time_label = Label(
            text="Deposit Time: Not Available",
            font_size=24,
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
            size_hint=(0.5, 0.5),
            font_name="assets/fonts/Poppins/Poppins-Medium.ttf"
        )
        self.time_label.bind(size=self.time_label.setter("text_size"))
        info_layout.add_widget(self.time_label)
        

        main_layout.add_widget(info_layout)

        # 底部按钮
        bottom_controls = BoxLayout(orientation="horizontal", size_hint=(1, 0.2), spacing=20)
        back_button = RoundedButton(
            text="BACK",
            font_size=24,
            size_hint=(None, 0.5),
            width=200,
            custom_color=(0, 0, 0, 1),
            font_name="assets/fonts/Poppins/Poppins-Bold.ttf",
            on_press=self.go_back
        )

        bottom_controls.add_widget(back_button)
        
        spacer = BoxLayout(size_hint=(1, 1))
        bottom_controls.add_widget(spacer)

        next_button = RoundedButton(
            text="SELECT",
            font_size=24,
            size_hint=(None, 0.5),
            width=200,
            custom_color=(0, 0, 0, 1),
            font_name="assets/fonts/Poppins/Poppins-Bold.ttf",
            on_press=lambda instance: self.navigate_to_open_door(mode="take_item") 
        )
        bottom_controls.add_widget(next_button)
        main_layout.add_widget(bottom_controls)
        layout.add_widget(main_layout)
        
        end_bar = YellowBar(
            title_text="",
        )
        layout.add_widget(end_bar)
        
        self.add_widget(layout)

    def set_item(self):
        """根据当前选择的物品设置界面内容"""
        current_item = self.manager.current_item
        if current_item:
            # Update the title bar with the item name
            self.title_bar.update_title(current_item.get("name", "No Name Available"))

            self.image_path = current_item.get("image_path", "")
            self.audio_path = current_item.get("audio_path", "")
            self.image_display.source = self.image_path if os.path.exists(self.image_path) else ""
            self.name_label.text = f"Item Name: {current_item.get('name', 'Not Available')}"
            self.time_label.text = f"Deposit Time: {current_item.get('deposit_time', 'Not Available')}"
        else:
            print("No item selected!")

    def on_enter(self):
        """进入界面时设置内容"""
        self.set_item()

    def play_audio(self, instance):
        """播放音频"""
        if os.path.exists(self.audio_path):
            self.audio_label.text = "Audio: Playing..."
            try:
                playsound(self.audio_path)
                self.audio_label.text = "Audio: Finish Playing"
            except Exception as e:
                print(f"Error playing audio: {e}")
                self.audio_label.text = "Audio: Not Playing"
        else:
            self.audio_label.text = "Audio: No Audio Message Left"

    def go_back(self, instance):
        """返回上一个界面"""
        self.manager.current_item = None
        self.manager.current = "select_take_screen"

    def navigate_to_open_door(self, mode):
        self.manager.switch_to("open_door_screen", mode="take")

        # open_door_screen = self.manager.get_screen("open_door_screen")
        # open_door_screen.set_mode(mode)
        # self.manager.current = "open_door_screen"
