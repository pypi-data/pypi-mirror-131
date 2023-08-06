# pylint: disable=too-many-lines
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=bare-except
# pylint: disable=line-too-long
'''
    Contains the general methods for manipulating directories.
'''

# import json
# from re import search
import time
import json
import traceback
import shutil
import os
from pathlib import Path
from threading import Thread
import logging
# import utils.string_utils as strUtils
import ftputil
from ftputil.error import FTPOSError
import colemen_string_utils as strUtils
import utils.objectUtils as obj
import utils.file_write as write
import utils.file as f
import utils.resources

logger = logging.getLogger(__name__)
_THREAD_GET_FILES_ARRAY = []


def create(path, dir_name=False, **kwargs):
    '''
        Create a directory or path of directories on the local machine or an FTP server.

        ----------

        Arguments
        -------------------------
        `path` {str}
            The path to create or a path to where it should create the dir_name directory
        [`dir_name`=False] {str}
            The name of the directory to create.

        Keyword Arguments
        -----------------
        [`ftp`=None] {obj}
            A reference to the ftputil object.

        Return {bool}
        ----------------------
        True upon success, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 11:33:50
        `memberOf`: dir
        `version`: 1.0
        `method_name`: create
    '''
    success = False
    ftp = obj.get_kwarg(["ftp"], None, None, **kwargs)
    if dir_name is not False:
        path = os.path.join(path, dir_name)

    if ftp is not None:
        try:
            if ftp.path.exists(path) is False:
                ftp.makedirs(path, exist_ok=True)
                success = True
        except ftputil.error.PermanentError as error:
            print(f"error: {str(error)}")
    else:
        if exists(path) is False:
            Path(path).mkdir(parents=True, exist_ok=True)
            if exists(path) is True:
                success = True
        else:
            success = True

    return success


def exists(file_path, **kwargs):
    '''
        Confirms that the directory file_path exists

        ----------

        Arguments
        -------------------------
        `file_path` {str}
            The path to confirm.

        Keyword Arguments
        -----------------
        [`ftp`=None] {obj}
            A reference to the ftputil object.

        Return {bool}
        ----------------------
        True if the directory exists, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 11:44:03
        `memberOf`: dir
        `version`: 1.0
        `method_name`: exists
    '''
    dir_exists = False
    ftp = obj.get_kwarg(["ftp"], None, None, **kwargs)

    if ftp is not None:
        dir_exists = exists_ftp(file_path, ftp)
    else:
        if os.path.isdir(file_path) is True:
            dir_exists = True

    return dir_exists


def exists_ftp(file_path, ftp):
    '''
        Checks if an FTP directory exists.

        ----------

        Arguments
        -------------------------
        `file_path` {str}
            The path to confirm.

        `ftp` {obj}
            A reference to the ftputil object.

        Return {bool}
        ----------------------
        True if the directory exists, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 11:59:05
        `memberOf`: dir
        `version`: 1.0
        `method_name`: exists_ftp
    '''
    dir_exists = False
    try:
        if ftp.exists(file_path):
            dir_exists = True
    except ftputil.error.PermanentError as error:
        print(f"error: {str(error)}")
    return dir_exists


def get_folders(search_path=False, **kwargs):
    '''
        Get all directories from the search_path.

        ----------

        Arguments
        -------------------------
        `search_path` {str|list}
            The search path or list of paths to iterate.\n
            This is the same as the keyword argument search_path,
            the kwarg is provided for consistency.

        Keyword Arguments
        -----------------
            [`search_path`=cwd] {str|list}
                The search path or list of paths to iterate.

            [`recursive`=True] {boolean}
                If True the path is iterated recursively

            [`exclude`=[]] {str|list}
                A string or list of strings, if the file path contains any of them,
                the directory is ignored.

            [`include`=[]] {str|list}
                A string or list of strings, if the file path does NOT contain any of them,
                the directory is ignored.

            [`paths_only`=False] {bool}
                If True, the returned value will be a list of directory paths.

            [`ftp`=None] {obj}
                A reference to the ftputil object.

        Return {list}
        ----------------------
        A list of dictionaries containing all matching directories.\n
        example:\n
            [{\n
                file_path:"beep/boop/bleep/blorp",\n
                dir_name:"blorp"\n
            },...]\n
        if paths_only = True:\n
            ["beep/boop/bleep/blorp",...]

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 12:17:24
        `memberOf`: dir
        `version`: 1.0
        `method_name`: get_folders
    '''
    dir_array = []
    if search_path is False:
        search_path = obj.get_kwarg(['search path', 'search'], os.getcwd(), (list, str), **kwargs)
    if isinstance(search_path, list) is False:
        search_path = [search_path]

    recursive = obj.get_kwarg(['recursive', 'recurse'], True, bool, **kwargs)

    include = obj.get_kwarg(['include'], [], (list, str), **kwargs)
    if isinstance(include, (str)):
        include = [include]

    exclude = obj.get_kwarg(['exclude', 'ignore', 'ignore array'], [], (list, str), **kwargs)
    if isinstance(exclude, (str)):
        exclude = [exclude]

    paths_only = obj.get_kwarg(['paths only', 'path only'], False, (bool), **kwargs)

    ftp = obj.get_kwarg(["ftp"], None, None, **kwargs)
    if ftp is not None:
        return get_folders_ftp(search_path, **kwargs)

    for path in search_path:
        # # pylint: disable=unused-variable
        for root, folders, files in os.walk(path):
            # print(folders)
            for current_dir in folders:
                if paths_only:
                    dir_array.append(os.path.join(root, current_dir))
                    continue
                dir_data = {}
                dir_data['dir_name'] = current_dir
                dir_data['file_path'] = os.path.join(root, current_dir)
                ignore = False
                if len(exclude) > 0:
                    if strUtils.parse.array_in_string(exclude, dir_data['file_path']) is True:
                        continue
                if len(include) > 0:
                    if strUtils.parse.array_in_string(include, dir_data['file_path']) is False:
                        continue
                # if ignore_array is not False:
                #     for x in ignore_array:
                #         if x in dir_data['file_path']:
                #             ignore = True

                # if ignore is False:

                dir_array.append(dir_data)

            if recursive is False:
                break
    return dir_array


def get_folders_ftp(search_path=False, **kwargs):
    '''
        Get all directories from the search_path.

        ----------

        Arguments
        -------------------------
        `search_path` {str|list}
            The search path or list of paths to iterate.\n
            This is the same as the keyword argument search_path,
            the kwarg is provided for consistency.

        Keyword Arguments
        -----------------
            [`search_path`=cwd] {str|list}
                The search path or list of paths to iterate.

            `ftp` {obj}
                A reference to the ftputil object.

            [`recursive`=True] {boolean}
                If True the path is iterated recursively

            [`exclude`=[]] {str|list}
                A string or list of strings, if the file path contains any of them,
                the directory is ignored.

            [`include`=[]] {str|list}
                A string or list of strings, if the file path does NOT contain any of them,
                the directory is ignored.

            [`paths_only`=False] {bool}
                If True, the returned value will be a list of directory paths.


        Return {list}
        ----------------------
        A list of dictionaries containing all matching directories.\n
        example:\n
            [{\n
                file_path:"beep/boop/bleep/blorp",\n
                dir_name:"blorp"\n
            },...]\n
        if paths_only = True:\n
            ["beep/boop/bleep/blorp",...]

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 12:31:27
        `memberOf`: dir
        `version`: 1.0
        `method_name`: get_folders_ftp
    '''
    dir_array = []
    if search_path is False:
        search_path = obj.get_kwarg(['search path', 'search'], os.getcwd(), (list, str), **kwargs)
    if isinstance(search_path, list) is False:
        search_path = [search_path]

    recursive = obj.get_kwarg(['recursive', 'recurse'], True, bool, **kwargs)

    include = obj.get_kwarg(['include'], [], (list, str), **kwargs)
    if isinstance(include, (str)):
        include = [include]

    exclude = obj.get_kwarg(['exclude', 'ignore', 'ignore array'], [], (list, str), **kwargs)
    if isinstance(exclude, (str)):
        exclude = [exclude]

    paths_only = obj.get_kwarg(['paths only', 'path only'], False, (bool), **kwargs)

    ftp = obj.get_kwarg(["ftp"], None, None, **kwargs)
    if ftp is None:
        logger.warning("No FTP obj reference provided.")
        return False

    # print(f"search_path: {search_path}")
    for path in search_path:
        # # pylint: disable=unused-variable
        for root, folders, files in ftp.walk(path):
            # print(folders)
            for current_dir in folders:
                if paths_only:
                    dir_array.append(os.path.join(root, current_dir))
                    continue
                dir_data = {}
                dir_data['dir_name'] = current_dir
                dir_data['file_path'] = os.path.join(root, current_dir)
                ignore = False
                if len(exclude) > 0:
                    if strUtils.parse.array_in_string(exclude, dir_data['file_path']) is True:
                        continue
                if len(include) > 0:
                    if strUtils.parse.array_in_string(include, dir_data['file_path']) is False:
                        continue

                dir_array.append(dir_data)

            if recursive is False:
                break
    return dir_array


def get_files(search_path=False, **kwargs):
    '''
        Get all files/data from the search_path.

        ----------

        Keyword Arguments
        -----------------
            [`search_path`=cwd] {str|list}
                The search path or list of paths to iterate.

            [`recursive`=True] {boolean}
                If True the path is iterated recursively

            [`ignore`=[]] {str|list}
                A term or list or terms to ignore if the file path contains any of them.

            [`extensions`=[]] {str|list}
                An extension or list of extensions that the file must have.

            [`threaded`=True] {bool}
                if True, the process is multi-threaded,
                this makes indexing much faster,
                but it can easily overwhelm a cpu depending upon the drive.

            `data_include` {str|list}
                The data to get for each file, the shorter this list the faster it will complete.
                By default it will get this:
                    ['file_name', 'extension', 'name_no_ext', 'dir_path', 'access_time',
                    'modified_time', 'created_time', 'size']
                so the list you provide will limit the amount of
                reading/formatting needed to gather data.
                Example:
                    ['modified_time','size']  will take ~0.000129939 seconds per file on an SSD

                    ['file_name', 'extension', 'name_no_ext', 'dir_path', 'access_time',
                    'modified_time', 'created_time', 'size']

                    will take ~0.000173600 seconds per file on an SSD,
                    it's not much but little things matter.. that's what she said.

        return
        ----------
        `return` {list}
            A list of dictionaries containing all matching files.
    '''
    file_array = []
    if search_path is False:
        search_path = obj.get_kwarg(['search path', 'search'], os.getcwd(), (str, list), **kwargs)
    if isinstance(search_path, list) is False:
        search_path = [search_path]

    threaded = obj.get_kwarg(['threaded', 'thread'], True, bool, **kwargs)
    recursive = obj.get_kwarg(['recursive', 'recurse'], True, bool, **kwargs)

    data_include = obj.get_kwarg(['data include'], [], (list, str), **kwargs)
    if isinstance(data_include, (str)):
        data_include = [data_include]

    # ignore_array = obj.get_kwarg(['ignore', 'ignore_array', 'exclude'], [], (str, list), **kwargs)
    exclude = obj.get_kwarg(['exclude', 'ignore', 'ignore array'], [], (list, str), **kwargs)
    if isinstance(exclude, (str)):
        exclude = [exclude]

    include = obj.get_kwarg(['include'], [], (list, str), **kwargs)
    if isinstance(include, (str)):
        include = [include]

    extension_array = strUtils.format.extension(
        obj.get_kwarg(['extensions', 'ext', 'extension'], [], (str, list), **kwargs))
    if isinstance(extension_array, (str)):
        extension_array = [extension_array]

    if threaded is True:
        for path in search_path:
            gft = GetFilesThreaded(path, recursive=recursive, data_include=data_include,
                                   exclude=exclude, include=include, extensions=extension_array)
            return gft.master()
    # print(json.dumps(extension_array, indent=4))
    for path in search_path:
        # pylint: disable=unused-variable
        for root, folders, files in os.walk(path):
            for file in files:
                file_data = f.get_data(os.path.join(root, file), include=data_include)
                if file_data is not None:
                    # ignore = False
                    # print(f"file_data['extension']: {file_data['extension']}")
                    if len(exclude) > 0:
                        if strUtils.parse.array_in_string(exclude, file_data['file_path']) is True:
                            continue

                    if len(include) > 0:
                        if strUtils.parse.array_in_string(include, file_data['file_path']) is False:
                            continue

                    if len(extension_array) > 0:
                        file_ext = strUtils.format.extension(file_data['extension'])
                        if file_ext not in extension_array:
                            continue

                    # if len(ignore_array) > 0:
                    #     for ignore_string in ignore_array:
                    #         if ignore_string in file_data['file_path']:
                    #             ignore = True

                    # if ignore is False:
                        # fd['file_hash'] = generateFileHash(fd['file_path'])
                    file_array.append(file_data)

            if recursive is False:
                break
        return file_array
        # path_files = index_files(path, extension_array, ignore_array, recursive)
        # file_array = path_files + file_array
    return file_array


class GetFilesThreaded:
    '''
        A class implementation of the get_files method.
        This allows it use threading.
    '''

    def __init__(self, search_path, **kwargs):
        self.threads = []
        self.file_array = []
        self.max_threads = 20
        self.search_path = search_path

        if search_path is False:
            self.search_path = obj.get_kwarg(
                ['search path', 'search'], os.getcwd(), (str, list), **kwargs)
        if isinstance(self.search_path, list) is False:
            self.search_path = [self.search_path]

        self.recursive = obj.get_kwarg(['recursive', 'recurse'], True, bool, **kwargs)

        self.data_include = obj.get_kwarg(['data include'], [], (list, str), **kwargs)
        if isinstance(self.data_include, (str)):
            self.data_include = [self.data_include]

        # ignore_array = obj.get_kwarg(
            # ['ignore', 'ignore_array', 'exclude'], [], (str, list), **kwargs)
        self.exclude = obj.get_kwarg(
            ['exclude', 'ignore', 'ignore array'], [], (list, str), **kwargs)
        if isinstance(self.exclude, (str)):
            self.exclude = [self.exclude]

        self.include = obj.get_kwarg(['include'], [], (list, str), **kwargs)
        if isinstance(self.include, (str)):
            self.include = [self.include]

        self.extension_array = strUtils.format.extension(
            obj.get_kwarg(['extensions', 'ext', 'extension'], [], (str, list), **kwargs))
        if isinstance(self.extension_array, (str)):
            self.extension_array = [self.extension_array]

    def remove_thread_by_id(self, thread_id):
        '''
            Removes an active thread from self.threads

            ----------

            Arguments
            -------------------------
            `thread_id` {str}
                The id of the thread to remove

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-19-2021 13:48:58
            `memberOf`: dir
            `version`: 1.0
            `method_name`: remove_thread_by_id
        '''
        threads = self.threads
        new_threads = []
        for thread in threads:
            if thread != thread_id:
                new_threads.append(thread)
        self.threads = new_threads

    def _get_data_thread(self, file_path):
        file_data = f.get_data(file_path, data_include=self.data_include)
        if file_data is not None:
            # ignore = False
            # print(f"file_data['extension']: {file_data['extension']}")
            if len(self.exclude) > 0:
                if strUtils.parse.array_in_string(self.exclude, file_data['file_path']) is True:
                    return

            if len(self.include) > 0:
                if strUtils.parse.array_in_string(self.include, file_data['file_path']) is False:
                    return

            if len(self.extension_array) > 0:
                file_ext = strUtils.format.extension(file_data['extension'])
                if file_ext not in self.extension_array:
                    return

        self.file_array.append(file_data)

    def single_file_thread(self, data):
        '''
            Executes the get_data function on an array of files in a separate thread
            and removes itself from self.threads once completed.

            ----------

            Arguments
            -------------------------
            `data` {dict}
                a dictionary containing the file_paths and thread_id keys

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-19-2021 13:49:59
            `memberOf`: dir
            `version`: 1.0
            `method_name`: single_file_thread
        '''
        file_paths = data['file_paths']
        for file_path in file_paths:
            self._get_data_thread(file_path)
        self.remove_thread_by_id(data['thread_id'])

    def master(self):
        '''
            Executes the get files process using threads

            ----------

            Return {list}
            ----------------------
            A list of files found in the search_path.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-19-2021 13:52:24
            `memberOf`: dir
            `version`: 1.0
            `method_name`: master
        '''
        for path in self.search_path:
            # pylint: disable=unused-variable
            for root, folders, files in os.walk(path):

                # print(f"Active Threads: {csu.format.left_pad(len(self.threads),3,'0')} Total Files: {len(self.file_array)}", end="\r", flush=True)
                while len(self.threads) >= self.max_threads:
                    time.sleep(.1)

                file_paths = [os.path.join(root, x) for x in files]
                data = {
                    "thread_id": strUtils.gen.hash(json.dumps(file_paths)),
                    "file_paths": file_paths
                }
                thread = Thread(target=self.single_file_thread, args=(data,))
                self.threads.append(data['thread_id'])
                thread.start()

                if self.recursive is False:
                    break
            # return self.file_array
            # path_files = index_files(path, extension_array, ignore_array, recursive)
            # file_array = path_files + file_array
        # print(f"                                                                                                                      ", end="\r", flush=True)
        return self.file_array

        # def _get_files_single_thread(search_path=False, recursive=False, exclude=None, include=None, extensions=None, data_include=None):
        #     '''
        #         Get all files/data from the search_path.

        #         ----------
        #         Keyword Arguments
        #         -----------------

        #             `search_path`=cwd {str|list}
        #                 The search path or list of paths to iterate.
        #             `recursive`=True {boolean}
        #                 If True the path is iterated recursively
        #             `ignore`=[] {str|list}
        #                 A term or list or terms to ignore if the file path contains any of them.
        #             `extensions`=[] {str|list}
        #                 An extension or list of extensions that the file must have.

        #         return
        #         ----------
        #         `return` {str}
        #             A list of dictionaries containing all matching files.
        #     '''
        #     global _THREAD_GET_FILES_ARRAY
        #     if exclude is None:
        #         exclude = []
        #     if include is None:
        #         include = []
        #     if extensions is None:
        #         extensions = []
        #     if data_include is None:
        #         data_include = []
        #     for path in search_path:
        #         print(f"Files indexed: {len(_THREAD_GET_FILES_ARRAY)}", end="\r", flush=True)
        #         _THREAD_GET_FILES_ARRAY = _THREAD_GET_FILES_ARRAY + get_files(search_path=path, recursive=recursive, exclude=exclude, include=include, extensions=extensions, data_include=data_include)
        #     # _THREAD_GET_FILES_ARRAY = _THREAD_GET_FILES_ARRAY + get_files(search_path=search_path, recursive=recursive, exclude=exclude, include=include, extensions=extensions)
        #     return

        # def get_files_thread(search_path=False, **kwargs):
        #     '''
        #         Get all files/data from the search_path.

        #         ----------
        #         Keyword Arguments
        #         -----------------

        #             `search_path`=cwd {str|list}
        #                 The search path or list of paths to iterate.
        #             `recursive`=True {boolean}
        #                 If True the path is iterated recursively
        #             `ignore`=[] {str|list}
        #                 A term or list or terms to ignore if the file path contains any of them.
        #             `extensions`=[] {str|list}
        #                 An extension or list of extensions that the file must have.

        #         return
        #         ----------
        #         `return` {str}
        #             A list of dictionaries containing all matching files.
        #     '''
        #     global _THREAD_GET_FILES_ARRAY
        #     _THREAD_GET_FILES_ARRAY = []

        #     file_array = []
        #     if search_path is False:
        #         search_path = obj.get_kwarg(['search path', 'search'], os.getcwd(), (str, list), **kwargs)
        #     if isinstance(search_path, list) is False:
        #         search_path = [search_path]

        #     data_include = obj.get_kwarg(['data include'], [], (list, str), **kwargs)
        #     if isinstance(data_include, (str)):
        #         data_include = [data_include]

        #     recursive = obj.get_kwarg(['recursive', 'recurse'], True, bool, **kwargs)

        #     # ignore_array = obj.get_kwarg(['ignore', 'ignore_array', 'exclude'], [], (str, list), **kwargs)
        #     exclude = obj.get_kwarg(['exclude', 'ignore', 'ignore array'], [], (list, str), **kwargs)
        #     if isinstance(exclude, (str)):
        #         exclude = [exclude]

        #     include = obj.get_kwarg(['include'], [], (list, str), **kwargs)
        #     if isinstance(include, (str)):
        #         include = [include]

        #     extension_array = strUtils.format.extension(obj.get_kwarg(['extensions', 'ext', 'extension'], [], (str, list), **kwargs))
        #     if isinstance(extension_array, (str)):
        #         extension_array = [extension_array]

        #     dir_array = get_folders(search_path, recursive=recursive, exclude=exclude, include=include, paths_only=True)
        #     # dir_array.append(search_path)
        #     max_threads = 30
        #     dirs_per_thread = round(len(dir_array) / max_threads)
        #     print(f"dirs_per_thread: {dirs_per_thread}")
        #     threads = []
        #     for idx in range(max_threads):
        #         min_id = idx * dirs_per_thread
        #         max_id = min_id + dirs_per_thread
        #         if max_id > len(dir_array):
        #             max_id = len(dir_array)

        #         search_paths = dir_array[min_id:max_id]
        #         print(f"Thread {idx} [{min_id}:{max_id}]")
        #         threads.append(Thread(target=_get_files_single_thread, args=(search_paths, recursive, exclude, include, data_include)))

        #         # file_array = get_files(search_paths, recursive=recursive, exclude=exclude, include=include)
        #         # file_array += get_files(search_paths, recursive=recursive, exclude=exclude, include=include)
        #     for thread in threads:
        #         thread.start()
        #     for thread in threads:
        #         thread.join()
        #         # print(f"result: {result}")
        #     return _THREAD_GET_FILES_ARRAY
        #     # print(f"dir_array")
        #     # print(json.dumps(dir_array, indent=4))
        #     # print(f"_THREAD_GET_FILES_ARRAY")
        #     # print(json.dumps(_THREAD_GET_FILES_ARRAY, indent=4))

        #     # print(f"Total files indexed: {len(file_array)}")


def index_files(start_path, extension_array=None, ignore_array=None, recursive=True):
    '''
        Iterates the start_path to find all files within.

        ----------
        Arguments
        -----------------

            `search_path`=cwd {str|list}
                The search path or list of paths to iterate.
            `ignore`=[] {str|list}
                A term or list or terms to ignore if the file path contains any of them.
            `extensions`=[] {str|list}
                An extension or list of extensions that the file must have.
            `recursive`=True {boolean}
                If True the path is iterated recursively

        return
        ----------
        `return` {str}
            A list of dictionaries containing all matching files.
    '''
    if isinstance(extension_array, list) is False:
        extension_array = []
    if isinstance(ignore_array, list) is False:
        ignore_array = []
    file_array = []
    # pylint: disable=unused-variable
    for root, folders, files in os.walk(start_path):
        for file in files:
            file_data = f.get_data(os.path.join(root, file))
            ignore = False

            if len(extension_array) > 0:
                if file_data['extension'] not in extension_array:
                    ignore = True

            if len(ignore_array) > 0:
                for ignore_string in ignore_array:
                    if ignore_string in file_data['file_path']:
                        ignore = True

            if ignore is False:
                # fd['file_hash'] = generateFileHash(fd['file_path'])
                file_array.append(file_data)

        if recursive is False:
            break
    return file_array


def delete(file_path, ftp=None):
    '''
        Deletes a directory from the local machine or FTP server.

        ----------

        Arguments
        -------------------------
        `file_path` {str}
            The path of the directory to delete.

        [`ftp`=None] {obj}
            A reference to the ftputil object.


        Return {bool}
        ----------------------
        True upon success, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 11:56:21
        `memberOf`: dir
        `version`: 1.0
        `method_name`: delete
    '''
    success = False
    if ftp is not None:
        success = delete_ftp(file_path, ftp)
    try:
        shutil.rmtree(file_path)
        success = True
    except OSError as error:
        logger.warning("Failed to delete directory: %s", file_path)
        logger.warning("Error: %s : %s", file_path, error.strerror)
        success = False
        # print("Error: %s : %s" % (file_path, error.strerror))
    return success


def delete_ftp(file_path, ftp):
    '''
        Deletes a directory on an FTP server.

        ----------

        Arguments
        -------------------------
        `file_path` {str}
            The path of the directory to delete.

        [`ftp`=None] {obj}
            A reference to the ftputil object.

        Return {bool}
        ----------------------
        True upon success, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 12:11:53
        `memberOf`: dir
        `version`: 1.0
        `method_name`: delete_ftp
    '''
    success = False
    if exists_ftp(file_path, ftp):
        try:
            ftp.rmtree(file_path)
            if exists_ftp(file_path, ftp) is False:
                success = True
        except FTPOSError as error:
            logger.warning("Failed to delete directory: %s", file_path)
            logger.warning("Error: %s : %s", file_path, error.strerror)
            success = False
    return success


def copy(src, dst=False, **kwargs):
    '''
        Copy a directory to another location.

        ----------

        Arguments
        -------------------------
        `src` {str|list|dict}
            The source directory to copy.\n
            A list of dictionaries/lists:\n
                [["xxx","aaa"],{src_path:"xxx",dst_path:"aaa"}]
            A dictionary:\n
                {src_path:"xxx",dst_path:"aaa"}

        Keyword Arguments
        -------------------------
        `ftp` {obj}
            A reference to the ftputil object.
        [`ftp_direction`='local_to_server'] {str}
            The direction of the copying:
                local_to_server: Copy local directories/files to the FTP server.
                server_to_local: Copy FTP server directories/files to the Local machine.

        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 12:34:48
        `memberOf`: dir
        `version`: 1.0
        `method_name`: copy
    '''
    ftp = obj.get_kwarg(["ftp"], None, None, **kwargs)
    ftp_direction = obj.get_kwarg(["ftp direction"], 'local_to_server', (str), **kwargs)
    copy_list = [src, dst]
    if dst is False:
        copy_list = _parse_copy_data_from_obj(src)

    for dir_data in copy_list:
        if ftp is not None:
            if ftp_direction == 'local_to_server':
                mirror_to_server(dir_data['src_path'], dir_data['dst_path'], **kwargs)
        else:
            mirror(dir_data['src_path'], dir_data['dst_path'], **kwargs)


def mirror(src, dst, **kwargs):
    '''
        Mirrors a source directory to the destination directory.\n
        Optionally, copying files.\n

        ----------

        Arguments
        -------------------------
        `src` {str}
            The file path to be copied to the dst
        `dst` {str}
            The path to copy the src to.

        Keyword Arguments
        -------------------------
        [`empty_files`=False] {bool}
            If True, files are copied but have no contents.
        [`dirs_only`=False] {bool}
            If True, only directories are copied.
        [`recursive`=True] {bool}
            If True the path is iterated recursively
        [`exclude`=[]] {str|list}
            A string or list of strings, if the file path contains any of them,
            the directory is ignored.\n
            If provided, these rules apply to both files and directories.
        [`include`=[]] {str|list}
            A string or list of strings, if the file path does NOT contain any of them,
            the directory is ignored.\n
            If provided, these rules apply to both files and directories.
        [`exclude_dirs`=[]] {str|list}
            A string or list of strings, if the file path contains any of them,
            the directory is ignored.\n
            If provided, these rules apply only to directories.
        [`include_dirs`=[]] {str|list}
            A string or list of strings, if the file path does NOT contain any of them,
            the directory is ignored.\n
            If provided, these rules apply only to directories.
        [`exclude_files`=[]] {str|list}
            A string or list of strings, if the file path contains any of them,
            the directory is ignored.\n
            If provided, these rules apply only to files.
        [`include_files`=[]] {str|list}
            A string or list of strings, if the file path does NOT contain any of them,
            the directory is ignored.\n
            If provided, these rules apply only to files.
        [`ftp`=None] {obj}
            A reference to the ftputil object.
        [`ftp_direction`='local_to_server'] {str}
            The direction of the copying:
                local_to_server: Copy local directories/files to the FTP server.
                server_to_local: Copy FTP server directories/files to the Local machine.


        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-11-2021 14:34:12
        `memberOf`: dir
        `version`: 1.0
        `method_name`: mirror
    '''
    # if EMPTY_FILES is True, it creates a duplicate file with no content.
    empty_files = obj.get_kwarg(['empty files'], False, bool, **kwargs)
    dirs_only = obj.get_kwarg(['dirs only'], False, bool, **kwargs)
    recursive = obj.get_kwarg(['recursive', 'recurse'], True, (bool), **kwargs)
    include = obj.get_kwarg(['include'], [], (list, str), **kwargs)
    exclude = obj.get_kwarg(['exclude'], [], (list, str), **kwargs)

    include_dirs = obj.get_kwarg(['include dirs'], include, (list, str), **kwargs)
    exclude_dirs = obj.get_kwarg(['exclude dirs'], exclude, (list, str), **kwargs)

    include_files = obj.get_kwarg(['include files'], include, (list, str), **kwargs)
    exclude_files = obj.get_kwarg(['exclude files'], exclude, (list, str), **kwargs)

    ftp = obj.get_kwarg(["ftp"], None, None, **kwargs)
    ftp_direction = obj.get_kwarg(["ftp direction"], 'local_to_server', (str), **kwargs)

    if ftp is not None:
        if ftp_direction == "local_to_server":
            return mirror_to_server(src, dst, **kwargs)

    src = os.path.abspath(src)
    if exists(src) is False:
        logger.warning("Source path must exist.\nsource: %s", src)
        return False

    if exists(dst) is False:
        os.makedirs(dst)
    dirs = get_folders(search_path=src, recursive=recursive,
                       include=include_dirs, exclude=exclude_dirs)

    for folder in dirs:
        folder['dst_path'] = folder['file_path'].replace(src, dst)
        try:
            os.makedirs(folder['dst_path'], exist_ok=True)
            if dirs_only is False:
                files = get_files(search_path=folder['file_path'], include=include_files,
                                  exclude=exclude_files, recursive=False)
                # newlist = [x['dst_path'] = x['file_path'].replace(src, dst) for x in files]
                for file in files:
                    file['src_path'] = file['file_path']
                    file['dst_path'] = file['file_path'].replace(src, dst)
                # folder['dst_path'] = folder['file_path'].replace(src, dst)
                if empty_files is True:
                    for file in files:
                        write.write(file['dst_path'], "EMPTY TEST FILE CONTENT")
                else:
                    f.copy(files)
        except:
            # print(f"{traceback.format_exc()}")
            logger.warning("failed to create directory: %s", folder["dst_path"])
            logger.warning(traceback.format_exc())


def mirror_to_server(src, dst, **kwargs):
    '''
        Mirrors the local source directory to the FTP destination directory.
        Optionally, copying files.

        ----------

        Arguments
        -------------------------
        `src` {str}
            The LOCAL file path to be copied to the dst
        `dst` {str}
            The FTP path to copy the src to.

        Keyword Arguments
        -------------------------
        `ftp` {obj}
            A reference to the ftputil object.
        [`dirs_only`=False] {bool}
            If True, only directories are copied.
        [`recursive`=True] {bool}
            If True the path is iterated recursively
        [`exclude`=[]] {str|list}
            A string or list of strings, if the file path contains any of them,
            the directory is ignored.\n
            If provided, these rules apply to both files and directories.
        [`include`=[]] {str|list}
            A string or list of strings, if the file path does NOT contain any of them,
            the directory is ignored.\n
            If provided, these rules apply to both files and directories.
        [`exclude_dirs`=[]] {str|list}
            A string or list of strings, if the file path contains any of them,
            the directory is ignored.\n
            If provided, these rules apply only to directories.
        [`include_dirs`=[]] {str|list}
            A string or list of strings, if the file path does NOT contain any of them,
            the directory is ignored.\n
            If provided, these rules apply only to directories.
        [`exclude_files`=[]] {str|list}
            A string or list of strings, if the file path contains any of them,
            the directory is ignored.\n
            If provided, these rules apply only to files.
        [`include_files`=[]] {str|list}
            A string or list of strings, if the file path does NOT contain any of them,
            the directory is ignored.\n
            If provided, these rules apply only to files.



        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-11-2021 14:34:12
        `memberOf`: dir
        `version`: 1.0
        `method_name`: mirror
    '''
    # if EMPTY_FILES is True, it creates a duplicate file with no content.
    dirs_only = obj.get_kwarg(['dirs only'], False, bool, **kwargs)
    recursive = obj.get_kwarg(['recursive', 'recurse'], True, (bool), **kwargs)
    include = obj.get_kwarg(['include'], [], (list, str), **kwargs)
    exclude = obj.get_kwarg(['exclude'], [], (list, str), **kwargs)

    include_dirs = obj.get_kwarg(['include dirs'], include, (list, str), **kwargs)
    exclude_dirs = obj.get_kwarg(['exclude dirs'], exclude, (list, str), **kwargs)

    include_files = obj.get_kwarg(['include files'], include, (list, str), **kwargs)
    exclude_files = obj.get_kwarg(['exclude files'], exclude, (list, str), **kwargs)

    ftp = obj.get_kwarg(["ftp"], None, None, **kwargs)
    if ftp is None:
        logger.warning("No FTP object provided.")
        return False

    src = os.path.abspath(src)
    if exists(src) is False:
        logger.warning("Source path must exist.\nsource: %s", src)
        return False

    if exists(dst, ftp=ftp) is False:
        create(dst, ftp=ftp)

    dirs = get_folders(search_path=src, recursive=recursive,
                       include=include_dirs, exclude=exclude_dirs, ftp=ftp)

    for folder in dirs:
        folder['dst_path'] = folder['file_path'].replace(src, dst)
        try:
            create(folder['dst_path'], ftp=ftp)
            if dirs_only is False:
                files = get_files(search_path=folder['file_path'], include=include_files,
                                  exclude=exclude_files, recursive=False, ftp=ftp)
                # newlist = [x['dst_path'] = x['file_path'].replace(src, dst) for x in files]
                for file in files:
                    file['src_path'] = file['file_path']
                    file['dst_path'] = file['file_path'].replace(src, dst)
                f.copy(files, ftp=ftp)
        except:
            logger.warning("failed to create directory: %s", folder["dst_path"])
            logger.warning(traceback.format_exc())


def _parse_copy_data_from_obj(file_obj):
    data = {
        "src_path": None,
        "dst_path": None,
    }
    if isinstance(file_obj, (tuple, list)):
        if len(file_obj) == 2:
            data['src_path'] = file_obj[0]
            data['dst_path'] = file_obj[1]
        else:
            print("Invalid list/tuple provided for copy file. Must be [source_file_path, destination_file_path]")
    if isinstance(file_obj, (dict)):
        for syn in utils.resources.SRC_PATH_SYNONYMS:
            synvar = strUtils.gen.variations(syn)
            for synonym_variant in synvar:
                if synonym_variant in file_obj:
                    data['src_path'] = file_obj[synonym_variant]
        for syn in utils.resources.DEST_PATH_SYNONYMS:
            synvar = strUtils.gen.variations(syn)
            for synonym_variant in synvar:
                if synonym_variant in file_obj:
                    data['dst_path'] = file_obj[synonym_variant]

    if exists(data['src_path']) is False:
        print(f"Invalid source path provided, {data['src_path']} could not be found.")
    return data


# file = r"C:\Users\Colemen\Desktop\DAZ DOWNLOADS\poses"
# get_files(file)
# src = r"C:\Users\Colemen\Desktop\TEST_FOLDER\directoryMirrorTests\sourceDirectory"
# dst = r"C:\Users\Colemen\Desktop\TEST_FOLDER\directoryMirrorTests\targetDirectory"
# mirror(src, dst)

# src = r"Z:\Structure\Ra9\2021"
# start_time = time.time()
# get_files_thread(src)
# end_time = time.time()
# print(f"indexing duration: {end_time - start_time}")
