from src.infra.repos_memoria import MedicoRepositoryMemoria, PacienteRepositoryMemoria, ConsultaRepositoryMemoria
from src.dominio.regras import ServicoDeAgendamento

class Container:
    def __init__(self):
        self.medico_repo = MedicoRepositoryMemoria()
        self.paciente_repo = PacienteRepositoryMemoria()
        self.consulta_repo = ConsultaRepositoryMemoria()
        
        self.agendamento_servico = ServicoDeAgendamento(
            self.medico_repo,
            self.paciente_repo,
            self.consulta_repo
        )