from bitlogs.message_type import MessageType
from bitlogs.terminal_colors import TerminalColors


class InfoMessage(MessageType):
    def get_name(self):
        return "INFO"

    def get_color_code(self):
        return TerminalColors.OKBLUE
