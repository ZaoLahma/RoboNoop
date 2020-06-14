class MessageBase:
    @staticmethod
    def get_msg_id(self):
        raise NotImplementedError

    def encode(self):
        raise NotImplementedError

    def decode(self):
        raise NotImplementedError