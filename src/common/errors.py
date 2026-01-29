class ErroExplicado(Exception):
    def __init__(self, msg, causa, solucao):
        super().__init__(msg)
        self.causa = causa
        self.solucao = solucao