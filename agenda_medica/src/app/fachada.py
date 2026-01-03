from datetime import datetime, timedelta
from src.dominio import servicos
from .container import Container

class FachadaSistema:
    def __init__(self):
        self.container = Container()

    def adicionar_medico(self, nome: str, especialidade: str):
        return servicos.cadastrar_medico(self.container.medico_repo, nome, especialidade)

    def listar_medicos(self):
        return servicos.listar_medicos(self.container.medico_repo)

    def buscar_medico(self, medico_id: int):
        return servicos.buscar_medico(self.container.medico_repo, medico_id)

    def remover_medico(self, medico_id: int):
        return servicos.remover_medico(self.container.medico_repo, self.container.consulta_repo, medico_id)

    def adicionar_paciente(self, nome: str):
        return servicos.cadastrar_paciente(self.container.paciente_repo, nome)

    def listar_pacientes(self):
        return servicos.listar_pacientes(self.container.paciente_repo)

    def buscar_paciente(self, paciente_id: int):
        return servicos.buscar_paciente(self.container.paciente_repo, paciente_id)

    def remover_paciente(self, paciente_id: int):
        return servicos.remover_paciente(self.container.paciente_repo, self.container.consulta_repo, paciente_id)

    def agendar_consulta(self, medico_id: int, paciente_id: int, data_hora_str: str, duracao_minutos: int):
        inicio = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")
        fim = inicio + timedelta(minutes=duracao_minutos)
        return servicos.agendar_consulta(
            self.container.consulta_repo,
            self.container.medico_repo,
            self.container.paciente_repo,
            medico_id,
            paciente_id,
            inicio,
            fim
        )

    def buscar_consulta(self, consulta_id: int):
        return servicos.buscar_consulta(self.container.consulta_repo, consulta_id)

    def cancelar_consulta(self, consulta_id: int):
        return servicos.cancelar_consulta(self.container.consulta_repo, consulta_id)

    def remarcar_consulta(self, consulta_id: int, novo_medico_id: int, nova_data_str: str):
        inicio = datetime.strptime(nova_data_str, "%d/%m/%Y %H:%M")
        return servicos.remarcar_consulta(
            self.container.consulta_repo,
            self.container.medico_repo,
            consulta_id,
            novo_medico_id,
            inicio
        )

    def listar_consultas_todas(self):
        consultas = servicos.listar_consultas(self.container.consulta_repo)
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