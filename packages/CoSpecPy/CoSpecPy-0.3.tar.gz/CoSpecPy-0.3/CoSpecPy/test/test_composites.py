from CoSpecPy.composites import Composite
from CoSpecPy.download import DownloadHandler

print("Testing Composite")
test_aria2_download = DownloadHandler("aria2", 5, 10, "test_tmp")
test_aria2_download.clear_up()
test_aria2_download.download_example()

example_composite = Composite("example_composite")
example_composite.example_from_downloads()
