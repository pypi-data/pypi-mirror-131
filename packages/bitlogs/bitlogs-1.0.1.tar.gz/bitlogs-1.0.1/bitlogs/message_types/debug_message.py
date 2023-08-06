from bitlogs.message_type import MessageType
from bitlogs.terminal_colors import TerminalColors


class DebugMessage(MessageType):
    def get_name(self):
        return "DEBUG"

    def get_color_code(self):
        return TerminalColors.OKGREEN
