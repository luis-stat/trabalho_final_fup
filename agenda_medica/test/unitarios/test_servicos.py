import pytest
from datetime import datetime, timedelta
from src.infra.repos_memoria import MedicoRepositoryMemoria, PacienteRepositoryMemoria, ConsultaRepositoryMemoria
from src.dominio import servicos
from src.dominio import regras

@pytest.fixture
def repos():
    return (MedicoRepositoryMemoria(), PacienteRepositoryMemoria(), ConsultaRepositoryMemoria())

def test_cadastrar_medico_sucesso(repos):
    mr, _, _ = repos
    medico = servicos.cadastrar_medico(mr, "Dr House", "Infectologista")
    assert medico.id == 1
    assert medico.nome == "Dr House"
    assert len(mr.listar()) == 1

def test_validacao_nome_medico_numeros(repos):
    mr, _, _ = repos
    with pytest.raises(ValueError):
        servicos.cadastrar_medico(mr, "Dr House 10", "Infectologista")

def test_agendar_consulta_sucesso(repos):
    mr, pr, cr = repos
    m = servicos.cadastrar_medico(mr, "Dr House", "Infectologista")
    p = servicos.cadastrar_paciente(pr, "Maria")
    
    inicio = datetime(2025, 12, 25, 10, 0)
    fim = inicio + timedelta(hours=1)
    
    consulta = servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio, fim)
    assert consulta.id == 1
    assert consulta.medico_id == m.id

def test_impedir_agendamento_conflitante(repos):
    mr, pr, cr = repos
    m = servicos.cadastrar_medico(mr, "Dr House", "Infectologista")
    p = servicos.cadastrar_paciente(pr, "Maria")
    
    inicio = datetime(2025, 12, 25, 10, 0)
    fim = datetime(2025, 12, 25, 11, 0)
    servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio, fim)
    
    inicio_conflito = datetime(2025, 12, 25, 10, 30)
    fim_conflito = datetime(2025, 12, 25, 11, 30)
    
    with pytest.raises(ValueError):
        servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio_conflito, fim_conflito)

def test_impedir_agendamento_erroneo_pac(repos):
    mr, pr, cr = repos
    m = servicos.cadastrar_medico(mr, "Dr House", "Infectologista")
    p = servicos.cadastrar_paciente(pr, "Maria")
    
    inicio = datetime(2025, 12, 25, 10, 0)
    fim = datetime(2025, 12, 25, 11, 0)
    servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio, fim)
    
    with pytest.raises(ValueError):
        servicos.agendar_consulta(cr, mr, pr, m.id, 2, inicio, fim)

def test_impedir_agendamento_erroneo_med(repos):
    mr, pr, cr = repos
    m = servicos.cadastrar_medico(mr, "Dr House", "Infectologista")
    p = servicos.cadastrar_paciente(pr, "Maria")
    
    inicio = datetime(2025, 12, 25, 10, 0)
    fim = datetime(2025, 12, 25, 11, 0)
    servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio, fim)
    
    with pytest.raises(ValueError):
        servicos.agendar_consulta(cr, mr, pr, 2, p.id, inicio, fim)

def test_impedir_medico_conflitante_med(repos):
    mr, pr, cr = repos
    m = servicos.cadastrar_medico(mr, "Dr House", "Infectologista")
    p = servicos.cadastrar_paciente(pr, "Maria")
    p1 = servicos.cadastrar_paciente(pr, "José")
    
    inicio = datetime(2025, 12, 25, 10, 0)
    fim = datetime(2025, 12, 25, 11, 0)
    
    servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio, fim)
    
    with pytest.raises(ValueError):
        servicos.agendar_consulta(cr, mr, pr, m.id, p1.id, inicio, fim)

def test_impedir_medico_conflitante_pac(repos):
    mr, pr, cr = repos
    m = servicos.cadastrar_medico(mr, "Dr House", "Infectologista")
    p = servicos.cadastrar_paciente(pr, "Maria")
    m1 = servicos.cadastrar_medico(mr, "Dr Albert", "Combinatória")
    
    inicio = datetime(2025, 12, 25, 10, 0)
    fim = datetime(2025, 12, 25, 11, 0)
    
    servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio, fim)
    
    with pytest.raises(ValueError):
        servicos.agendar_consulta(cr, mr, pr, m1.id, p.id, inicio, fim)

def test_remover_medico_com_realocacao_automatica(repos):
    mr, pr, cr = repos
    m1 = servicos.cadastrar_medico(mr, "Dr A", "Cardio")
    m2 = servicos.cadastrar_medico(mr, "Dr B", "Cardio")
    p = servicos.cadastrar_paciente(pr, "Jose")
    
    inicio = datetime(2025, 12, 25, 14, 0)
    fim = datetime(2025, 12, 25, 15, 0)
    servicos.agendar_consulta(cr, mr, pr, m1.id, p.id, inicio, fim)
    
    servicos.remover_medico(mr, cr, m1.id)
    
    consultas = cr.listar()
    assert len(consultas) == 1
    assert consultas[0].medico_id == m2.id
    assert mr.buscar_por_id(m1.id) is None

def test_remover_paciente_limpa_consultas(repos):
    mr, pr, cr = repos
    m = servicos.cadastrar_medico(mr, "Dr A", "Nutricionista")
    p = servicos.cadastrar_paciente(pr, "Jose")
    
    inicio = datetime(2025, 12, 25, 14, 0)
    fim = datetime(2025, 12, 25, 15, 0)
    servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio, fim)
    
    servicos.remover_paciente(pr, cr, p.id)
    
    assert len(cr.listar()) == 0
    assert pr.buscar_por_id(p.id) is None