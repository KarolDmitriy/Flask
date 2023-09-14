import os
import argparse
import requests
import concurrent.futures
import asyncio
import aiohttp
import time

# Создаем папку "images" в корневом каталоге программы, если она не существует
if not os.path.exists("images"):
    os.makedirs("images")

def download_image(url):
    try:
        # Загружаем изображение по указанному URL и замеряем время начала загрузки
        start_time = time.time()
        response = requests.get(url)
        if response.status_code == 200:
            # Определяем имя файла, сохраняем изображение и выводим время загрузки
            image_name = os.path.join("images", os.path.basename(url))
            with open(image_name, 'wb') as file:
                file.write(response.content)
            end_time = time.time()  # Замеряем время окончания загрузки
            download_time = end_time - start_time  # Вычисляем время загрузки
            total_time = end_time - program_start_time  # Вычисляем общее время работы программы
            print(f"Downloaded {image_name} in {download_time:.2f} seconds")
            print(f"Total time: {total_time:.2f} seconds\n")
        else:
            # В случае неудачной загрузки выводим сообщение об ошибке
            print(f"Failed to download {url}")
    except Exception as e:
        # В случае возникновения исключения выводим сообщение об ошибке
        print(f"Error downloading {url}: {str(e)}")

async def async_download_image(session, url):
    try:
        # Замеряем время начала загрузки
        start_time = time.time()
        async with session.get(url) as response:
            if response.status == 200:
                # Определяем имя файла, сохраняем изображение и выводим время загрузки
                image_name = os.path.join("images", os.path.basename(url))
                with open(image_name, 'wb') as file:
                    file.write(await response.read())
                end_time = time.time()  # Замеряем время окончания загрузки
                download_time = end_time - start_time  # Вычисляем время загрузки
                total_time = end_time - program_start_time  # Вычисляем общее время работы программы
                print(f"Downloaded {image_name} in {download_time:.2f} seconds")
                print(f"Total time: {total_time:.2f} seconds\n")
            else:
                # В случае неудачной загрузки выводим сообщение об ошибке
                print(f"Failed to download {url}")
    except Exception as e:
        # В случае возникновения исключения выводим сообщение об ошибке
        print(f"Error downloading {url}: {str(e)}")

# Замеряем время начала выполнения программы
program_start_time = time.time()

def main():
    parser = argparse.ArgumentParser(description="Download images from a list of URLs.")
    parser.add_argument("urls", nargs="+", help="List of URLs to download images from.")
    args = parser.parse_args()
    urls = args.urls

    # Многопоточный подход
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Используем ThreadPoolExecutor для создания нескольких потоков и загрузки изображений параллельно
        thread_results = list(executor.map(download_image, urls))

    # Многопроцессорный подход
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Используем ProcessPoolExecutor для создания нескольких процессов и загрузки изображений параллельно
        process_results = list(executor.map(download_image, urls))

    # Асинхронный подход
    async def async_main():
        async with aiohttp.ClientSession() as session:
            # Используем aiohttp и asyncio для асинхронной загрузки изображений
            for url in urls:
                await async_download_image(session, url)

    asyncio.run(async_main())

if __name__ == "__main__":
    main()
