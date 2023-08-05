from selenium.webdriver.chrome.options import Options as ChromeOptions

class Options(ChromeOptions):
    KEY: str
    def __init__(self) -> None: ...
    @property
    def capabilities(self): ...
    def set_capability(self, name, value) -> None: ...
    @property
    def android_package_name(self): ...
    @android_package_name.setter
    def android_package_name(self, value) -> None: ...
    @property
    def android_device_socket(self): ...
    @android_device_socket.setter
    def android_device_socket(self, value) -> None: ...
    @property
    def android_command_line_file(self): ...
    @android_command_line_file.setter
    def android_command_line_file(self, value) -> None: ...
    def to_capabilities(self): ...

class AndroidOptions(Options):
    android_package_name: str
    def __init__(self) -> None: ...
