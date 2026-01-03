import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.app.fachada import FachadaSistema

class AppAgendaMedica:
    def __init__(self, root):
        self.fachada = FachadaSistema()
        self.root = root
        self.root.title("Sistema de Agenda Médica")
        self.root.geometry("800x600")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self._criar_aba_medicos()
        self._criar_aba_pacientes()
        self._criar_aba_consultas()

    def _criar_aba_medicos(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Médicos")

        frame_inputs = ttk.Frame(frame)
        frame_inputs.pack(side='top', fill='x', padx=10, pady=10)

        ttk.Label(frame_inputs, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_med_nome = ttk.Entry(frame_inputs, width=40)
        self.entry_med_nome.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(frame_inputs, text="Especialidade:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_med_esp = ttk.Entry(frame_inputs, width=40)
        self.entry_med_esp.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        btn_add = ttk.Button(frame_inputs, text="Salvar Médico", command=self.add_medico)
        btn_add.grid(row=2, column=0, columnspan=2, pady=10)

        frame_lista = ttk.Frame(frame)
        frame_lista.pack(side='bottom', fill='both', expand=True, padx=10, pady=10)

        columns = ('id', 'nome', 'especialidade')
        self.tree_medicos = ttk.Treeview(frame_lista, columns=columns, show='headings')
        self.tree_medicos.heading('id', text='ID')
        self.tree_medicos.heading('nome', text='Nome')
        self.tree_medicos.heading('especialidade', text='Especialidade')
        
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_medicos.yview)
        self.tree_medicos.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.tree_medicos.pack(side='left', fill='both', expand=True)
        
        frame_botoes = ttk.Frame(frame)
        frame_botoes.pack(pady=5)
        
        btn_del = ttk.Button(frame_botoes, text="Remover Selecionado", command=self.del_medico)
        btn_del.pack(side='left', padx=5)
        
        btn_search = ttk.Button(frame_botoes, text="Buscar por ID", command=self.buscar_medico)
        btn_search.pack(side='left', padx=5)

    def _criar_aba_pacientes(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Pacientes")

        frame_inputs = ttk.Frame(frame)
        frame_inputs.pack(side='top', fill='x', padx=10, pady=10)

        ttk.Label(frame_inputs, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_pac_nome = ttk.Entry(frame_inputs, width=40)
        self.entry_pac_nome.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        btn_add = ttk.Button(frame_inputs, text="Salvar Paciente", command=self.add_paciente)
        btn_add.grid(row=1, column=0, columnspan=2, pady=10)

        frame_lista = ttk.Frame(frame)
        frame_lista.pack(side='bottom', fill='both', expand=True, padx=10, pady=10)

        columns = ('id', 'nome')
        self.tree_pacientes = ttk.Treeview(frame_lista, columns=columns, show='headings')
        self.tree_pacientes.heading('id', text='ID')
        self.tree_pacientes.heading('nome', text='Nome')
        
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_pacientes.yview)
        self.tree_pacientes.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.tree_pacientes.pack(side='left', fill='both', expand=True)

        frame_botoes = ttk.Frame(frame)
        frame_botoes.pack(pady=5)

        btn_del = ttk.Button(frame_botoes, text="Remover Selecionado", command=self.del_paciente)
        btn_del.pack(side='left', padx=5)

        btn_search = ttk.Button(frame_botoes, text="Buscar por ID", command=self.buscar_paciente)
        btn_search.pack(side='left', padx=5)

    def _criar_aba_consultas(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Consultas")

        frame_inputs = ttk.Frame(frame)
        frame_inputs.pack(side='top', fill='x', padx=10, pady=10)

        ttk.Label(frame_inputs, text="ID Médico:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_con_med_id = ttk.Entry(frame_inputs)
        self.entry_con_med_id.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(frame_inputs, text="ID Paciente:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_con_pac_id = ttk.Entry(frame_inputs)
        self.entry_con_pac_id.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(frame_inputs, text="Data (dd/mm/aaaa HH:MM):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_con_data = ttk.Entry(frame_inputs)
        self.entry_con_data.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(frame_inputs, text="Duração (min):").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.entry_con_duracao = ttk.Entry(frame_inputs)
        self.entry_con_duracao.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        btn_add = ttk.Button(frame_inputs, text="Agendar Consulta", command=self.add_consulta)
        btn_add.grid(row=4, column=0, columnspan=2, pady=15)

        frame_lista = ttk.Frame(frame)
        frame_lista.pack(side='bottom', fill='both', expand=True, padx=10, pady=10)

        columns = ('id', 'medico', 'paciente', 'inicio', 'fim')
        self.tree_consultas = ttk.Treeview(frame_lista, columns=columns, show='headings')
        self.tree_consultas.heading('id', text='ID')
        self.tree_consultas.heading('medico', text='Médico')
        self.tree_consultas.heading('paciente', text='Paciente')
        self.tree_consultas.heading('inicio', text='Início')
        self.tree_consultas.heading('fim', text='Fim')
        
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_consultas.yview)
        self.tree_consultas.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.tree_consultas.pack(side='left', fill='both', expand=True)
        
        frame_botoes = ttk.Frame(frame)
        frame_botoes.pack(pady=5)
        
        btn_refresh = ttk.Button(frame_botoes, text="Atualizar Lista", command=self.atualizar_consultas)
        btn_refresh.pack(side='left', padx=5)

        btn_cancel = ttk.Button(frame_botoes, text="Cancelar Selecionada", command=self.cancelar_consulta)
        btn_cancel.pack(side='left', padx=5)

        btn_reschedule = ttk.Button(frame_botoes, text="Remarcar Selecionada", command=self.remarcar_consulta)
        btn_reschedule.pack(side='left', padx=5)

        btn_search = ttk.Button(frame_botoes, text="Buscar por ID", command=self.buscar_consulta)
        btn_search.pack(side='left', padx=5)

    def add_medico(self):
        try:
            self.fachada.adicionar_medico(self.entry_med_nome.get(), self.entry_med_esp.get())
            self.atualizar_medicos()
            self.entry_med_nome.delete(0, tk.END)
            self.entry_med_esp.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Médico adicionado!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def del_medico(self):
        selected = self.tree_medicos.selection()
        if selected:
            item = self.tree_medicos.item(selected[0])
            id_med = int(item['values'][0])
            if self.fachada.remover_medico(id_med):
                self.atualizar_medicos()
                self.atualizar_consultas()
                messagebox.showinfo("Sucesso", "Médico removido e consultas processadas.")
            else:
                messagebox.showerror("Erro", "Médico não encontrado ou erro na remoção.")

    def buscar_medico(self):
        id_med = simpledialog.askinteger("Buscar Médico", "Digite o ID do médico:")
        if id_med:
            medico = self.fachada.buscar_medico(id_med)
            if medico:
                messagebox.showinfo("Médico Encontrado", f"ID: {medico.id}\nNome: {medico.nome}\nEspecialidade: {medico.especialidade}")
            else:
                messagebox.showwarning("Atenção", "Médico não encontrado.")

    def atualizar_medicos(self):
        for i in self.tree_medicos.get_children():
            self.tree_medicos.delete(i)
        for m in self.fachada.listar_medicos():
            self.tree_medicos.insert('', tk.END, values=(m.id, m.nome, m.especialidade))

    def add_paciente(self):
        try:
            self.fachada.adicionar_paciente(self.entry_pac_nome.get())
            self.atualizar_pacientes()
            self.entry_pac_nome.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Paciente adicionado!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def del_paciente(self):
        selected = self.tree_pacientes.selection()
        if selected:
            item = self.tree_pacientes.item(selected[0])
            id_pac = int(item['values'][0])
            if self.fachada.remover_paciente(id_pac):
                self.atualizar_pacientes()
                self.atualizar_consultas()
                messagebox.showinfo("Sucesso", "Paciente removido e consultas processadas.")
            else:
                messagebox.showerror("Erro", "Paciente não encontrado ou erro na remoção.")

    def buscar_paciente(self):
        id_pac = simpledialog.askinteger("Buscar Paciente", "Digite o ID do paciente:")
        if id_pac:
            paciente = self.fachada.buscar_paciente(id_pac)
            if paciente:
                messagebox.showinfo("Paciente Encontrado", f"ID: {paciente.id}\nNome: {paciente.nome}")
            else:
                messagebox.showwarning("Atenção", "Paciente não encontrado.")

    def atualizar_pacientes(self):
        for i in self.tree_pacientes.get_children():
            self.tree_pacientes.delete(i)
        for p in self.fachada.listar_pacientes():
            self.tree_pacientes.insert('', tk.END, values=(p.id, p.nome))

    def add_consulta(self):
        try:
            med_str = self.entry_con_med_id.get()
            pac_str = self.entry_con_pac_id.get()
            dur_str = self.entry_con_duracao.get()
            data_str = self.entry_con_data.get()

            if not med_str or not pac_str or not dur_str or not data_str:
                raise ValueError("Preencha todos os campos da consulta!")

            med_id = int(med_str)
            pac_id = int(pac_str)
            duracao = int(dur_str)
            
            self.fachada.agendar_consulta(med_id, pac_id, data_str, duracao)
            self.atualizar_consultas()
            messagebox.showinfo("Sucesso", "Consulta agendada!")
        except ValueError as ve:
            messagebox.showerror("Erro de Validação", str(ve))
        except Exception as e:
            messagebox.showerror("Erro Técnico", str(e))

    def cancelar_consulta(self):
        selected = self.tree_consultas.selection()
        if selected:
            item = self.tree_consultas.item(selected[0])
            id_con = int(item['values'][0])
            if self.fachada.cancelar_consulta(id_con):
                self.atualizar_consultas()
                messagebox.showinfo("Sucesso", "Consulta cancelada.")
            else:
                messagebox.showerror("Erro", "Erro ao cancelar a consulta.")

    def remarcar_consulta(self):
        selected = self.tree_consultas.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma consulta para remarcar.")
            return

        item = self.tree_consultas.item(selected[0])
        id_con = int(item['values'][0])
        
        win = tk.Toplevel(self.root)
        win.title("Remarcar Consulta")
        win.geometry("400x300")
        
        tk.Label(win, text="Novo ID do Médico:").pack(pady=5)
        entry_med = tk.Entry(win)
        entry_med.pack(pady=5)
        
        tk.Label(win, text="Nova Data (dd/mm/aaaa HH:MM):").pack(pady=5)
        entry_data = tk.Entry(win)
        entry_data.pack(pady=5)
        
        def confirmar():
            try:
                novo_med_str = entry_med.get()
                nova_data_str = entry_data.get()
                
                if not novo_med_str or not nova_data_str:
                    raise ValueError("Preencha todos os campos.")
                
                novo_med_id = int(novo_med_str)
                
                self.fachada.remarcar_consulta(id_con, novo_med_id, nova_data_str)
                self.atualizar_consultas()
                messagebox.showinfo("Sucesso", "Consulta remarcada!")
                win.destroy()
            except ValueError as ve:
                messagebox.showerror("Erro de Validação", str(ve))
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        
        tk.Button(win, text="Confirmar", command=confirmar).pack(pady=15)

    def buscar_consulta(self):
        id_con = simpledialog.askinteger("Buscar Consulta", "Digite o ID da consulta:")
        if id_con:
            consulta = self.fachada.buscar_consulta(id_con)
            if consulta:
                messagebox.showinfo("Consulta Encontrada", f"ID: {consulta.id}\nID Médico: {consulta.medico_id}\nID Paciente: {consulta.paciente_id}\nInício: {consulta.inicio}\nFim: {consulta.fim}")
            else:
                messagebox.showwarning("Atenção", "Consulta não encontrada.")

    def atualizar_consultas(self):
        for i in self.tree_consultas.get_children():
            self.tree_consultas.delete(i)
        for c in self.fachada.listar_consultas_todas():
            self.tree_consultas.insert('', tk.END, values=(
                c['id'], c['medico'], c['paciente'], c['inicio'], c['fim']
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = AppAgendaMedica(root)
    root.mainloop()