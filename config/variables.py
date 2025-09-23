from pathlib import Path

class Config:
    path_files = Path(__file__).parents[1]
    libs_files = path_files / 'modules' / 'utils'
    db_path = path_files / 'data' / 'books.db'