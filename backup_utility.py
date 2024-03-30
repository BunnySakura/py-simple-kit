import shutil
import argparse
import subprocess
import time
import os


class BackupUtility:
    def __init__(self):
        self.cloud_app = ""
        self.remote_path = ""
        self.source_paths = []

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description="Backup files to cloud storage.")
        parser.add_argument("-c", "--cloud", required=True, help="Path to the cloud storage client.")
        parser.add_argument("-r", "--remote", required=True, help="Remote path in the cloud storage.")
        parser.add_argument("-s", "--source", required=True, nargs='+', help="Source paths of the files to backup.")
        return parser.parse_args()

    @staticmethod
    def archive_files(source_path, date):
        source_name = os.path.basename(os.path.normpath(source_path))
        filename = f"{source_name}_{date}"
        return shutil.make_archive(filename, 'zip', source_path)

    def upload_archive(self, archive_filename):
        upload_cmd = [self.cloud_app, "u", archive_filename, self.remote_path]
        subprocess.run(upload_cmd)

    @staticmethod
    def cleanup_temp_archive(archive_filename):
        os.remove(archive_filename)

    def run_backup(self):
        args = self.parse_arguments()

        self.cloud_app = args.cloud
        self.remote_path = args.remote
        self.source_paths = args.source

        date = time.strftime("%Y-%m-%d", time.localtime())

        for source_path in self.source_paths:
            archive_filename = self.archive_files(source_path, date)
            self.upload_archive(archive_filename)
            self.cleanup_temp_archive(archive_filename)


if __name__ == '__main__':
    backup_utility = BackupUtility()
    backup_utility.run_backup()
