
import os


class FirmwareBinPath(object):

    def __init__(self):
        self.linux_path = "/home/share/sqa/FW_Release/redtail/nightly"
        self.windows_path = r"\\172.29.190.4\share\sqa\FW_Release\redtail\nightly"

    def search_firmware_folder(self, commit):
        bin_folder = None
        for item in os.listdir(self.windows_path):
            item_path = os.path.join(self.windows_path, item)
            if os.path.isdir(item_path):
                if commit in item_path:
                    bin_folder = item
                    break
        return bin_folder

    def search_firmware_file(self, bin_folder, commit, volume):
        bin_file = None
        bin_path = os.path.join(self.windows_path, bin_folder)
        for item in os.listdir(bin_path):
            item_path = os.path.join(bin_path, item)
            if os.path.isfile(item_path):
                if commit in item:
                    if "_{}_".format(volume.lower()) in item.lower():
                        if item.endswith(".bin"):
                            bin_file = item
        return bin_file

    def get_auto_build_fw_path(self, commit, volume):
        volume = "ALL" if volume == "" else volume
        linux_path,  windows_path = None, None
        bin_folder = self.search_firmware_folder(commit)
        if bin_folder is not None:
            bin_file = self.search_firmware_file(bin_folder, commit, volume)
            if bin_file is not None:
                linux_path = "{}/{}/{}".format(self.linux_path, bin_folder, bin_file)
                windows_path = os.path.join(self.windows_path, bin_folder, bin_file)
        return windows_path, linux_path

    def get_related_fw_path(self, base_path, commit, volume):
        fw_path = None
        fw_file = self.search_firmware_file(base_path, commit, volume)
        if fw_file is not None:
            fw_path = os.path.join(base_path, fw_file)
        return fw_path
