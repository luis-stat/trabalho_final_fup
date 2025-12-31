import pytest
import tkinter as tk
from tkinter import messagebox
from main import AppAgendaMedica

@pytest.fixture
def app(monkeypatch):
    root = tk.Tk()
    
    def mock_showinfo(*args, **kwargs): return None
    def mock_showerror(*args, **kwargs): return None
    
    monkeypatch.setattr(messagebox, 'showinfo', mock_showinfo)
    monkeypatch.setattr(messagebox, 'showerror', mock_showerror)
    
    app = AppAgendaMedica(root)
    yield app
    root.destroy()

def test_gui_adicionar_medico(app):
    app.entry_med_nome.insert(0, "Dr Estranho")
    app.entry_med_esp.insert(0, "Cirurgião")
    
    app.add_medico()
    
    medicos = app.fachada.listar_medicos()
    assert len(medicos) == 1
    assert medicos[0].nome == "Dr Estranho"
    
    children = app.tree_medicos.get_children()
    assert len(children) == 1

def test_gui_adicionar_paciente(app):
    app.entry_pac_nome.insert(0, "Peter Parker")
    
    app.add_paciente()
    
    pacientes = app.fachada.listar_pacientes()
    assert len(pacientes) == 1
    assert pacientes[0].nome == "Peter Parker"

def test_gui_agendar_consulta_fluxo_completo(app):
    app.fachada.adicionar_medico("Dr Estranho", "Mistico")
    app.fachada.adicionar_paciente("Wong")
    
    app.entry_con_med_id.insert(0, "1")
    app.entry_con_pac_id.insert(0, "1")
    app.entry_con_data.insert(0, "20/05/2025 14:00")
    app.entry_con_duracao.insert(0, "60")
    
    app.add_consulta()
    
    consultas = app.fachada.listar_consultas_todas()
    assert len(consultas) == 1
    assert consultas[0]['medico'] == "Dr Estranho"

def test_gui_remover_medico_selecionado(app):
    app.fachada.adicionar_medico("Dr Octopus", "Cirurgião")
    app.atualizar_medicos()
    
    items = app.tree_medicos.get_children()
    app.tree_medicos.selection_set(items[0])
    
    app.del_medico()
    
    assert len(app.fachada.listar_medicos()) == 0
    assert len(app.tree_medicos.get_children()) == 0

def test_gui_remover_paciente_selecionado(app):
    app.fachada.adicionar_paciente("Mary Jane")
    app.atualizar_pacientes()
    
    items = app.tree_pacientes.get_children()
    app.tree_pacientes.selection_set(items[0])
    
    app.del_paciente()
    
    assert len(app.fachada.listar_pacientes()) == 0
    assert len(app.tree_pacientes.get_children()) == 0