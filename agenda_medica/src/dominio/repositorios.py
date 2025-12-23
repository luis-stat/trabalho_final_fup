from .modelos import Medico, Paciente, Consulta

class MedicoRepository:
    def __init__(self):
        self._dados = {}
        self._proximo_id = 1

    def proximo_id(self) -> int:
        return self._proximo_id

    def adicionar(self, medico: Medico) -> Medico:
        if medico.id in self._dados:
            raise ValueError(f"Médico com ID {medico.id} já existe.")
        self._dados[medico.id] = medico
        if medico.id >= self._proximo_id:
            self._proximo_id = medico.id + 1
        return medico


    def buscar_por_id(self, medico_id: int) -> Medico | None:
        return self._dados.get(medico_id)

    def listar(self) -> list[Medico]:
        return list(self._dados.values())

    def remover(self, medico_id: int) -> bool:
        if medico_id in self._dados:
            del self._dados[medico_id]
            return True
        return False

class PacienteRepository:
    def __init__(self):
        self._dados = {}
        self._proximo_id = 1

    def proximo_id(self) -> int:
        return self._proximo_id

    def adicionar(self, paciente: Paciente) -> Paciente:
        if paciente.id in self._dados:
            raise ValueError(f"Paciente com ID {paciente.id} já existe.")
        self._dados[paciente.id] = paciente
        if paciente.id >= self._proximo_id:
            self._proximo_id = paciente.id + 1
        return paciente

    def buscar_por_id(self, paciente_id: int) -> Paciente | None:
        return self._dados.get(paciente_id)

    def listar(self) -> list[Paciente]:
        return list(self._dados.values())

    def remover(self, paciente_id: int) -> bool:
        if paciente_id in self._dados:
            del self._dados[paciente_id]
            return True
        return False

class ConsultaRepository:
    def __init__(self):
        self._dados = {}
        self._proximo_id = 1

    def proximo_id(self) -> int:
        return self._proximo_id

    def adicionar(self, consulta: Consulta) -> Consulta:
        if consulta.id in self._dados:
            raise ValueError(f"Consulta com ID {consulta.id} já existe.")
        self._dados[consulta.id] = consulta
        if consulta.id >= self._proximo_id:
            self._proximo_id = consulta.id + 1
        return consulta

    def buscar_por_id(self, consulta_id: int) -> Consulta | None:
        return self._dados.get(consulta_id)

    def listar(self) -> list[Consulta]:
        return list(self._dados.values())

    def listar_por_medico(self, medico_id: int) -> list[Consulta]:
        return [c for c in self._dados.values() if c.medico_id == medico_id]

    def remover(self, consulta_id: int) -> bool:
        if consulta_id in self._dados:
            del self._dados[consulta_id]
            return True
        return False