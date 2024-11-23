
# from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
# from kivy.uix.button import Button
from screens.components import BaseScreen, RoundedButton
# from kivy.uix.gridlayout import GridLayout
from database.db_operations import insert_deposit, update_taken

import cv2
import sounddevice as sd
import wave
import os
# from datetime import datetime
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
# from kivy.animation import Animation


class PhotoAudioScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_name = None  # 物品名称
        self.photo_path = None
        self.audio_path = None
        
        self.camera = None  # 摄像头实例
        self.preview_mode = False  # 是否为预览模式
        self.default_photo_path = "assets\default_photo.jpg" # defalt figure path
        
        self.recording_active = False
        self.record_timer = 0
        self.max_duration = 60  # 最长录音时长，单位为秒
        self.default_audio_path = "assets\default_audio.wav"
        
        self.mode = "deposit"

        # 主布局
        main_layout = BoxLayout(
            orientation="horizontal",
            spacing=50,
            padding=[100, 100, 100, 100],
        )
        
        first_col = BoxLayout(
            orientation="vertical",
            spacing=50,
            size_hint=(0.6, 1),
        )
        
        self.image_widget = Image(size_hint=(1, 0.7))
        first_col.add_widget(self.image_widget)

        # 摄像头按钮
        self.camera_frame = RoundedButton(
            text="Click to open camera",
            font_size=48,
            size_hint=(1, 0.1),
            custom_color=(0.9, 0.9, 0.9, 1)  # Gray
        )
        first_col.add_widget(self.camera_frame)
        self.camera_frame.bind(on_press=self.toggle_camera_preview)
        
        # 状态标签
        self.status_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(1, 0.1),
            spacing=10
        )

        # 图标（默认状态图标）
        self.status_icon = Image(
            source="assets\image copy.png",  # 替换为你的图标路径
            size_hint=(0.1, 1)
        )
        self.status_layout.add_widget(self.status_icon)

        # 标签
        self.status_label = Label(
            text="Ready to record audio",
            font_size=24,
            color=(0, 0, 0, 1),
            size_hint=(0.9, 1)
        )
        self.status_layout.add_widget(self.status_label)

        first_col.add_widget(self.status_layout)
        
        self.record_button = RoundedButton(
            text="Click to record audio",
            font_size=48,
            size_hint=(1, 0.1),
            custom_color=(0.9, 0.9, 0.9, 1)  # Gray
        )
        first_col.add_widget(self.record_button)
        self.record_button.bind(on_press=self.toggle_recording)
        

        second_col = BoxLayout(
            orientation="vertical",
            spacing=50,
            size_hint=(0.4, 1),
        )
        
        # 提示文本
        text_label = Label(
            text="Do you want to take a photo\nor leave a audio message?",
            font_size=48,
            halign="left",
            valign="middle",
            color=(0, 0, 0, 1),
            size_hint=(1, 0.6)
        )
        second_col.add_widget(text_label)

        # 底部按钮
        button_layout = BoxLayout(orientation="horizontal", spacing=20, size_hint=(1, 0.1))
        back_button = RoundedButton(
            text="BACK",
            font_size=48,
            size_hint=(0.4, 0.65),
            custom_color=(0.9, 0.9, 0.9, 1)  # Gray
        )
        button_layout.add_widget(back_button)
        back_button.bind(on_press=self.go_back)
        
        next_button = RoundedButton(
            text="NEXT",
            font_size=48,
            size_hint=(0.4, 0.65),
            custom_color=(0.9, 0.9, 0.9, 1)  # Gray
        )
        button_layout.add_widget(next_button)
        next_button.bind(on_press=self.go_next)
        
        second_col.add_widget(button_layout)

        main_layout.add_widget(first_col)
        main_layout.add_widget(second_col)

        # 添加按钮布局到主界面
        self.add_widget(main_layout)


    def toggle_camera_preview(self, instance):
        """打开或关闭摄像头实时预览"""
        if not self.preview_mode:
            # 启动摄像头预览
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                print("Error: Cannot access the camera")
                return
            self.preview_mode = True
            self.camera_frame.text = "Click to capture photo"
            Clock.schedule_interval(self.update_camera_preview, 1.0 / 30.0)  # 每秒30帧
        else:
            # 捕获照片并关闭摄像头预览
            ret, frame = self.camera.read()
            if ret:
                # 保存照片
                temp_folder = "temp"
                if not os.path.exists(temp_folder):
                    os.makedirs(temp_folder)

                # 删除临时目录中已有的照片
                for file in os.listdir(temp_folder):
                    if file.endswith(".jpg"):
                        os.remove(os.path.join(temp_folder, file))

                # 保存新照片到临时目录
                self.photo_path = os.path.join(temp_folder, "temp_photo.jpg")
                cv2.imwrite(self.photo_path, frame)
                print(f"Photo temporarily saved: {self.photo_path}")

                # 停止摄像头
                self.camera.release()
                self.camera = None
                self.preview_mode = False
                self.camera_frame.text = "Click to open camera"
                Clock.unschedule(self.update_camera_preview)

                # 显示静态照片
                self.display_photo(frame)
            else:
                print("Error: Could not capture photo")

    def update_camera_preview(self, dt):
        """更新摄像头实时画面"""
        if self.camera:
            ret, frame = self.camera.read()
            if ret:
                frame = cv2.rotate(frame, cv2.ROTATE_180)
                
                # 转换 BGR 到 RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                buf = frame.tobytes()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
                texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
                self.image_widget.texture = texture

    def display_photo(self, frame):
        """显示拍摄的静态照片"""
        frame = cv2.rotate(frame, cv2.ROTATE_180)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        buf = frame.tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.image_widget.texture = texture
    
    def toggle_recording(self, instance):
        """开始或停止录音"""
        if not self.recording_active:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """开始录音"""
        try:
            # 检查设备默认采样率
            device_info = sd.query_devices(sd.default.device, 'input')
            self.fs = int(device_info['default_samplerate'])

            # 删除旧的临时音频
            temp_folder = "temp"
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)

            for file in os.listdir(temp_folder):
                if file.endswith(".wav"):
                    os.remove(os.path.join(temp_folder, file))

            # 设置临时音频路径
            self.audio_path = os.path.join(temp_folder, "temp_audio.wav")

            # 开始录音
            self.recording = sd.rec(int(self.max_duration * self.fs), samplerate=self.fs, channels=1, dtype='int16')
            self.recording_active = True
            self.record_timer = 0
            Clock.schedule_interval(self.update_recording_status, 1.0)  # 每秒更新状态
            self.status_label.text = "Recording... 0s"
            self.record_button.text = "Stop Recording"
            print("Recording started.")
        except Exception as e:
            print(f"Error starting recording: {e}")

    def stop_recording(self):
        """停止录音"""
        if not self.recording_active:
            return

        try:
            sd.stop()
            Clock.unschedule(self.update_recording_status)  # 停止更新状态
            self.recording_active = False

            # 保存录音
            with wave.open(self.audio_path, 'w') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self.fs)
                wf.writeframes(self.recording[:int(self.record_timer * self.fs)].tobytes())

            self.status_label.text = "Recording saved!"
            self.record_button.text = "Start Recording"
            print(f"Audio saved at {self.audio_path}")
        except Exception as e:
            print(f"Error stopping recording: {e}")

    def update_recording_status(self, dt):
        """更新录音状态"""
        self.record_timer += dt
        if self.record_timer >= self.max_duration:
            self.status_label.text = "Maximum duration reached. Stopping recording..."
            self.stop_recording()
        else:
            self.status_label.text = f"Recording... {int(self.record_timer)}s"
            
    def reset(self):
        """重置界面内容"""
        self.photo_path = None
        self.audio_path = None
        self.image_widget.texture = None  # 清空图片预览
        self.camera_frame.text = "Click to open camera"
        self.status_label.text = "Ready to record audio"
        self.record_button.text = "Click to record audio"
        self.recording_active = False
        self.record_timer = 0
        self.preview_mode = False

        # 停止摄像头预览（如果未停止）
        if self.camera:
            self.camera.release()
            self.camera = None
            Clock.unschedule(self.update_camera_preview)

        # 清理临时目录中的文件
        temp_folder = "temp"
        if os.path.exists(temp_folder):
            for file in os.listdir(temp_folder):
                if file.endswith(".jpg") or file.endswith(".wav"):
                    os.remove(os.path.join(temp_folder, file))
            print("Temporary files cleared.")

    
    def prepare_folder(self):
        """创建项目文件夹"""
        if not self.item_name:
            print("Item name is required to create folder!")
            return

        self.folder_path = f"data/{self.item_name}"
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            print(f"Folder created: {self.folder_path}")
    
    def set_mode(self, mode):
        """设置当前界面的模式"""
        self.mode = mode
        if self.mode == "deposit":
            print("Mode set to DEPOSIT")
        elif self.mode == "take":
            print("Mode set to TAKE")


    def go_back(self, instance):
        """返回上一个界面并清理临时数据"""
        # 清理临时目录中的照片
        temp_folder = "temp"
        if os.path.exists(temp_folder):
            for file in os.listdir(temp_folder):
                if file.endswith(".jpg") or file.endswith(".wav"):
                    os.remove(os.path.join(temp_folder, file))
            print("Temporary photos cleared.")

        self.reset()
        self.manager.current = "input_name_screen"
            
    def save_file(self, file_path, default_path, folder_path, file_name):
        """保存文件到指定文件夹，如果文件不存在则使用默认文件"""
        if file_path and os.path.exists(file_path):
            # 移动文件到目标文件夹
            final_path = os.path.join(folder_path, file_name)
            os.rename(file_path, final_path)
            print(f"File moved to: {final_path}")
        else:
            # 使用默认文件
            final_path = os.path.join(folder_path, file_name)
            if not os.path.exists(final_path):
                if os.path.exists(default_path):
                    import shutil
                    shutil.copy(default_path, final_path)
            print(f"No file provided, using default file: {final_path}")
        return final_path

    def go_next(self, instance):
        """跳过到下一个界面"""

        # 更新数据库中的照片和音频路径
        if self.mode == "deposit":
            self.prepare_folder()
            self.photo_path = self.save_file(
                file_path=self.photo_path,
                default_path=self.default_photo_path,
                folder_path=self.folder_path,
                file_name=f"{self.item_name}_deposit_photo.jpg"
            )

            self.audio_path = self.save_file(
                file_path=self.audio_path,
                default_path=self.default_audio_path,
                folder_path=self.folder_path,
                file_name=f"{self.item_name}_deposit_audio.wav"
            )
            
            # 保存到数据库
            insert_deposit(
                name=self.item_name,
                deposit_photo_path=self.photo_path,
                deposit_audio_path=self.audio_path
            )
            
            print(f"Stored photo: {self.photo_path}, audio: {self.audio_path}")
            
            self.reset()

            self.manager.current = "open_door_screen"
        else:  # take 模式
            # 假设 current_item 是当前选中的物品
            current_item = self.manager.current_item
            if current_item:
                self.item_name = current_item["name"]  # 获取当前物品的 ID
                print(f"item name {self.item_name}")

                self.prepare_folder()
                
                self.photo_path = self.save_file(
                    file_path=self.photo_path,
                    default_path=self.default_photo_path,
                    folder_path=self.folder_path,
                    file_name=f"{self.item_name}_taken_photo.jpg"
                )

                self.audio_path = self.save_file(
                    file_path=self.audio_path,
                    default_path=self.default_audio_path,
                    folder_path=self.folder_path,
                    file_name=f"{self.item_name}_taken_audio.wav"
                )

                # 更新数据库
                update_taken(
                    item_name=self.item_name,
                    taken_photo_path=self.photo_path,
                    taken_audio_path=self.audio_path
                )
                print(f"Updated taken photo: {self.photo_path}, audio: {self.audio_path}")
            else:
                print("No item selected for take operation!")

            self.manager.current_item = None
            self.reset()

            self.manager.current = "choose_interact_type"

        
