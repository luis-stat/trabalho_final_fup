from datetime import datetime
from .modelos import Consulta
from .repositorios import MedicoRepository, PacienteRepository, ConsultaRepository

class ServicoDeAgendamento:
    def __init__(
        self,
        medico_repo: MedicoRepository,
        paciente_repo: PacienteRepository,
        consulta_repo: ConsultaRepository
    ):
        self.medico_repo = medico_repo
        self.paciente_repo = paciente_repo
        self.consulta_repo = consulta_repo

    def agendar_consulta(self, medico_id: int, paciente_id: int, inicio: datetime, fim: datetime) -> Consulta:
        medico = self.medico_repo.buscar_por_id(medico_id)
        if not medico:
            raise ValueError("Médico não encontrado.")

        paciente = self.paciente_repo.buscar_por_id(paciente_id)
        if not paciente:
            raise ValueError("Paciente não encontrado.")

        consultas_existentes = self.consulta_repo.listar_por_medico(medico_id)
        for consulta in consultas_existentes:
            if self._verificar_sobreposicao(inicio, fim, consulta.inicio, consulta.fim):
                raise ValueError("O médico já possui uma consulta neste horário.")

        novo_id = self.consulta_repo.proximo_id()
        
        nova_consulta = Consulta(
            id=novo_id,
            medico_id=medico_id,
            paciente_id=paciente_id,
            inicio=inicio,
            fim=fim
        )
        return self.consulta_repo.adicionar(nova_consulta)

    def remover_medico_e_consultas(self, medico_id: int) -> bool:
        consultas = self.consulta_repo.listar_por_medico(medico_id)
        for consulta in consultas:
            self.consulta_repo.remover(consulta.id)
        
        return self.medico_repo.remover(medico_id)

    def _verificar_sobreposicao(self, inicio1: datetime, fim1: datetime, inicio2: datetime, fim2: datetime) -> bool:
        return max(inicio1, inicio2) < min(fim1, fim2)