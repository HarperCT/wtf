import tempfile
import os
import shutil
import datetime
import logging
from pathlib import Path
from collections import defaultdict

logger = logging.getLogger(__name__)


def archive_outputs(
    outputs: list[tuple[str, tuple[str, str, bool]]],
    destination: str | Path = None
) -> Path:
    """
    Archives plugin outputs into a timestamped zip file.
    
    Args:
        outputs: List of (plugin_name, (stdout, stderr, timed_out)) tuples
        destination: Directory to save the archive (defaults to current dir)
    
    Returns:
        Path to the created archive file
    """
    # Generate timestamp at call time, not import time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    archive_name = f"{timestamp}_wtf_output"
    
    # Track duplicate plugin names for efficient numbering
    plugin_counts = defaultdict(int)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        for plugin_name, (stdout, stderr, timed_out) in outputs:
            # Handle duplicate plugin names efficiently
            count = plugin_counts[plugin_name]
            plugin_counts[plugin_name] += 1
            
            # Generate unique filename
            if count == 0:
                filename = f"{plugin_name}.txt"
            else:
                filename = f"{plugin_name}_{count}.txt"
            
            file_path = temp_path / filename
            
            try:
                # Write all output information, not just stdout
                with open(file_path, 'w', encoding='utf-8') as f:
                    # Write header with metadata
                    f.write(f"=== {plugin_name} Output ===\n")
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"Timed Out: {timed_out}\n")
                    f.write("=" * 50 + "\n\n")
                    
                    # Write stdout
                    if stdout:
                        f.write("=== STDOUT ===\n")
                        f.write(stdout)
                        if not stdout.endswith('\n'):
                            f.write('\n')
                        f.write("\n")
                    
                    # Write stderr if present
                    if stderr:
                        f.write("=== STDERR ===\n")
                        f.write(stderr)
                        if not stderr.endswith('\n'):
                            f.write('\n')
                    
                    # Add timeout warning if applicable
                    if timed_out:
                        f.write("\n=== WARNING ===\n")
                        f.write("This plugin timed out or encountered an error.\n")
                        f.write("Output may be incomplete.\n")
                        
            except IOError as e:
                logger.error(f"Failed to write output for {plugin_name}: {e}")
                continue
        
        # Create archive
        try:
            archive_base = shutil.make_archive(
                archive_name,
                "zip",
                temp_dir
            )
            archive_path = Path(archive_base)
            
            # Move to destination if specified
            if destination:
                dest_path = Path(destination)
                dest_path.mkdir(parents=True, exist_ok=True)
                final_path = dest_path / archive_path.name
                shutil.move(str(archive_path), str(final_path))
                logger.info(f"Archive created: {final_path}")
                return final_path
            else:
                logger.info(f"Archive created: {archive_path}")
                return archive_path
                
        except Exception as e:
            logger.error(f"Failed to create archive: {e}")
            raise
