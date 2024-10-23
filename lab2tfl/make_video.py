from PIL import Image, ImageOps, ImageDraw, ImageFont
from PIL.Image import Resampling
from pathlib import Path
from moviepy.editor import ImageSequenceClip
from show import create_folder, reset_attempt_counter, clear_folder


resample_method = Resampling.LANCZOS


def combine_images(left_image_path, right_image_path, output_path, attempt_number, fixed_size=(2400, 1700)):
    try:
        # Открываем изображения и конвертируем в RGB
        left_image = Image.open(left_image_path).convert("RGB")
        right_image = Image.open(right_image_path).convert("RGB")

        # Размер для каждой из двух частей изображения
        single_width = fixed_size[0] // 2
        single_height = fixed_size[1] - 200  # 200 пикселей для подписей сверху
        single_size = (single_width, single_height)

        # Изменяем размер с сохранением пропорций и добавляем отступы для выравнивания
        left_image = ImageOps.pad(left_image, single_size, method=resample_method, color=(255, 255, 255))
        right_image = ImageOps.pad(right_image, single_size, method=resample_method, color=(255, 255, 255))

        # Создаём новое изображение для объединения
        combined_image = Image.new('RGB', fixed_size, color=(255, 255, 255))
        combined_image.paste(left_image, (0, 200))  # Смещение по вертикали для подписи
        combined_image.paste(right_image, (single_width, 200))

        # Добавляем подписи
        draw = ImageDraw.Draw(combined_image)

        # Определяем шрифт и размер. Укажите путь к вашему шрифту .ttf, если требуется
        try:
            # Для Windows
            font = ImageFont.truetype("arial.ttf", size=60)
        except IOError:
            try:
                # Для Unix/Linux
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=60)
            except IOError:
                # Используем стандартный шрифт, если внешние шрифты не найдены
                font = ImageFont.load_default()

        # Тексты
        left_text = "Исходный лабиринт"
        right_text = f"Попытка {attempt_number}"

        # Вычисляем размеры текста с помощью textbbox
        left_bbox = draw.textbbox((0, 0), left_text, font=font)
        right_bbox = draw.textbbox((0, 0), right_text, font=font)
        left_text_width = left_bbox[2] - left_bbox[0]
        left_text_height = left_bbox[3] - left_bbox[1]
        right_text_width = right_bbox[2] - right_bbox[0]
        right_text_height = right_bbox[3] - right_bbox[1]

        # Определяем положение текста (центр над каждым изображением)
        left_text_position = ((single_width - left_text_width) // 2, 50)  # 50 пикселей от верхнего края
        right_text_position = (single_width + (single_width - right_text_width) // 2, 50)

        # Добавляем основной текст без фона
        text_color = "purple"  # Цвет текста
        draw.text(left_text_position, left_text, font=font, fill=text_color)
        draw.text(right_text_position, right_text, font=font, fill=text_color)

        # Сохраняем объединённое изображение в формате PNG для сохранения качества
        combined_image.save(output_path, format='PNG')
        print(f"Combined image saved: {output_path}")
    except Exception as e:
        print(f"Ошибка создания комбинированного: {e}")
        raise


def create_combined_images_sequence(original_labyrinth_path, attempts_folder, output_folder, fixed_size=(2400, 1600)):
    create_folder(output_folder)

    # Получаем список файлов с попытками пользователя, отсортированный по имени (номер попытки)
    attempts_images = sorted(Path(attempts_folder).glob('attempt_*.png'), key=lambda p: int(p.stem.split('_')[1]))

    combined_images_paths = []

    for idx, attempt_image_path in enumerate(attempts_images):
        output_image_path = Path(output_folder) / f'combined_{idx}.png'
        if idx == len(attempts_images) - 1:
            idx -= 1
        combine_images(original_labyrinth_path, attempt_image_path, output_image_path, attempt_number=idx + 1, fixed_size=fixed_size)
        combined_images_paths.append(str(output_image_path))

    return combined_images_paths


def create_video_from_images(image_files, output_video_path, fps=1):
    if not image_files:
        raise ValueError("Список изображений пуст. Невозможно создать видео.")

    # Проверяем, что все изображения имеют одинаковый размер
    first_image = Image.open(image_files[0])
    width, height = first_image.size
    for img_path in image_files[1:]:
        img = Image.open(img_path)
        if img.size != (width, height):
            raise ValueError(f"Изображение {img_path} имеет размер {img.size}, отличающийся от первого изображения {(width, height)}.")

    # Загружаем изображения и создаем видео
    clip = ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile(output_video_path, codec='libx264', bitrate='5000k')



def create_labyrinth_video(original_labyrinth_path, attempts_folder, output_folder, output_video_path):
    create_folder(Path(output_video_path).parent)

    # Создаем последовательность объединенных изображений
    combined_images_paths = create_combined_images_sequence(
        original_labyrinth_path,
        attempts_folder,
        output_folder
    )

    if not combined_images_paths:
        print("Нет попыток для создания видео.")
        return

    # Создаем видео из изображений
    create_video_from_images(combined_images_paths, output_video_path, fps=1)  # fps=1, чтобы каждое изображение показывалось 1 секунду


def give_me_video():
    create_folder(Path('../videos/labyrinth_attempts.mp4').parent)
    create_labyrinth_video(
        '../images/labyrinth.png',
        '../images/attempts',
        '../images/combined',
        '../videos/labyrinth_attempts.mp4'
    )
    reset_attempt_counter()
    clear_folder('../images/attempts')
    clear_folder('../images/combined')