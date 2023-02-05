import subprocess
import sys
import threading
import urllib.request
from pathlib import Path
from subprocess import check_output

from tqdm_up_to import TqdmUpTo


class MosquittoServer:
    MOSQUITTO_LINK = 'https://mosquitto.org/files/binary/win64/mosquitto-2.0.15-install-windows-x64.exe'

    def __init__(self):
        script_dir = Path(__file__).parent
        self.install_file = script_dir / Path(self.MOSQUITTO_LINK[self.MOSQUITTO_LINK.rfind('/') + 1:])
        self.working_dir = script_dir / Path('mosquitto')
        self.executable = self.working_dir / Path('mosquitto.exe')
        if not self.executable.is_file():
            if not self.install_file.is_file():
                with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
                              desc=self.install_file.name) as t:
                    urllib.request.urlretrieve(self.MOSQUITTO_LINK, self.install_file, reporthook=t.update_to)
            print(check_output(f'7z e -o{self.working_dir}/ {self.install_file}', shell=True).decode())
            self.install_file.unlink()
        self.thread = None

    def run(self, daemon=False):
        if daemon:
            process = subprocess.Popen(f'{self.executable} -v -c mosquitto.conf', cwd=self.working_dir)
        else:
            process = subprocess.Popen(f'{self.executable} -v -c mosquitto.conf', cwd=self.working_dir,
                                       stdout=sys.stdout, stderr=sys.stderr)
        process.wait()

    def run_as_daemon(self):
        self.thread = threading.Thread(name='mosquitto', target=self.run, args=(True,), daemon=True)
        self.thread.start()


if __name__ == '__main__':
    mosquitto_server = MosquittoServer()
    mosquitto_server.run()
