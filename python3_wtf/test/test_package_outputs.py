import os
import zipfile
import tempfile

from python3_wtf.package_outputs import archive_outputs, archive_name


def test_archive_outputs_creates_zip_file_and_moves_it():
    # Sample input: list of (filename, [content])
    outputs = [("test1", ["line 1\nline 2"]), ("test2", ["line A\nline B"])]

    with tempfile.TemporaryDirectory() as temp_output_dir:
        archive_outputs(outputs, destination=temp_output_dir)
        zip_path = os.path.join(temp_output_dir, f"{archive_name}.zip")
        assert os.path.isfile(zip_path), "ZIP archive was not created in destination."
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zip_contents = zf.namelist()
            assert "test1.txt" in zip_contents
            assert "test2.txt" in zip_contents
            with zf.open("test1.txt") as file:
                content = file.read().decode()
                assert "line 1" in content


def test_archive_outputs_handles_missing_destination():
    outputs = [("testfile", ["data"])]
    archive_outputs(outputs)
    zip_filename = f"{archive_name}.zip"
    assert os.path.exists(zip_filename)
    os.remove(zip_filename)


def test_archive_outputs_creates_zip_file_with_indexed_files():
    # Sample input: list of (filename, [content])
    outputs = [
        ("test1", ["line 1\nline 2"]),
        ("test1", ["line 1\nline 2"]),
        ("test2", ["line A\nline B"]),
    ]
    with tempfile.TemporaryDirectory() as temp_output_dir:
        archive_outputs(outputs, destination=temp_output_dir)
        zip_path = os.path.join(temp_output_dir, f"{archive_name}.zip")
        assert os.path.isfile(zip_path), "ZIP archive was not created in destination."
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zip_contents = zf.namelist()
            assert "test1.txt" in zip_contents
            assert "test1_0.txt" in zip_contents
            assert "test2.txt" in zip_contents
            with zf.open("test1.txt") as file:
                content = file.read().decode()
                assert "line 1" in content
