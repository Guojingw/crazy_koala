from PIL import Image

image_path = image_path = "C:\Users\yangm\HRI2025\crazy_koala\data\test\test_deposit_photo.jpg"
  # 替换为图片路径
with Image.open(image_path) as img:
    print(f"Image Size: {img.size} (Width x Height)")
