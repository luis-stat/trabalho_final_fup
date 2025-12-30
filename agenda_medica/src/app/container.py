from src.infra.repos_memoria import MedicoRepositoryMemoria, PacienteRepositoryMemoria, ConsultaRepositoryMemoria

class Container:
    def __init__(self):
        self.medico_repo = MedicoRepositoryMemoria()
        self.paciente_repo = PacienteRepositoryMemoria()
        self.consulta_repo = ConsultaRepositoryMemoria()