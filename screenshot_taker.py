import pyautogui
from pynput import mouse, keyboard
from PIL import Image, ImageDraw
import datetime
import os
import sys

# Load a cursor image
cursor_image = Image.open("cursor.png").convert("RGBA")
cursor_width, cursor_height = cursor_image.size

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"log_{timestamp}.txt"



def write_to_log(text):
    with open(log_filename, "a") as f:
        f.write(text)


def latex_figure(image_filename):
    return (
        r"""
\begin{figure}
    \centering
    \includegraphics[width=0.5\linewidth]{"""
        + image_filename
        + r"""}
    \caption{Caption}
    \label{fig:enter-label}
\end{figure}
"""
    )


def on_click(x, y, button, pressed):
    if pressed:
        # Get the current timestamp for the screenshot filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"

        # Capture the screenshot
        screenshot = pyautogui.screenshot(
            region=(x - 200 + 1920, y - 200, 400, 400), allScreens=True
        )  #

        # Convert the screenshot to a PIL image
        screenshot_pil = screenshot.convert("RGBA")

        # Paste the cursor image on the screenshot
        combined_image = Image.new("RGBA", screenshot_pil.size, (0, 0, 0, 0))
        combined_image.paste(screenshot_pil, (0, 0))  # Paste the screenshot
        combined_image.paste(
            cursor_image,
            (200 + 12 - cursor_width // 2, 200 + 18 - cursor_height // 2),
            cursor_image,
        )

        # Save the combined image
        combined_image.save(os.path.join(os.getcwd(), filename))
        print(f"Screenshot saved: {filename}")

        write_to_log(latex_figure(filename))

def on_press(key):
    if key == keyboard.Key.esc:  # Exit when the Esc key is pressed
        print("Exiting program.")
        mouse_listener.stop()
        sys.exit()
    else:
        print(key)
        try:
            write_to_log(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
                write_to_log(' ')
            else:
                write_to_log('\n{}\n'.format(key))

write_to_log(timestamp)

# Set up mouse and keyboard listeners
mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press)

mouse_listener.start()
keyboard_listener.start()

print("Listening for mouse clicks. Press Esc to exit.")

# Keep the program running
mouse_listener.join()
keyboard_listener.join()
