class CommCtxt:
    COMM_STORAGE = None
    COMM_IF = None

    @staticmethod
    def get_comm_storage():
        return CommCtxt.COMM_STORAGE

    @staticmethod
    def set_comm_storage(comm_storage):
        CommCtxt.COMM_STORAGE = comm_storage

    @staticmethod 
    def get_comm_if():
        return CommCtxt.COMM_IF

    @staticmethod
    def set_comm_if(comm_if):
        CommCtxt.COMM_IF = comm_if