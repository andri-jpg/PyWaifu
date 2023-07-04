import urllib.request
import subprocess

class ModelDownloader:
    def ask_download(self, url, file_path):
        user_input = input(f"Model file '{file_path}' not found. Do you want to download the suggested model? Press 'y' for yes, or download the model yourself. [y/n]: ")
        if user_input.lower() == 'y':
            self.download_file(url, file_path)
        else:
            raise FileNotFoundError("Model file not downloaded. Please download the model file yourself.")

    def download_file(self, url, file_path):
        print(f"Downloading {file_path}...")
        urllib.request.urlretrieve(url, file_path)
        print("Download completed.")

    def install_git_lfs(self):
        try:
            subprocess.check_output(["git", "lfs", "install"])
            print("Git LFS installed successfully.")
        except subprocess.CalledProcessError as e:
            print("Failed to install Git LFS:", e)

    def clone_repository(self, repo_url):
        try:
            subprocess.check_output(["git", "clone", repo_url])
            print("Repository cloned successfully.")
        except subprocess.CalledProcessError as e:
            print("Failed to clone repository:", e)

