from PIL import Image, ImageOps
from PIL.Image import Resampling
from pathlib import Path
from moviepy.editor import ImageSequenceClip
from show import create_folder, reset_attempt_counter, clear_folder


resample_method = Resampling.LANCZOS


def combine_images(left_image_path, right_image_path, output_path, fixed_size=(1200, 800)):
    try:
        left_image = Image.open(left_image_path)
        right_image = Image.open(right_image_path)

        # Размер для каждой из двух частей изображения
        single_size = (fixed_size[0] // 2, fixed_size[1])

        # Изменяем размер с сохранением пропорций и добавляем отступы для выравнивания
        left_image = ImageOps.pad(left_image, single_size, method=Image.Resampling.LANCZOS, color=(255, 255, 255))
        right_image = ImageOps.pad(right_image, single_size, method=Image.Resampling.LANCZOS, color=(255, 255, 255))

        # Создаем новое изображение для объединения
        combined_image = Image.new('RGB', fixed_size, color=(255, 255, 255))
        combined_image.paste(left_image, (0, 0))
        combined_image.paste(right_image, (single_size[0], 0))

        combined_image.save(output_path)
        # print(f"Комбинированное сохранено: {output_path}")
    except Exception as e:
        print(f"Error combining images: {e}")
        raise


def create_combined_images_sequence(original_labyrinth_path, attempts_folder, output_folder, fixed_size=(1200, 800)):
    create_folder(output_folder)

    # Получаем список файлов с попытками пользователя, отсортированный по имени (номер попытки)
    attempts_images = sorted(Path(attempts_folder).glob('attempt_*.png'), key=lambda p: int(p.stem.split('_')[1]))

    combined_images_paths = []

    for idx, attempt_image_path in enumerate(attempts_images):
        output_image_path = Path(output_folder) / f'combined_{idx}.png'
        combine_images(original_labyrinth_path, attempt_image_path, output_image_path, fixed_size=fixed_size)
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
    clip.write_videofile(output_video_path, codec='libx264')



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