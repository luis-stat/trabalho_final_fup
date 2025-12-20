from abc import ABC, abstractmethod
from .modelos import Medico, Paciente, Consulta

class MedicoRepository(ABC):
    @abstractmethod
    def proximo_id(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def adicionar(self, medico: Medico) -> Medico:
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, medico_id: int) -> Medico | None:
        raise NotImplementedError

    @abstractmethod
    def listar(self) -> list[Medico]:
        raise NotImplementedError

    @abstractmethod
    def remover(self, medico_id: int) -> bool:
        raise NotImplementedError

class PacienteRepository(ABC):
    @abstractmethod
    def proximo_id(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def adicionar(self, paciente: Paciente) -> Paciente:
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, paciente_id: int) -> Paciente | None:
        raise NotImplementedError

    @abstractmethod
    def listar(self) -> list[Paciente]:
        raise NotImplementedError

    @abstractmethod
    def remover(self, paciente_id: int) -> bool:
        raise NotImplementedError

class ConsultaRepository(ABC):
    @abstractmethod
    def proximo_id(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def adicionar(self, consulta: Consulta) -> Consulta:
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, consulta_id: int) -> Consulta | None:
        raise NotImplementedError

    @abstractmethod
    def listar(self) -> list[Consulta]:
        raise NotImplementedError

    @abstractmethod
    def listar_por_medico(self, medico_id: int) -> list[Consulta]:
        raise NotImplementedError

    @abstractmethod
    def remover(self, consulta_id: int) -> bool:
        raise NotImplementedError