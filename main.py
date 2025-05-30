import os
import time
import requests
from datetime import datetime
from typing import Optional


def create_folder(folder_path: str) -> None:
    """
    Create a folder if it does not already exist.

    Args:
        folder_path (str): Path to the folder.
    """
    os.makedirs(folder_path, exist_ok=True)


def generate_timestamp_filename(folder_path: str, extension: str = ".jpg") -> str:
    """
    Generate a high-precision timestamped filename (down to microseconds).

    Args:
        folder_path (str): Directory where the file will be saved.
        extension (str): File extension to use.

    Returns:
        str: Full file path with timestamp-based filename.
    """
    timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    filename: str = f"{timestamp}{extension}"
    return os.path.join(folder_path, filename)


def download_image(url: str, headers: dict, save_path: str) -> Optional[str]:
    """
    Download an image from a URL and save it to a specified path.

    Args:
        url (str): The image URL.
        headers (dict): HTTP headers to include in the request.
        save_path (str): Local file path to save the image.

    Returns:
        Optional[str]: Path to the saved image if successful, else None.
    """
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                file.write(response.content)
            return save_path
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error downloading image: {e}")
    return None


def main() -> None:
    """
    Continuously download images until stopped by the user.
    """
    url: str = "https://thispersondoesnotexist.com/"
    folder: str = "Images"
    headers: dict = {"User-Agent": "Mozilla/5.0"}

    create_folder(folder)
    print("Starting continuous download. Press Ctrl+C to stop.\n")

    try:
        while True:
            filename: str = generate_timestamp_filename(folder)
            saved_path: Optional[str] = download_image(url, headers, filename)

            if saved_path:
                print(f"[✓] Saved: {saved_path}")
            else:
                print("[!] Download failed.")


    except KeyboardInterrupt:
        print("\nDownload stopped by user. Exiting gracefully.")


# Run the script
if __name__ == "__main__":
    main()
