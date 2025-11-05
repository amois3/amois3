"""Image optimization service."""
import logging
import base64
from io import BytesIO
from PIL import Image

from config import settings

logger = logging.getLogger(__name__)


class ImageOptimizer:
    """Optimize images for OpenAI API to save costs."""

    def __init__(self):
        self.max_size = settings.max_image_size
        self.quality = settings.image_quality

    def optimize_and_encode(self, image_bytes: bytes) -> str:
        """
        Optimize image and encode to base64.

        Args:
            image_bytes: Raw image bytes

        Returns:
            Base64 encoded optimized image
        """
        try:
            # Open image
            image = Image.open(BytesIO(image_bytes))

            # Convert to RGB if necessary
            if image.mode in ("RGBA", "P", "LA"):
                # Create white background
                background = Image.new("RGB", image.size, (255, 255, 255))
                if image.mode == "P":
                    image = image.convert("RGBA")
                background.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
                image = background
            elif image.mode != "RGB":
                image = image.convert("RGB")

            # Resize if too large
            if max(image.size) > self.max_size:
                ratio = self.max_size / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)
                logger.info(f"Resized image from {image.size} to {new_size}")

            # Save to bytes with compression
            output = BytesIO()
            image.save(output, format="JPEG", quality=self.quality, optimize=True)
            optimized_bytes = output.getvalue()

            # Calculate compression ratio
            original_size = len(image_bytes)
            optimized_size = len(optimized_bytes)
            ratio = (1 - optimized_size / original_size) * 100
            logger.info(f"Image compressed: {original_size} -> {optimized_size} bytes ({ratio:.1f}% reduction)")

            # Encode to base64
            return base64.b64encode(optimized_bytes).decode("utf-8")

        except Exception as e:
            logger.error(f"Failed to optimize image: {e}")
            # Fallback: just encode original
            return base64.b64encode(image_bytes).decode("utf-8")

    def estimate_tokens(self, image_bytes: bytes) -> int:
        """
        Estimate number of tokens for image.

        Based on OpenAI's pricing:
        - Low detail: 85 tokens
        - High detail: 170 tokens + additional based on image size
        """
        try:
            image = Image.open(BytesIO(image_bytes))
            width, height = image.size

            # High detail calculation
            # Images are scaled to fit within 2048x2048, then divided into 512x512 tiles
            scale = min(2048 / max(width, height), 1.0)
            scaled_width = int(width * scale)
            scaled_height = int(height * scale)

            tiles_width = (scaled_width + 511) // 512
            tiles_height = (scaled_height + 511) // 512
            total_tiles = tiles_width * tiles_height

            # Each tile is 170 tokens, plus 85 base tokens
            estimated_tokens = 85 + (170 * total_tiles)

            return estimated_tokens

        except Exception as e:
            logger.error(f"Failed to estimate tokens: {e}")
            return 765  # Average estimate
