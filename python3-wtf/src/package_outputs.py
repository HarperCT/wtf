import tempfile
import os
import shutil
import time
import datetime
import logging
logger = logging.getLogger(__name__)


dt_object = datetime.datetime.fromtimestamp(time.time())
human_readable_datetime = dt_object.strftime("%Y-%m-%d-%H:%M:%S")
archive_name = f"{human_readable_datetime}_wtf_output" 


def archive_outputs(outputs: list[tuple[str, str]], destination: str = None):
    with tempfile.TemporaryDirectory() as temp_dir:
        for output in outputs:
            with open(os.path.join(temp_dir, f"{output[0]}.txt"), 'w') as file:
                top_out = output[1][0]
                file.write(top_out)
        shutil.make_archive(archive_name, "zip", temp_dir)
        try:
            if destination:
                shutil.move(archive_name + ".zip", destination)
        except Exception as e:
            logger.error("Failed to move file to destination. Leaving it where it is")
