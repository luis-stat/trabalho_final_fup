import pytest
import tkinter as tk
from tkinter import messagebox
from main import AppAgendaMedica
import os
import sys

@pytest.fixture
def app(monkeypatch):
    """Fixture para criar a aplicação Tkinter para testes"""
    
    def mock_showinfo(*args, **kwargs): return None
    def mock_showerror(*args, **kwargs): return None
    def mock_askyesno(*args, **kwargs): return True
    
    monkeypatch.setattr(messagebox, 'showinfo', mock_showinfo)
    monkeypatch.setattr(messagebox, 'showerror', mock_showerror)
    monkeypatch.setattr(messagebox, 'askyesno', mock_askyesno)
    
    root = None
    try:
        if sys.platform == "win32":
            import ctypes
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except:
                pass
        
        root = tk.Tk()
        root.withdraw()
        root.update_idletasks()
        
        app_instance = AppAgendaMedica(root)
        
        yield app_instance
        
    except tk.TclError as e:
        pytest.skip(f"Tkinter não disponível: {str(e)}")
    finally:
        if root:
            try:
                root.destroy()
            except:
                pass

def test_gui_adicionar_medico(app):
    """Teste para adicionar médico via GUI"""
    app.entry_med_nome.delete(0, tk.END)
    app.entry_med_esp.delete(0, tk.END)
    
    app.entry_med_nome.insert(0, "Dr Estranho")
    app.entry_med_esp.insert(0, "Cirurgião")
    
    app.add_medico()
    
    medicos = app.fachada.listar_medicos()
    assert len(medicos) == 1
    assert medicos[0].nome == "Dr Estranho"
    
    children = app.tree_medicos.get_children()
    assert len(children) == 1

def test_gui_adicionar_paciente(app):
    """Teste para adicionar paciente via GUI"""
    app.entry_pac_nome.delete(0, tk.END)
    
    app.entry_pac_nome.insert(0, "Peter Parker")
    
    app.add_paciente()
    
    pacientes = app.fachada.listar_pacientes()
    assert len(pacientes) == 1
    assert pacientes[0].nome == "Peter Parker"
    
    children = app.tree_pacientes.get_children()
    assert len(children) == 1

def test_gui_agendar_consulta_fluxo_completo(app):
    """Teste completo do fluxo de agendamento"""
    app.fachada.adicionar_medico("Dr Estranho", "Mistico")
    app.fachada.adicionar_paciente("Wong")
    
    app.atualizar_medicos()
    app.atualizar_pacientes()
    
    app.entry_con_med_id.delete(0, tk.END)
    app.entry_con_pac_id.delete(0, tk.END)
    app.entry_con_data.delete(0, tk.END)
    app.entry_con_duracao.delete(0, tk.END)
    
    app.entry_con_med_id.insert(0, "1")
    app.entry_con_pac_id.insert(0, "1")
    app.entry_con_data.insert(0, "20/05/2027 14:00")
    app.entry_con_duracao.insert(0, "60")
    
    app.add_consulta()
    
    consultas = app.fachada.listar_consultas_todas()
    assert len(consultas) == 1
    assert consultas[0]['medico'] == "Dr Estranho"
    
    children = app.tree_consultas.get_children()
    assert len(children) == 1

def test_gui_remover_medico_selecionado(app):
    """Teste para remover médico selecionado"""
    app.fachada.adicionar_medico("Dr Octopus", "Cirurgião")
    app.atualizar_medicos()
    
    items = app.tree_medicos.get_children()
    assert len(items) == 1
    app.tree_medicos.selection_set(items[0])
    
    app.del_medico()
    
    assert len(app.fachada.listar_medicos()) == 0
    assert len(app.tree_medicos.get_children()) == 0

def test_gui_remover_paciente_selecionado(app):
    """Teste para remover paciente selecionado"""
    app.fachada.adicionar_paciente("Mary Jane")
    app.atualizar_pacientes()
    
    items = app.tree_pacientes.get_children()
    assert len(items) == 1
    app.tree_pacientes.selection_set(items[0])
    
    app.del_paciente()
    
    assert len(app.fachada.listar_pacientes()) == 0
    assert len(app.tree_pacientes.get_children()) == 0

def test_gui_campos_vazios(app):
    """Teste para tentar adicionar com campos vazios"""
    medicos_iniciais = len(app.fachada.listar_medicos())
    
    app.entry_med_nome.delete(0, tk.END)
    app.entry_med_esp.delete(0, tk.END)
    app.entry_med_esp.insert(0, "Especialidade")
    
    app.add_medico()
    
    assert len(app.fachada.listar_medicos()) == medicos_iniciais