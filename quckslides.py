import random
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageColor
import textwrap

THIS_DIR = Path(__file__).parent.resolve()
IMAGE_DIR = THIS_DIR / 'template/bg_man/'
OUT_DIR = THIS_DIR / 'output'
if not OUT_DIR.exists():
    Path.mkdir(OUT_DIR)
SIZE = 1024, 1024

FONT = 'Rubik.ttf'
FONT_B = 'Rubik-Bold.ttf'


def color(c):
    return ImageColor.getcolor(c, 'RGB')


COLORS = (color('#FA8072'), color('#E9967A'),
          color('#F08080'), color('#FFA07A'),
          color('#FFB6C1'), color('#FF8C00'),
          color('#DA70D6'), color('#9932CC'),
          color('#6A5ACD'), color('#D2691E'),
          color('#00FA9A'), color('#808000'),
          color('#20B2AA'), color('#00FFFF'),
          color('#6495ED'), color('#696969'),
          )


COLORS_FONT = (color('#8B0000'), color('#B22222'),
               color('#CD5C5C'), color('#DC143C'),
               color('#DB7093'), color('#FF6347'),
               color('#9370DB'), color('#800080'),
               color('#483D8B'), color('#8B4513'),
               color('#3CB371'), color('#9ACD32'),
               color('#8FBC8F'), color('#AFEEEE'),
               color('#7B68EE'), color('#2F4F4F'),
               )


def get_fonts(min_size, max_size):
    font = ImageFont.truetype(FONT, size=random.randint(min_size, max_size))
    font_b = ImageFont.truetype(FONT_B, size=random.randint(min_size, max_size))
    return font, font_b


def get_fit_font(drawer, line, x_start, y_start):
    font_min = 50
    font_max = 80
    font = random.choice(get_fonts(font_min, font_max))
    while (drawer.textbbox((x_start, y_start), line, font=font)[2] > SIZE[0] or
           drawer.textbbox((x_start, y_start), line, font=font)[3] > SIZE[1]):
        font_min -= 2
        font_max -= 2
        if font_min <= 0 or font_max <= 0:
            break
        font = random.choice(get_fonts(font_min, font_max))

    return font


def draw_something(drawer):
    opacity = random.randint(96, 192)
    if random.random() > 0.5:
        # Draw rectangle
        x_min = random.randint(0, int(SIZE[0] / 1.25))
        y_min = random.randint(0, int(SIZE[1] / 1.25))
        x_max = random.randint(x_min + random.randint(int(SIZE[0] / 50), int(SIZE[0] / 20)), SIZE[0])
        y_max = random.randint(y_min + random.randint(int(SIZE[1] / 50), int(SIZE[1] / 20)), SIZE[1])
        drawer.rectangle(((x_min, y_min), (x_max, y_max)),
                         fill=random.choice(COLORS) + (opacity,))
    else:
        # Draw ellipse
        x_min = random.randint(0, int(SIZE[0] / 1.25))
        y_min = random.randint(0, int(SIZE[1] / 1.25))
        x_max = random.randint(x_min, SIZE[0])
        y_max = random.randint(y_min, SIZE[1])
        drawer.ellipse(((x_min, y_min), (x_max, y_max)),
                       fill=random.choice(COLORS) + (opacity,))


def draw_text(drawer, text):
    """
    :param drawer: ImageDraw
    :param text: tuple with strings, max length two strings
    :return: no return
    """
    # Check does slide have topic description
    if len(text) > 1:
        # Draw topic name text
        line = text[0]
        x_start = random.randint(int(SIZE[0] / 20), int(SIZE[0] / 3))
        y_start = random.randint(int(SIZE[1] / 20), int(SIZE[1] / 5))
        font = get_fit_font(drawer, line, x_start, y_start)

        drawer.text((x_start, y_start),
                    line,
                    font=font,
                    fill=random.choice(COLORS_FONT))
        # Draw topic description text
        x_start = random.randint(int(SIZE[0] / 20), int(SIZE[0] / 3))
        y_start = random.randint(int(SIZE[1] / 3), int(SIZE[1] / 2))
        lines = textwrap.wrap(text[1], width=30)
        for line in lines:
            font = get_fit_font(drawer, line, x_start, y_start)

            _, _, line_width, line_height = drawer.textbbox((0, 0), line, font=font)
            drawer.text((x_start, y_start),
                        line,
                        font=font,
                        fill=random.choice(COLORS_FONT))
            y_start += line_height
    else:
        # Draw slide without topic description
        line = text[0]
        x_start = random.randint(int(SIZE[0] / 20), int(SIZE[0] / 3))
        y_start = random.randint(int(SIZE[1] / 10), int(SIZE[1] / 2))
        font = get_fit_font(drawer, line, x_start, y_start)

        drawer.text((x_start, y_start),
                    text[0],
                    font=font,
                    fill=random.choice(COLORS_FONT))


def create_slides(input_texts):
    images = [Image.open(IMAGE_DIR / f).convert('RGB').resize(SIZE)
              for f in os.listdir(IMAGE_DIR)
              ]

    res_images = []

    for text in input_texts:
        res_images.append(random.choice(images).copy())
        drawer = ImageDraw.Draw(res_images[-1], "RGBA")
        for _ in range(random.randint(3, 7)):
            if random.random() > 0.5:
                # Do draw
                draw_something(drawer)
        # Draw texts by drawer
        draw_text(drawer, text)

    pdf_path = OUT_DIR / "QuickSlides.pdf"
    res_images[0].save(
        pdf_path, "PDF", resolution=100.0, save_all=True, append_images=res_images[1:]
    )
