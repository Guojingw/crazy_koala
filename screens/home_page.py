from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from screens.components import BaseScreen, RoundedButton, YellowBar, YellowTitleBar

class HomePage(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 设置主布局
        layout = BoxLayout(
            orientation="horizontal",
            spacing=50,
            padding=[100, 100, 100, 100],  # Padding: [left, top, right, bottom]
        )

        # 设置背景颜色为白色
        with self.canvas.before:
            Color(1, 1, 1, 1)  # 白色背景
            self.bg = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_bg, pos=self._update_bg)

        # 添加左侧图片
        img = Image(
            source="assets\door_close.png",  # 替换为图片路径
            allow_stretch=True,
            keep_ratio=True
        )
        layout.add_widget(img)

        # 添加右侧文字布局
        text_layout = BoxLayout(orientation="vertical", spacing=10)

        # 主标题
        title_label = Label(
            text="Connect to our community\nTogether",
            font_size=72,
            color=(0, 0, 0, 1),
            halign="left",
            valign="bottom",
            size_hint=(1, 0.5),
            font_name="assets/fonts/Poppins/Poppins-ExtraBold.ttf"
        )
        title_label.bind(size=title_label.setter("text_size"))

        text_layout.add_widget(title_label)

        second_label = Label(
            text="For better future",
            font_size=48,
            color=(0, 0, 0, 1),
            halign="left",
            valign="top",
            size_hint=(1, 0.3),
            font_name="assets/fonts/Poppins/Poppins-LightItalic.ttf"
        )
        second_label.bind(size=second_label.setter("text_size"))

        text_layout.add_widget(second_label)

        start_button = RoundedButton(
            text="Press Koala Nose To Start",
            font_size=36,
            size_hint=(1, 0.1),
            custom_color=(0, 0, 0, 1),
            font_name="assets/fonts/Poppins/Poppins-Bold.ttf"
        )
        text_layout.add_widget(start_button)

        layout.add_widget(text_layout)


        layout.bind(on_touch_down=self.go_to_next_page)

        # 添加主布局到屏幕
        self.add_widget(layout)

    def _update_bg(self, *args):
        """动态更新背景大小和位置"""
        self.bg.size = self.size
        self.bg.pos = self.pos

    def go_to_next_page(self, instance, touch):
        """跳转到第二个页面"""
        self.manager.current = "choose_interact_type"

class ChooseInteractType(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout: center everything vertically
        layout = BoxLayout(
            orientation="vertical",
            spacing=50,
        )

        title_bar = YellowBar(
            title_text="Home Page",
        )
        layout.add_widget(title_bar)

         # Main layout: center everything vertically
        main_layout = BoxLayout(
            orientation="vertical",
            spacing=50,
            padding=[100, 50, 100, 100],  # Padding: [left, top, right, bottom]
        )

        # First row: DEPOSIT and TAKE buttons
        first_row = BoxLayout(
            orientation="horizontal",
            spacing=100,
            size_hint=(1, 0.5),
        )
        deposit_button = RoundedButton(
            text="DEPOSIT",
            font_size=64,
            size_hint=(0.4, 1),
            custom_color=(1, 0.8, 0, 1),
            font_name="assets/fonts/Poppins/Poppins-Bold.ttf"
        )
        first_row.add_widget(deposit_button)
        deposit_button.bind(on_press=self.go_to_input_name_screen)
        
        take_button = RoundedButton(
            text="TAKE",
            font_size=64,
            size_hint=(0.4, 1),
            custom_color=(0.6, 1, 0.6, 1),  # Green
            font_name="assets/fonts/Poppins/Poppins-Bold.ttf"
        )

        first_row.add_widget(take_button)
        take_button.bind(on_press=self.go_to_select_take_screen)

        # Second row: Check happiness memories and End by pressing nose buttons
        second_row = BoxLayout(
            orientation="horizontal",
            spacing=100,
            size_hint=(1, 0.2),  # Occupy 30% of the height
        )
        memeries_button = RoundedButton(
            text="Happiness Memories",
            font_size=48,
            size_hint=(0.4, 0.5),
            custom_color=(0.9, 0.9, 0.9, 1),  # Gray
            font_name="assets/fonts/Poppins/Poppins-Bold.ttf"
        )
        second_row.add_widget(memeries_button)
        memeries_button.bind(on_press=self.go_to_select_memeries)
        
        hint_layout = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint=(0.4, 0.5),
        )
        # 插入图片
        hint_image = Image(
            source="assets\simple_logo.png",
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(0.3, 1),
        )
        hint_layout.add_widget(hint_image)

        # 添加提示文字
        hint_label = Label(
            text="End by pressing nose",
            font_size=36,
            color=(0, 0, 0, 1),
            halign="center",
            valign="middle",
            size_hint=(0.7, 1),
            font_name="assets/fonts/Poppins/Poppins-Bold.ttf"
        )
        hint_label.bind(size=hint_label.setter("text_size"))
        hint_layout.add_widget(hint_label)
        
        second_row.add_widget(hint_layout)

        # Add rows to the main layout
        main_layout.add_widget(first_row)
        main_layout.add_widget(second_row)
        layout.add_widget(main_layout)

        end_bar = YellowBar(
            title_text="",
        )
        layout.add_widget(end_bar)

        self.add_widget(layout)
        
    def go_to_input_name_screen(self, instance):
        """跳转到 InputNameScreen"""
        # self.manager.mode = "deposit"
        # self.manager.current = "input_name_screen"
        self.manager.switch_to("input_name_screen", mode="deposit")
    
    def go_to_select_take_screen(self, instance):
        """跳转到 SelectTakeItemScreen"""
        # self.manager.mode = "take"
        take_item_screen = self.manager.get_screen("select_take_screen")
        take_item_screen.load_items()
        # self.manager.current = "select_take_screen"
        self.manager.switch_to("select_take_screen", mode="take")
    
    def go_to_select_memeries(self, instance):
        """跳转到 Select memeries"""
        take_item_screen = self.manager.get_screen("happy_memories_screen")
        take_item_screen.load_items()
        self.manager.current = "happy_memories_screen"
