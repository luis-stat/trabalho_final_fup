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
    medico = servicos.cadastrar_medico(mr, "Médico A", "Especialidade A")
    assert medico.id == 1
    assert medico.nome == "Médico A"
    assert len(mr.listar()) == 1

def test_validacao_nome_medico_numeros(repos):
    mr, _, _ = repos
    with pytest.raises(ValueError):
        servicos.cadastrar_medico(mr, "Médico 10", "Infectologista")

def test_agendar_consulta_sucesso(repos):
    mr, pr, cr = repos
    m = servicos.cadastrar_medico(mr, "Dr House", "Infectologista")
    p = servicos.cadastrar_paciente(pr, "Maria")
    
    inicio = datetime(2027, 12, 25, 10, 0)
    fim = inicio + timedelta(hours=1)
    
    consulta = servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio, fim)
    assert consulta.id == 1
    assert consulta.medico_id == m.id

def test_impedir_agendamento_conflitante(repos):
    mr, pr, cr = repos
    m = servicos.cadastrar_medico(mr, "Dr House", "Infectologista")
    p = servicos.cadastrar_paciente(pr, "Maria")
    
    inicio = datetime(2027, 12, 25, 10, 0)
    fim = datetime(2027, 12, 25, 11, 0)
    servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio, fim)
    
    inicio_conflito = datetime(2027, 12, 25, 10, 30)
    fim_conflito = datetime(2027, 12, 25, 11, 30)
    
    with pytest.raises(ValueError):
        servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio_conflito, fim_conflito)

def test_impedir_agendamento_erroneo_pac(repos):
    mr, pr, cr = repos
    m = servicos.cadastrar_medico(mr, "Dr House", "Infectologista")
    p = servicos.cadastrar_paciente(pr, "Maria")
    
    inicio = datetime(2027, 12, 25, 10, 0)
    fim = datetime(2027, 12, 25, 11, 0)
    servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio, fim)
    
    with pytest.raises(ValueError):
        servicos.agendar_consulta(cr, mr, pr, m.id, 2, inicio, fim)

def test_impedir_agendamento_erroneo_med(repos):
    mr, pr, cr = repos
    m = servicos.cadastrar_medico(mr, "Dr House", "Infectologista")
    p = servicos.cadastrar_paciente(pr, "Maria")
    
    inicio = datetime(2027, 12, 25, 10, 0)
    fim = datetime(2027, 12, 25, 11, 0)
    servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio, fim)
    
    with pytest.raises(ValueError):
        servicos.agendar_consulta(cr, mr, pr, 2, p.id, inicio, fim)

def test_impedir_conflitante_med(repos):
    mr, pr, cr = repos
    m = servicos.cadastrar_medico(mr, "Dr House", "Infectologista")
    p = servicos.cadastrar_paciente(pr, "Maria")
    p1 = servicos.cadastrar_paciente(pr, "José")
    
    inicio = datetime(2027, 12, 25, 10, 0)
    fim = datetime(2027, 12, 25, 11, 0)
    
    servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio, fim)
    
    with pytest.raises(ValueError):
        servicos.agendar_consulta(cr, mr, pr, m.id, p1.id, inicio, fim)

def test_impedir_conflitante_pac(repos):
    mr, pr, cr = repos
    m = servicos.cadastrar_medico(mr, "Dr House", "Infectologista")
    p = servicos.cadastrar_paciente(pr, "Maria")
    m1 = servicos.cadastrar_medico(mr, "Dr Albert", "Combinatória")
    
    inicio = datetime(2027, 12, 25, 10, 0)
    fim = datetime(2027, 12, 25, 11, 0)
    
    servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio, fim)
    
    with pytest.raises(ValueError):
        servicos.agendar_consulta(cr, mr, pr, m1.id, p.id, inicio, fim)

def test_remover_medico_com_realocacao_automatica(repos):
    mr, pr, cr = repos
    m1 = servicos.cadastrar_medico(mr, "Dr A", "Cardio")
    m2 = servicos.cadastrar_medico(mr, "Dr B", "Cardio")
    p = servicos.cadastrar_paciente(pr, "Jose")
    
    inicio = datetime(2027, 12, 25, 14, 0)
    fim = datetime(2027, 12, 25, 15, 0)
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
    
    inicio = datetime(2027, 12, 25, 14, 0)
    fim = datetime(2027, 12, 25, 15, 0)
    servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio, fim)
    
    servicos.remover_paciente(pr, cr, p.id)
    
    assert len(cr.listar()) == 0
    assert pr.buscar_por_id(p.id) is None

def test_buscar_medico_sucesso(repos):
    mr, _, _ = repos
    m = servicos.cadastrar_medico(mr, "Dr Strange", "Místico")
    
    encontrado = servicos.buscar_medico(mr, m.id)
    assert encontrado is not None
    assert encontrado.nome == "Dr Strange"
    assert encontrado.id == m.id

    assert servicos.buscar_medico(mr, 999) is None

def test_buscar_paciente_sucesso(repos):
    _, pr, _ = repos
    p = servicos.cadastrar_paciente(pr, "Bruce Banner")
    
    encontrado = servicos.buscar_paciente(pr, p.id)
    assert encontrado is not None
    assert encontrado.nome == "Bruce Banner"
    assert encontrado.id == p.id

    assert servicos.buscar_paciente(pr, 999) is None

def test_buscar_consultas_sucesso(repos):
    mr, pr, cr = repos
    m = servicos.cadastrar_medico(mr, "Dr House", "Infecto")
    p = servicos.cadastrar_paciente(pr, "Wilson")
    
    inicio = datetime(2027, 1, 1, 10, 0)
    fim = datetime(2027, 1, 1, 11, 0)
    c = servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio, fim)
    
    encontrado = servicos.buscar_consulta(cr, c.id)
    assert encontrado is not None
    assert encontrado.id == c.id
    assert encontrado.medico_id == m.id

    assert servicos.buscar_consulta(cr, 999) is None

def test_cancelar_consultas_sucesso(repos):
    mr, pr, cr = repos
    m = servicos.cadastrar_medico(mr, "Dr House", "Infecto")
    p = servicos.cadastrar_paciente(pr, "Wilson")
    
    inicio = datetime(2027, 1, 1, 10, 0)
    fim = datetime(2027, 1, 1, 11, 0)
    c = servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio, fim)
    
    assert len(cr.listar()) == 1
    
    sucesso = servicos.cancelar_consulta(cr, c.id)
    assert sucesso is True
    
    assert len(cr.listar()) == 0
    assert servicos.buscar_consulta(cr, c.id) is None
    
    assert servicos.cancelar_consulta(cr, 999) is False

def test_remarcar_consulta_sucesso(repos):
    mr, pr, cr = repos
    m1 = servicos.cadastrar_medico(mr, "Dr House", "Infecto")
    m2 = servicos.cadastrar_medico(mr, "Dr Wilson", "Onco")
    p = servicos.cadastrar_paciente(pr, "Thirteen")
    
    inicio = datetime(2027, 5, 20, 10, 0)
    fim = datetime(2027, 5, 20, 11, 0)
    consulta = servicos.agendar_consulta(cr, mr, pr, m1.id, p.id, inicio, fim)
    
    novo_inicio = datetime(2027, 5, 21, 14, 0)
    
    consulta_remarcada = servicos.remarcar_consulta(cr, mr, consulta.id, m2.id, novo_inicio)
    
    assert consulta_remarcada.medico_id == m2.id
    assert consulta_remarcada.inicio == novo_inicio
    assert consulta_remarcada.fim == datetime(2027, 5, 21, 15, 0)

def test_remarcar_consulta_data_passada(repos):
    mr, pr, cr = repos
    m = servicos.cadastrar_medico(mr, "Dr House", "Infecto")
    p = servicos.cadastrar_paciente(pr, "Thirteen")
    
    inicio = datetime(2027, 5, 20, 10, 0)
    fim = datetime(2027, 5, 20, 11, 0)
    consulta = servicos.agendar_consulta(cr, mr, pr, m.id, p.id, inicio, fim)
    
    data_passada = datetime(2000, 1, 1, 10, 0)
    
    with pytest.raises(ValueError) as excinfo:
        servicos.remarcar_consulta(cr, mr, consulta.id, m.id, data_passada)
    assert "datas passadas" in str(excinfo.value)

def test_remarcar_consulta_conflito_medico(repos):
    mr, pr, cr = repos
    m1 = servicos.cadastrar_medico(mr, "Dr House", "Infecto")
    m2 = servicos.cadastrar_medico(mr, "Dr Wilson", "Onco")
    p = servicos.cadastrar_paciente(pr, "Thirteen")
    p2 = servicos.cadastrar_paciente(pr, "Foreman")
    
    inicio1 = datetime(2027, 6, 1, 10, 0)
    fim1 = datetime(2027, 6, 1, 11, 0)
    c1 = servicos.agendar_consulta(cr, mr, pr, m1.id, p.id, inicio1, fim1)
    
    servicos.agendar_consulta(cr, mr, pr, m2.id, p2.id, datetime(2027, 6, 2, 10, 0), datetime(2027, 6, 2, 11, 0))
    
    novo_inicio = datetime(2027, 6, 2, 10, 0)
    
    with pytest.raises(ValueError) as excinfo:
        servicos.remarcar_consulta(cr, mr, c1.id, m2.id, novo_inicio)
    assert "O médico já possui uma consulta" in str(excinfo.value)

def test_remarcar_consulta_conflito_paciente(repos):
    mr, pr, cr = repos
    m1 = servicos.cadastrar_medico(mr, "Dr House", "Infecto")
    m2 = servicos.cadastrar_medico(mr, "Dr Wilson", "Onco")
    p = servicos.cadastrar_paciente(pr, "Thirteen")
    
    c1 = servicos.agendar_consulta(cr, mr, pr, m1.id, p.id, datetime(2027, 7, 1, 10, 0), datetime(2027, 7, 1, 11, 0))
    
    servicos.agendar_consulta(cr, mr, pr, m2.id, p.id, datetime(2027, 7, 2, 10, 0), datetime(2027, 7, 2, 11, 0))
    
    novo_inicio = datetime(2027, 7, 2, 10, 0)
    
    with pytest.raises(ValueError) as excinfo:
        servicos.remarcar_consulta(cr, mr, c1.id, m1.id, novo_inicio)
    assert "O paciente já possui uma consulta" in str(excinfo.value)