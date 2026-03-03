"""
Instagram Story — Hook Template — Design 2
Style: Minimalist Dark, left-aligned hook text,
       'guizot labs' branding in top-left.
Optimized for 1080x1920 (9:16) ratio.
"""

from PIL import Image, ImageDraw
from src.features.canvas_feature.canvas import create_canvas
from src.features.canvas_feature.text_utils import load_font, wrap_text, draw_text_block, get_text_height


class HookDesign2:
    def __init__(self, ratio: dict, content: dict):
        self.width = ratio["width"]
        self.height = ratio["height"]
        self.content = content

    def render(self) -> Image.Image:
        # --- Background: Deep Black ---
        bg_color = "#000000"
        img = create_canvas(self.width, self.height, bg_color)
        draw = ImageDraw.Draw(img)

        text_white = "#FFFFFF"

        # --- Branding: 'guizot labs' (Top-Left) ---
        padding_x = 90
        padding_y = 150
        
        brand_font_bold = load_font("poppins_semibold", 48)
        draw.text((padding_x, padding_y), "guizot", fill=text_white, font=brand_font_bold)
        
        brand_w_guizot = draw.textlength("guizot", font=brand_font_bold)
        brand_font_reg = load_font("poppins_regular", 48)
        draw.text((padding_x + brand_w_guizot + 10, padding_y), "labs", fill=text_white, font=brand_font_reg)

        # --- Separator Line ---
        draw.line([padding_x, padding_y + 100, self.width - padding_x, padding_y + 100], fill=text_white, width=1)

        # --- Hook text (Center-aligned) ---
        hook_text = self.content.get("hook_text", "Your Hook Text Here")

        text_area_width = self.width - 200
        
        font_size = 76
        font = load_font("poppins_semibold", font_size)
        lines = wrap_text(hook_text, font, text_area_width)

        text_height = get_text_height(lines, font, line_spacing=24)
        start_y = (self.height - text_height) // 2

        draw_text_block(
            draw,
            lines,
            font,
            x=padding_x,
            y=start_y,
            color=text_white,
            line_spacing=24,
            align="left",
        )

        # --- Footer Text ---
        footer_font = load_font("poppins_regular", 38)
        draw.text((padding_x, self.height - 220), "guizot.framer.ai", fill=text_white, font=footer_font)

        # --- Subtle decoration: Corner accents ---
        accent_len = 50
        accent_thickness = 3
        # Bottom-right corner
        draw.line([self.width - 90, self.height - 170 - accent_len, self.width - 90, self.height - 170], fill=text_white, width=accent_thickness)
        draw.line([self.width - 90 - accent_len, self.height - 170, self.width - 90, self.height - 170], fill=text_white, width=accent_thickness)

        return img
