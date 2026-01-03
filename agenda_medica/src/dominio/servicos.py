from datetime import datetime
from .modelos import Medico, Paciente, Consulta
from .repositorios import MedicoRepository, PacienteRepository, ConsultaRepository
from .regras import verificar_sobreposicao, validar_intervalo, validar_data_futura

def cadastrar_medico(repo: MedicoRepository, nome: str, especialidade: str) -> Medico:
    novo = Medico(id=repo.proximo_id(), nome=nome, especialidade=especialidade)
    return repo.adicionar(novo)

def listar_medicos(repo: MedicoRepository) -> list[Medico]:
    return repo.listar()

def buscar_medico(repo: MedicoRepository, medico_id: int) -> Medico | None:
    return repo.buscar_por_id(medico_id)

def remover_medico(medico_repo: MedicoRepository, consulta_repo: ConsultaRepository, medico_id: int) -> bool:
    medico_remover = medico_repo.buscar_por_id(medico_id)
    if not medico_remover:
        return False

    consultas = list(consulta_repo.listar_por_medico(medico_id))
    todos_medicos = medico_repo.listar()
    
    substitutos = [
        m for m in todos_medicos 
        if m.especialidade == medico_remover.especialidade and m.id != medico_id
    ]

    for consulta in consultas:
        realocado = False
        for substituto in substitutos:
            conflito = False
            consultas_substituto = consulta_repo.listar_por_medico(substituto.id)
            
            for cs in consultas_substituto:
                if verificar_sobreposicao(consulta.inicio, consulta.fim, cs.inicio, cs.fim):
                    conflito = True
                    break
            
            if not conflito:
                consulta_repo.remover(consulta.id)
                nova_consulta = Consulta(
                    id=consulta.id,
                    medico_id=substituto.id,
                    paciente_id=consulta.paciente_id,
                    inicio=consulta.inicio,
                    fim=consulta.fim
                )
                consulta_repo.adicionar(nova_consulta)
                realocado = True
                break
        
        if not realocado:
            consulta_repo.remover(consulta.id)
    
    return medico_repo.remover(medico_id)

def cadastrar_paciente(repo: PacienteRepository, nome: str) -> Paciente:
    novo = Paciente(id=repo.proximo_id(), nome=nome)
    return repo.adicionar(novo)

def listar_pacientes(repo: PacienteRepository) -> list[Paciente]:
    return repo.listar()

def buscar_paciente(repo: PacienteRepository, paciente_id: int) -> Paciente | None:
    return repo.buscar_por_id(paciente_id)

def remover_paciente(paciente_repo: PacienteRepository, consulta_repo: ConsultaRepository, paciente_id: int) -> bool:
    if not paciente_repo.buscar_por_id(paciente_id):
        return False
        
    todas_consultas = list(consulta_repo.listar())
    for consulta in todas_consultas:
        if consulta.paciente_id == paciente_id:
            consulta_repo.remover(consulta.id)
            
    return paciente_repo.remover(paciente_id)

def agendar_consulta(
    consulta_repo: ConsultaRepository, 
    medico_repo: MedicoRepository, 
    paciente_repo: PacienteRepository, 
    medico_id: int, 
    paciente_id: int, 
    inicio: datetime, 
    fim: datetime
) -> Consulta:
    if not medico_repo.buscar_por_id(medico_id):
        raise ValueError("Médico não encontrado.")
    if not paciente_repo.buscar_por_id(paciente_id):
        raise ValueError("Paciente não encontrado.")
    if not validar_intervalo(inicio, fim):
        raise ValueError("O fim da consulta deve ser maior do que o início.")
    if not validar_data_futura(inicio):
        raise ValueError("Não é possível agendar consultas para datas passadas.")

    consultas_medico = consulta_repo.listar_por_medico(medico_id)
    for consulta in consultas_medico:
        if verificar_sobreposicao(inicio, fim, consulta.inicio, consulta.fim):
            raise ValueError("O médico já possui uma consulta neste horário.")

    consultas_paciente = consulta_repo.listar_por_paciente(paciente_id)
    for consulta in consultas_paciente:
        if verificar_sobreposicao(inicio, fim, consulta.inicio, consulta.fim):
            raise ValueError("O paciente já possui uma consulta neste horário.")

    nova = Consulta(
        id=consulta_repo.proximo_id(),
        medico_id=medico_id,
        paciente_id=paciente_id,
        inicio=inicio,
        fim=fim
    )
    return consulta_repo.adicionar(nova)

def buscar_consulta(repo: ConsultaRepository, consulta_id: int) -> Consulta | None:
    return repo.buscar_por_id(consulta_id)

def cancelar_consulta(repo: ConsultaRepository, consulta_id: int) -> bool:
    return repo.remover(consulta_id)

def remarcar_consulta(
    consulta_repo: ConsultaRepository,
    medico_repo: MedicoRepository,
    consulta_id: int,
    novo_medico_id: int,
    nova_inicio: datetime
) -> Consulta:
    consulta = consulta_repo.buscar_por_id(consulta_id)
    if not consulta:
        raise ValueError("Consulta não encontrada.")
    
    if not medico_repo.buscar_por_id(novo_medico_id):
        raise ValueError("Novo médico não encontrado.")

    duracao = consulta.fim - consulta.inicio
    novo_fim = nova_inicio + duracao
    
    if not validar_intervalo(nova_inicio, novo_fim):
            raise ValueError("Horário inválido.")
    
    if not validar_data_futura(nova_inicio):
        raise ValueError("Não é possível remarcar consultas para datas passadas.")

    consultas_medico = consulta_repo.listar_por_medico(novo_medico_id)
    for c in consultas_medico:
        if c.id != consulta_id:
            if verificar_sobreposicao(nova_inicio, novo_fim, c.inicio, c.fim):
                raise ValueError("O médico já possui uma consulta neste horário.")

    consultas_paciente = consulta_repo.listar_por_paciente(consulta.paciente_id)
    for c in consultas_paciente:
        if c.id != consulta_id:
            if verificar_sobreposicao(nova_inicio, novo_fim, c.inicio, c.fim):
                raise ValueError("O paciente já possui uma consulta neste horário.")

    consulta.medico_id = novo_medico_id
    consulta.inicio = nova_inicio
    consulta.fim = novo_fim
    return consulta

def listar_consultas(repo: ConsultaRepository) -> list[Consulta]:
    return repo.listar()