BASE_DIR = ''
CACHED_QUERIES = dict()


def set_base_dir(directory_name: str):
    global BASE_DIR
    if not directory_name.endswith('/'):
        raise Exception('Directory name must end with "/"')
    BASE_DIR = directory_name


def read(query_name: str, file_extension: str = 'sql') -> str:
    file_name = query_name + '.' + file_extension
    if file_name in CACHED_QUERIES:
        return CACHED_QUERIES[file_name]

    file = open(BASE_DIR + file_name, 'r')
    query = file.read()
    file.close()

    CACHED_QUERIES[file_name] = query

    return query


def clear_cache():
    global CACHED_QUERIES
    CACHED_QUERIES = dict()



class SQLReader:
    def __init__(self, directory_name: str = '', auto_clear: bool = False) -> None:
        """
        directory_name: directory with sql files
        auto_clear: don`t save queries in cache
        """
        if not directory_name.endswith('/'):
            raise Exception('Directory name must end with "/"')
        self.base_dir = directory_name
        self.cached_queries = dict()
        self.auto_clear = auto_clear
    
    def clear_cache(self):
        """Clear queries cache"""
        self.cached_queries = dict()

    def read(self, query_name: str, file_extension: str = 'sql') -> str:
        file_name = query_name + '.' + file_extension
        if file_name in self.cached_queries:
            return self.cached_queries[file_name]

        file = open(self.base_dir + file_name, 'r')
        query = file.read()
        file.close()

        if not self.auto_clear:
            self.cached_queries[file_name] = query

        return query




