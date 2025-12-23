from typing import Generic, TypeVar
from dominio.modelos import Medico, Paciente, Consulta
from dominio.repositorios import MedicoRepository, PacienteRepository, ConsultaRepository

T = TypeVar("T")

class BaseRepositoryMemoria(Generic[T]):
    def __init__(self):
        self._dados: dict[int, T] = {}
        self._proximo_id = 1

    def proximo_id(self) -> int:
        return self._proximo_id

    def adicionar(self, obj: T) -> T:
        if obj.id in self._dados:
            raise ValueError(f"ID {obj.id} já existe.")
        self._dados[obj.id] = obj
        if obj.id >= self._proximo_id:
            self._proximo_id = obj.id + 1
        return obj

    def buscar_por_id(self, obj_id: int) -> T | None:
        return self._dados.get(obj_id)

    def listar(self) -> list[T]:
        return list(self._dados.values())

    def remover(self, obj_id: int) -> bool:
        return self._dados.pop(obj_id, None) is not None


class MedicoRepositoryMemoria(BaseRepositoryMemoria[Medico], MedicoRepository):
    pass


class PacienteRepositoryMemoria(BaseRepositoryMemoria[Paciente], PacienteRepository):
    pass


class ConsultaRepositoryMemoria(BaseRepositoryMemoria[Consulta], ConsultaRepository):
    def listar_por_medico(self, medico_id: int) -> list[Consulta]:
        return [c for c in self._dados.values() if c.medico_id == medico_id]
