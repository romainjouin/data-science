class path_cleaner:
    """
    Class which rename files so that they are compatible with OneDrive
    """
    unwanted_chars_in_directories = ["\\", ":", "*", "?", "\"", ">", "<", "|", "�"]
    unwanted_chars_in_filenames = ["/", "\\", ":", "*", "?", "\"", ">", "<", "|", "�"]    
    def remove(string, list_of_unwanted_car, replacement_char="_"):
        """
        Remove unwanted chars from a string.
        """
        new_string = string
        for unwanted_char in list_of_unwanted_car:
            new_string = new_string.replace(unwanted_char, replacement_char)
        return new_string

    def clean_dirname(self, dirname):
        """
        Remove unwanted characters from directory names.
        """
        return remove(dirname,self.unwanted_chars_in_directories)

    def clean_filename(self, filename):
        """
        Remove unwanted characters from filename.
        """
        return remove(filename,self.unwanted_chars_in_filenames)

    def ensure_compatible_directory_name(self, actual_dirname):
        """
        Rename a the directory if it has an unwanted character.
        """
        cleaned_dirname = clean_dirname(actual_dirname)
        if actual_dirname != cleaned_dirname:
            import os
            os.rename(actual_dirname, cleaned_dirname)
            print(("rename = %s to %s"% (actual_dirname, cleaned_dirname)))
        return cleaned_dirname


    def make_sub_directories_compatible_with_oneDrive(self, directory_path):
        """
        Rename all subdirectory so that they are compatible with oneDrive.
        """
        assert os.path.isdir(directory_path), "Dir [{0}] doesn't exist".format(directory_path)
        for dirname, dirnames, filenames in os.walk(directory_path) :
            dirnames = [os.path.join(dirname,sub_directory) for sub_directory in dirnames]
            list(map(ensure_compatible_dirname, dirnames))
