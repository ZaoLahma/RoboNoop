class CommCtxt:
    COMM_IF = None

    @staticmethod 
    def get_comm_if():
        return CommCtxt.COMM_IF

    @staticmethod
    def set_comm_if(comm_if):
        CommCtxt.COMM_IF = comm_if