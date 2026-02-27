# **Sistema de Agendamento Médico** 

## Disciplina:
 [CK0087] FUNDAMENTOS DE PROGRAMAÇÃO

## Equipe

    Ana Lismara da Silva Lopes - 580591 
    Deusdedit Teixeira de Sousa Neto - 580811 
    Luís Miguel Frazão de Sousa - 581422


---

## Sobre o Projeto

O **Sistema de Agendamento Médico** é uma aplicação que permite o gerenciamento de **médicos**, **pacientes** e **consultas**, garantindo uma solução prática e organizada para o agendamento de consultas médicas, garantindo que não ocorram conflitos de horários entre pacientes e médicos.

### Principais funcionalidades:

- Cadastro de médicos e pacientes  
- Agendamento de consultas médicas  
- Verificação de conflitos de horário  
- Remoção de médicos com realocação automática de consultas  
- Remoção de pacientes com cancelamento das consultas associadas  
- Interface gráfica para interação com o usuário  

---

## Tecnologias Utilizadas

- **Linguagem:** Python  
- **Interface Gráfica:** Tkinter  
- **Testes Automatizados:** Pytest  
- **Persistência:** Repositórios em memória  
- **Arquitetura:** Camadas (Domínio, Serviços, Infraestrutura e Interface)

---

## Estrutura do Projeto

```text

src/
 ├── app/
 │    ├── __init__.py
 │    ├── container.py
 │    └── fachada.py
 ├── dominio/
 │    ├── __init__.py
 │    ├── modelos.py
 │    ├── regras.py
 │    ├── repositorios.py
 │    └── servicos.py
 ├── infra/
 │    └── repos_memoria.py
 └── __init__.py

tests/
 ├── ponta_a_ponta/
 │    └── test_gui.py
 └── unitario/
      └── test_servicos.py

.gitignore
.python-version
HISTORY.md
README.md
main.py
pyproject.toml
uv.lock


```

## Executando o Projeto

Siga os passos abaixo para executar o sistema em seu ambiente local:

![Rodando o projeto](/rodandoProjeto.gif)

## Exemplos de uso

![Rodando o projeto](/adicionandoMedico.gif)
![Rodando o projeto](/adicionandoPaciente.gif)
![Rodando o projeto](/agendandoConsulta.gif)