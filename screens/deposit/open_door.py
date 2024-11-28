from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from screens.components import BaseScreen, RoundedButton, YellowBar
from kivy.uix.image import Image


class OpenDoorScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.mode = "deposit"

        layout = BoxLayout(
            orientation="vertical",
            spacing=50,
        )
        
        self.title_bar = YellowBar(
            "",
        )
        layout.add_widget(self.title_bar)

        # 主布局
        main_layout = BoxLayout(
            orientation="horizontal",
            spacing=50,
            padding=[100, 20, 100, 20],
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
            text="",
            font_size=36,
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1),
            size_hint=(1, 0.8),
            font_name="assets/fonts/Poppins/Poppins-Medium.ttf"
        )
        
        self.instruction_label.bind(size=self.instruction_label.setter('text_size'))
        right_col.add_widget(self.instruction_label)

        # 底部按钮
        button_layout = BoxLayout(
            orientation="horizontal",
            spacing=20,
            size_hint=(1, 0.1)
        )
        
        spacer = BoxLayout(size_hint=(1, 1))
        button_layout.add_widget(spacer)

        next_button = RoundedButton(
            text="NEXT",
            font_size=24,
            size_hint=(None, 1),
            width=200,
            custom_color=(0.933, 0.757, 0.318, 1),
            font_name="assets/fonts/Poppins/Poppins-Bold.ttf"
        )
        next_button.bind(on_press=self.go_next)
        button_layout.add_widget(next_button)

        right_col.add_widget(button_layout)

        # 添加到主布局
        main_layout.add_widget(left_col)
        main_layout.add_widget(right_col)

        layout.add_widget(main_layout)

        end_bar = YellowBar(
            title_text="",
        )
        layout.add_widget(end_bar)

        self.add_widget(layout)
    
    def on_enter(self):
        """动态更新界面"""
        mode = self.manager.get_mode()  # 获取全局 mode
        self.mode = mode
        if mode == "deposit":
            self.title_bar.update_title("DEPOSIT")
            self.instruction_label.text = "Open the door to store the item."
        elif mode == "take":
            self.title_bar.update_title("TAKE")
            self.instruction_label.text = "Open the door to retrieve the item."
        else:
            self.title_bar.update_title("UNKNOWN")
            self.instruction_label.text = "Mode not set."
        self.manager.trigger_open_door()

    def toggle_door(self):
        """模拟打开或关闭仓门"""
        if self.image.source == "/Users/guojing/comp/HRI2025/crazy_koala/assets/image.png":
            self.image.source = "/Users/guojing/comp/HRI2025/crazy_koala/assets/image copy 4.png"
            self.instruction_label.text = "The door is open. Place your item."
        else:
            self.image.source = "/Users/guojing/comp/HRI2025/crazy_koala/assets/image.png"
            self.instruction_label.text = "Close the door after storing the item."

    
    def set_mode(self, mode):
        self.mode = mode

    def go_next(self, instance):
        """根据模式决定下一步逻辑"""
        if self.mode == "take":
            self.manager.switch_to("photo_audio_screen", mode="take")
        else:
           self.manager.current = "choose_interact_type"
