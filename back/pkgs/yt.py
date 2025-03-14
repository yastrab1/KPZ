import subprocess
import sys
# import yt-dlp


if __name__ == "__main__":
    args = sys.argv[1:]

    subprocess.run(["yt-dlp",*args])
