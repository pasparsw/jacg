import os
from logging import getLogger

from src.generators.python_code_generator import GeneratedContent
from src.utils import save_to_file

LOGGER = getLogger("GeneratedContentWriter")


class GeneratedContentWriter:
    def write(self, output_path: str, generated_content: GeneratedContent) -> None:
        LOGGER.info(f"Saving generated content to {output_path}")

        for path, content in generated_content.items():
            full_output_path: str = os.path.join(output_path, path)
            dir_path: str = os.path.dirname(full_output_path)

            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                with open(os.path.join(dir_path, "__init__.py"), 'w') as file:
                    file.write("")

            save_to_file(full_output_path, content)

        LOGGER.info("Saving of the generated content done")
