"""
Instagram Post — Quote Template — Design 2
Style: Plain black background, centered branding (small),
       large italic Quote text + subtitle (author).
Optimized for 1080x1350 (4:5) ratio.
"""

from PIL import Image, ImageDraw
from features.canvas_feature.canvas import create_canvas
from features.canvas_feature.text_utils import load_font, wrap_text, draw_text_block, get_text_height


class QuoteDesign2:
    def __init__(self, ratio: dict, content: dict):
        self.width = ratio["width"]
        self.height = ratio["height"]
        self.content = content

    def render(self) -> Image.Image:
        # --- Background: Plain Black ---
        img = create_canvas(self.width, self.height, "#000000")
        draw = ImageDraw.Draw(img)

        text_white = "#FFFFFF"
        center_x = self.width // 2

        # --- Branding: 'guizot labs' (Centered, small) ---
        brand_font_bold = load_font("poppins_semibold", 46)
        brand_font_reg = load_font("poppins_regular", 46)

        brand_bold_text = "guizot"
        brand_reg_text = "labs"
        spacing = 6

        brand_bold_w = draw.textlength(brand_bold_text, font=brand_font_bold)
        brand_reg_w = draw.textlength(brand_reg_text, font=brand_font_reg)
        total_brand_w = brand_bold_w + spacing + brand_reg_w
        brand_x = center_x - total_brand_w // 2
        brand_y = 80

        draw.text((brand_x, brand_y), brand_bold_text, fill=text_white, font=brand_font_bold)
        draw.text((brand_x + brand_bold_w + spacing, brand_y), brand_reg_text, fill=text_white, font=brand_font_reg)

        # --- Quote Text (large, italic, centered, using cta_text field) ---
        cta_text = self.content.get("cta_text", "Your Quote Text Here")
        
        # Add quotation marks if they aren't already there
        if not cta_text.startswith('"') and not cta_text.startswith('“'):
            cta_text = f'"{cta_text}"'
            
        cta_font = load_font("poppins_mediumitalic", 72)
        text_area_width = self.width - 180
        cta_lines = wrap_text(cta_text, cta_font, text_area_width)
        cta_height = get_text_height(cta_lines, cta_font, line_spacing=12)
        
        # --- Subtitle / Author (centered, below quote) ---
        subtitle_text = self.content.get("subtitle", "")
        
        # Add em dash if missing
        if subtitle_text and not subtitle_text.startswith("-") and not subtitle_text.startswith("—"):
             subtitle_text = f"— {subtitle_text}"
             
        subtitle_font = load_font("poppins_regular", 38)

        if subtitle_text:
            subtitle_lines = wrap_text(subtitle_text, subtitle_font, text_area_width)
            subtitle_height = get_text_height(subtitle_lines, subtitle_font, line_spacing=8)
        else:
            subtitle_lines = []
            subtitle_height = 0

        # --- Vertical layout: center the content block ---
        content_top = 160
        footer_y = self.height - 130

        gap_cta_subtitle = 40 if subtitle_text else 0
        total_content_h = cta_height + gap_cta_subtitle + subtitle_height
        available_h = footer_y - content_top
        start_y = content_top + (available_h - total_content_h) // 2

        current_y = start_y
        
        # Draw Quote text
        draw_text_block(
            draw, cta_lines, cta_font,
            x=90, y=current_y,
            color=text_white, line_spacing=12,
            align="center", max_width=text_area_width,
        )
        current_y += cta_height + gap_cta_subtitle

        # Draw subtitle / author
        if subtitle_lines:
            draw_text_block(
                draw, subtitle_lines, subtitle_font,
                x=90, y=current_y,
                color=text_white, line_spacing=8,
                align="center", max_width=text_area_width,
            )

        # --- Handle (bottom center) ---
        handle_font = load_font("poppins_regular", 32)
        handle_text = "@glabs.ai"
        handle_w = draw.textlength(handle_text, font=handle_font)
        draw.text((center_x - handle_w // 2, footer_y), handle_text, fill=text_white, font=handle_font)

        return img
