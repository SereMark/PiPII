import os
import tempfile
import asyncio
import unittest
from src.a1.a1_ex4 import read_file_async, merge_files_concurrently

class TestAsyncFileMerge(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Create a temporary directory for input/output files.
        self.test_dir = tempfile.TemporaryDirectory()
        self.dir_path = self.test_dir.name

    async def asyncTearDown(self):
        self.test_dir.cleanup()

    async def create_temp_file(self, filename, content):
        path = os.path.join(self.dir_path, filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return path

    async def test_read_file_async(self):
        content = "Line1\nLine2\nLine3\n"
        path = await self.create_temp_file("test1.txt", content)
        lines = await read_file_async(path)
        self.assertEqual(lines, ["Line1", "Line2", "Line3"])

    async def test_merge_files_concurrently_multiple_files(self):
        # Create three files with unsorted content.
        content1 = "banana\napple\n"
        content2 = "cherry\ndate\n"
        content3 = "fig\ngrape\n"
        file1 = await self.create_temp_file("file1.txt", content1)
        file2 = await self.create_temp_file("file2.txt", content2)
        file3 = await self.create_temp_file("file3.txt", content3)
        output_file = os.path.join(self.dir_path, "merged.txt")
        await merge_files_concurrently([file1, file2, file3], output_file)
        with open(output_file, 'r', encoding='utf-8') as f:
            merged_lines = [line.rstrip("\n") for line in f]
        expected_lines = sorted(["banana", "apple", "cherry", "date", "fig", "grape"])
        self.assertEqual(merged_lines, expected_lines)

    async def test_merge_files_concurrently_single_file(self):
        content = "zeta\nalpha\nbeta\n"
        file1 = await self.create_temp_file("single.txt", content)
        output_file = os.path.join(self.dir_path, "merged_single.txt")
        await merge_files_concurrently([file1], output_file)
        with open(output_file, 'r', encoding='utf-8') as f:
            merged_lines = [line.rstrip("\n") for line in f]
        expected_lines = sorted(["zeta", "alpha", "beta"])
        self.assertEqual(merged_lines, expected_lines)

    async def test_merge_files_overwrites_output(self):
        # Create an output file with initial content.
        content = "delta\nepsilon\n"
        file1 = await self.create_temp_file("file_over.txt", content)
        output_file = os.path.join(self.dir_path, "merged_over.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("old content")
        await merge_files_concurrently([file1], output_file)
        with open(output_file, 'r', encoding='utf-8') as f:
            merged_content = f.read()
        self.assertNotIn("old content", merged_content)

    def test_alphabetical_sorting(self):
        # Synchronous test for sorting using two files.
        async def inner():
            content1 = "delta\nalpha\n"
            content2 = "charlie\nbravo\n"
            file1 = await self.create_temp_file("file_a.txt", content1)
            file2 = await self.create_temp_file("file_b.txt", content2)
            output_file = os.path.join(self.dir_path, "merged_sort.txt")
            await merge_files_concurrently([file1, file2], output_file)
            with open(output_file, 'r', encoding='utf-8') as f:
                merged_lines = [line.rstrip("\n") for line in f]
            expected = sorted(["delta", "alpha", "charlie", "bravo"])
            self.assertEqual(merged_lines, expected)
        asyncio.run(inner())

    async def test_concurrent_reading(self):
        # Create several files and check that merge_files_concurrently merges them.
        files = []
        for i in range(5):
            content = f"line{i}a\nline{i}b\n"
            file_path = await self.create_temp_file(f"concurrent_{i}.txt", content)
            files.append(file_path)
        output_file = os.path.join(self.dir_path, "merged_concurrent.txt")
        await merge_files_concurrently(files, output_file)
        with open(output_file, 'r', encoding='utf-8') as f:
            merged_lines = [line.rstrip("\n") for line in f]
        expected_lines = []
        for i in range(5):
            expected_lines.extend([f"line{i}a", f"line{i}b"])
        self.assertEqual(merged_lines, sorted(expected_lines))

    async def test_trimming_newlines(self):
        # Verify that newlines are trimmed correctly.
        content = "line with newline\nanother line\n"
        file_path = await self.create_temp_file("trim.txt", content)
        lines = await read_file_async(file_path)
        self.assertEqual(lines, ["line with newline", "another line"])

    async def test_duplicate_lines(self):
        # Duplicate lines should all appear and be sorted.
        content1 = "apple\nbanana\napple\n"
        content2 = "banana\ncherry\n"
        file1 = await self.create_temp_file("dup1.txt", content1)
        file2 = await self.create_temp_file("dup2.txt", content2)
        output_file = os.path.join(self.dir_path, "merged_dup.txt")
        await merge_files_concurrently([file1, file2], output_file)
        with open(output_file, 'r', encoding='utf-8') as f:
            merged_lines = [line.rstrip("\n") for line in f]
        expected = sorted(["apple", "banana", "apple", "banana", "cherry"])
        self.assertEqual(merged_lines, expected)

    async def test_missing_file_raises_error(self):
        # When one input file is missing, the function should error out.
        file1 = await self.create_temp_file("exists.txt", "content\n")
        missing_file = os.path.join(self.dir_path, "nonexistent.txt")
        output_file = os.path.join(self.dir_path, "merged_error.txt")
        with self.assertRaises(TypeError):
            await merge_files_concurrently([file1, missing_file], output_file)

    async def test_empty_input_files(self):
        # With an empty list of input files, output should be an empty file.
        output_file = os.path.join(self.dir_path, "merged_empty.txt")
        await merge_files_concurrently([], output_file)
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertEqual(content, "")

if __name__ == '__main__':
    unittest.main()
