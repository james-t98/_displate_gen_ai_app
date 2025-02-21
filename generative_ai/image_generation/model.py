import replicate

class ImageGeneration():
    def __init__(self):
        pass

    def generate_image(self, prompt):
        output = replicate.run(
            "google/imagen-3-fast",
            input={
                "prompt": prompt,
                "aspect_ratio": "16:9",
                "safety_filter_level": "block_medium_and_above"
            }
        )
        return output