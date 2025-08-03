import logging
import thread_runner
import plugin_finder
import package_outputs

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

plugin_detector = plugin_finder.PluginDetector()
thread_runner = thread_runner.ThreadRunner(timeout=5, plugins=plugin_detector.applicable_plugins)
outputs = thread_runner.run_threads()

package_outputs.archive_outputs(outputs, "/tmp")
