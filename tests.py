import unittest
import os
import json
import storage

class TestBookStorage(unittest.TestCase):
    
    def setUp(self):
        # Создаем чистый файл перед каждым тестом
        if os.path.exists(storage.DATA_FILE):
            os.remove(storage.DATA_FILE)

    def tearDown(self):
        # Убираем за собой
        if os.path.exists(storage.DATA_FILE):
            os.remove(storage.DATA_FILE)

    def test_add_and_load(self):
        storage.add_book("Война и мир", "Толстой", 1869)
        books = storage.load_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["title"], "Война и мир")

    def test_invalid_year(self):
        with self.assertRaises(ValueError):
            storage.add_book("Книга", "Автор", "не_число")

    def test_empty_title(self):
        with self.assertRaises(ValueError):
            storage.add_book("", "Автор", 2000)

    def test_filtering(self):
        storage.add_book("Python Crash Course", "Eric Matthes", 2015)
        storage.add_book("Clean Code", "Robert Martin", 2008)
        
        result = storage.filter_books("Python")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["author"], "Eric Matthes")

    def test_boundary_year(self):
        # Граничный случай: год 0 или 2026
        storage.add_book("Old Book", "Unknown", 0)
        books = storage.load_books()
        self.assertEqual(books[0]["year"], 0)

if __name__ == "__main__":
    unittest.main()