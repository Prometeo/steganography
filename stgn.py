import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import numpy as np
import subprocess


def steg_write(
    image_path: str,
    message: str,
    output_path: str = "edited_image.png",
    spacing: int = 10,
) -> None:
    # check the image is a png
    file = subprocess.run(
        [f"file {image_path}"], shell=True, capture_output=True, text=True
    )
    if file.stdout:
        result = file.stdout.partition(":")[2]
        if "PNG" not in result:
            raise ValueError("The input image must be a PNG file")
    else:
        raise ValueError(file.stderr)

    # open the image using PIL
    img = Image.open(image_path)
    pixel_array = np.array(img)

    # convert unicode characters in message into integers
    message_values = [ord(char) for char in message]

    image_shape = pixel_array.shape

    pixel_list = pixel_array.flatten().tolist()
    if len(message) * spacing > len(pixel_list):
        raise ValueError(
            "The message length and spacing is larger than the number of pixels in the image"
        )

    # save indices where the message will be hidden
    idx_list = [idx * spacing for idx in range(len(message_values))]

    # replace pixel values with message values
    for idx, char in zip(idx_list, message_values):
        pixel_list[idx] = char

    # reshape list back to image shape
    edited_array = np.array(pixel_list).reshape(image_shape).astype(np.uint8)

    # save the edited image in a lossless format, png
    edited_img = Image.fromarray(edited_array)
    edited_img.save(output_path)

    # message length is needed as an input to decipher message
    print(f"Message Length: {len(message):,}")
    print("Image Saved!")


def steg_read(image_path: str, message_length: int, spacing: int = 10) -> str:
    # open the image using PIL
    img = Image.open(image_path)
    pixel_array = np.array(img)

    pixel_list = pixel_array.flatten().tolist()

    # retrieve indices where the message will be hidden
    idx_list = [idx * spacing for idx in range(message_length)]

    # extract hidden message values
    hidden_values = [pixel_list[idx] for idx in idx_list]

    # convert ascii values to unicode
    chars = [chr(value) for value in hidden_values]

    return "".join(chars)


def main():
    message = """Yo el Supremo Dictador de la República: Ordeno que al acaecer mi muerte mi cadáver sea decapitado; la cabeza puesta en una pica por tres días en la Plaza de la República donde se convocará al pueblo al son de las campanas echadas al vuelo."""
    print(f"original message: \n{message}")
    steg_write("images/example_picture.png", message)
    retrieved_message = steg_read("edited_image.png", len(message))
    print(retrieved_message)
    plt.imshow(mpimg.imread("edited_image.png"))
    plt.show()


if __name__ == "__main__":
    main()
