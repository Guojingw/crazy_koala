from kivy.config import Config
Config.set("graphics", "fullscreen", "auto")  # 全屏模式
Config.set("graphics", "borderless", "1")  # 无边框窗口
Config.set("graphics", "width", "1440")
Config.set("graphics", "height", "900")
Config.set("graphics", "resizable", False)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.home_page import HomePage, ChooseInteractType
from screens.deposit.input_item_name import InputNameScreen
from screens.deposit.photo_audio_record import PhotoAudioScreen
from screens.deposit.open_door import OpenDoorScreen
from screens.take.select_take_item import SelectTakeItemScreen
from screens.take.view_deposit_info import ViewDepositInfoScreen
from screens.memories.select_memories import HappyMemoriesScreen
from screens.memories.view_memories_details import ViewMemoriesDetailScreen
from database.db_setup import initialize_database

class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_item = {}
        self.add_widget(HomePage(name="home"))
        self.add_widget(ChooseInteractType(name="choose_interact_type"))
        self.add_widget(InputNameScreen(name="input_name_screen"))
        self.add_widget(PhotoAudioScreen(name="photo_audio_screen"))
        self.add_widget(OpenDoorScreen(name="open_door_screen"))
        self.add_widget(SelectTakeItemScreen(name="select_take_screen"))
        self.add_widget(ViewDepositInfoScreen(name="view_deposit_info_screen"))
        self.add_widget(HappyMemoriesScreen(name="happy_memories_screen"))
        self.add_widget(ViewMemoriesDetailScreen(name="view_memories_details_screen"))

class CrazyKoalaApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == "__main__":
    initialize_database()
    CrazyKoalaApp().run()
