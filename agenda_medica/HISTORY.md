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