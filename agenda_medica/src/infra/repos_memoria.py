from src.dominio.modelos import Medico, Paciente, Consulta
from src.dominio.repositorios import MedicoRepository, PacienteRepository, ConsultaRepository

class MedicoRepositoryMemoria(MedicoRepository):
    def __init__(self):
        self._dados = {}

    def proximo_id(self) -> int:
        id_tentativa = 1
        while id_tentativa in self._dados:
            id_tentativa += 1
        return id_tentativa

    def adicionar(self, medico: Medico) -> Medico:
        for m in self._dados.values():
            if m.nome.lower() == medico.nome.lower():
                raise ValueError(f"O médico '{medico.nome}' já está cadastrado.")
        
        self._dados[medico.id] = medico
        return medico

    def buscar_por_id(self, medico_id: int) -> Medico | None:
        return self._dados.get(medico_id)

    def listar(self) -> list[Medico]:
        return sorted(list(self._dados.values()), key=lambda m: m.id)

    def remover(self, medico_id: int) -> bool:
        if medico_id in self._dados:
            del self._dados[medico_id]
            return True
        return False

class PacienteRepositoryMemoria(PacienteRepository):
    def __init__(self):
        self._dados = {}

    def proximo_id(self) -> int:
        id_tentativa = 1
        while id_tentativa in self._dados:
            id_tentativa += 1
        return id_tentativa

    def adicionar(self, paciente: Paciente) -> Paciente:
        for p in self._dados.values():
            if p.nome.lower() == paciente.nome.lower():
                raise ValueError(f"O paciente '{paciente.nome}' já está cadastrado.")

        self._dados[paciente.id] = paciente
        return paciente

    def buscar_por_id(self, paciente_id: int) -> Paciente | None:
        return self._dados.get(paciente_id)

    def listar(self) -> list[Paciente]:
        return sorted(list(self._dados.values()), key=lambda p: p.id)

    def remover(self, paciente_id: int) -> bool:
        if paciente_id in self._dados:
            del self._dados[paciente_id]
            return True
        return False

class ConsultaRepositoryMemoria(ConsultaRepository):
    def __init__(self):
        self._dados = {}

    def proximo_id(self) -> int:
        id_tentativa = 1
        while id_tentativa in self._dados:
            id_tentativa += 1
        return id_tentativa

    def adicionar(self, consulta: Consulta) -> Consulta:
        self._dados[consulta.id] = consulta
        return consulta

    def buscar_por_id(self, consulta_id: int) -> Consulta | None:
        return self._dados.get(consulta_id)

    def listar(self) -> list[Consulta]:
        return sorted(list(self._dados.values()), key=lambda c: c.id)

    def listar_por_medico(self, medico_id: int) -> list[Consulta]:
        return [c for c in self._dados.values() if c.medico_id == medico_id]

    def remover(self, consulta_id: int) -> bool:
        if consulta_id in self._dados:
            del self._dados[consulta_id]
            return True
        return False