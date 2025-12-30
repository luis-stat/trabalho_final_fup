from dataclasses import dataclass
from datetime import datetime

@dataclass
class Medico:
    id: int
    nome: str
    especialidade: str

    def __post_init__(self) -> None:
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("O ID do médico deve ser um inteiro maior do que 0.")
        if not isinstance(self.nome, str) or not self.nome.strip():
            raise ValueError("O nome do médico não pode ser vazio.")
        if any(char.isdigit() for char in self.nome):
            raise ValueError("O nome do médico não pode conter números.")
        if any(char.isdigit() for char in self.especialidade):
            raise ValueError("A especialidade não pode conter números.")
        if not isinstance(self.especialidade, str) or not self.especialidade.strip():
            raise ValueError("A especialidade do médico não pode ser vazia.")

@dataclass
class Paciente:
    id: int
    nome: str

    def __post_init__(self) -> None:
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("O ID do paciente deve ser um inteiro maior do que 0.")
        if not isinstance(self.nome, str) or not self.nome.strip():
            raise ValueError("O nome do paciente não pode ser vazio.")
        if any(char.isdigit() for char in self.nome):
            raise ValueError("O nome do paciente não pode conter números.")

@dataclass
class Consulta:
    id: int
    medico_id: int
    paciente_id: int
    inicio: datetime
    fim: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("O ID da consulta deve ser um inteiro maior do que 0.")
        if not isinstance(self.medico_id, int) or self.medico_id <= 0:
            raise ValueError("O ID do médico deve ser um inteiro maior do que 0.")
        if not isinstance(self.paciente_id, int) or self.paciente_id <= 0:
            raise ValueError("O ID do paciente deve ser um inteiro maior do que 0.")
        if not isinstance(self.inicio, datetime) or not isinstance(self.fim, datetime):
            raise ValueError("O ínicio e fim da consulta devem ser do tipo `datetime`.")
        if self.fim <= self.inicio:
            raise ValueError("O fim da consulta deve ser maior do que o início da consulta.")