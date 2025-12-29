from datetime import datetime, timedelta
from src.dominio.modelos import Medico, Paciente
from .container import Container

class FachadaSistema:
    def __init__(self):
        self.container = Container()

    def adicionar_medico(self, nome: str, especialidade: str):
        repo = self.container.medico_repo
        novo_id = repo.proximo_id()
        medico = Medico(id=novo_id, nome=nome, especialidade=especialidade)
        return repo.adicionar(medico)

    def listar_medicos(self):
        return self.container.medico_repo.listar()

    def remover_medico(self, medico_id: int):
        return self.container.agendamento_servico.remover_medico_e_consultas(medico_id)

    def adicionar_paciente(self, nome: str):
        repo = self.container.paciente_repo
        novo_id = repo.proximo_id()
        paciente = Paciente(id=novo_id, nome=nome)
        return repo.adicionar(paciente)

    def listar_pacientes(self):
        return self.container.paciente_repo.listar()

    def remover_paciente(self, paciente_id: int):
        return self.container.paciente_repo.remover(paciente_id)

    def agendar_consulta(self, medico_id: int, paciente_id: int, data_hora_str: str, duracao_minutos: int):
        inicio = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")
        fim = inicio + timedelta(minutes=duracao_minutos)
        
        return self.container.agendamento_servico.agendar_consulta(
            medico_id=medico_id,
            paciente_id=paciente_id,
            inicio=inicio,
            fim=fim
        )

    def listar_consultas_todas(self):
        consultas = self.container.consulta_repo.listar()
        resultado = []
        for c in consultas:
            medico = self.container.medico_repo.buscar_por_id(c.medico_id)
            paciente = self.container.paciente_repo.buscar_por_id(c.paciente_id)
            nome_med = medico.nome if medico else "Desconhecido"
            nome_pac = paciente.nome if paciente else "Desconhecido"
            resultado.append({
                "id": c.id,
                "medico": nome_med,
                "paciente": nome_pac,
                "inicio": c.inicio.strftime("%d/%m/%Y %H:%M"),
                "fim": c.fim.strftime("%H:%M")
            })
        return resultado