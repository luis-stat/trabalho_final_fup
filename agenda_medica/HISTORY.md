# Histórico de Commits

Todas as mudanças significativas neste projeto serão documentadas neste arquivo.

## v0.1.0

- Configuração inicial do projeto com `pyproject.toml` definindo `requires-python = ">=3.13"`.
- Estruturação do layout do projeto utilizando o diretório `src/` para separar o código fonte.
- Criação da camada de domínio em `src/dominio` contendo:
  - `modelos.py`: Definição das entidades `Medico`, `Paciente` e `Consulta` utilizando _dataclasses_, com validações no `__post_init__` (tipos, IDs positivos, strings não vazias e consistência de datas).
  - `repositorios.py`: Interfaces abstratas (`MedicoRepository`, `PacienteRepository`, `ConsultaRepository`) definindo os contratos de persistência.
  - `regras.py`: Implementação do `ServicoDeAgendamento` encapsulando a lógica de negócio, incluindo a verificação de existência de entidades e validação de sobreposição de horários (`_verificar_sobreposicao`).
- Criação da camada de infraestrutura em `src/infra` contendo:
  - `repos_memoria.py`: Implementação de repositórios em memória utilizando Generics (`BaseRepositoryMemoria[T]`), provendo operações de adicionar, buscar por ID, listar, remover e geração sequencial de IDs.
- Adicionado `main.py` na raiz do pacote como ponto de entrada inicial da aplicação.
- Configuração de arquivos auxiliares `.gitignore` e `.python-version`.

## v0.2.0

- Implementação da camada de aplicação em `src/app`:
  - `container.py`: Configuração de injeção de dependência, instanciando os repositórios em memória e o serviço de agendamento.
  - `fachada.py`: Criação de uma fachada (`FachadaSistema`) para simplificar a comunicação entre a interface gráfica e o domínio, tratando a conversão de tipos primitivos e chamadas ao container.
- Desenvolvimento de interface gráfica (GUI) utilizando **Tkinter** no arquivo `main.py`, estruturada com abas para gerenciamento de médicos, pacientes e consultas, incluindo visualização em lista e formulários de entrada.
- Evolução das regras de negócio em `src/dominio/regras.py`:
  - Implementação do método `remover_medico_e_consultas`.
  - Adição de lógica de realocação: ao remover um médico, o sistema busca substitutos da mesma especialidade. Se houver disponibilidade de horário, a consulta é transferida; caso contrário, é cancelada.