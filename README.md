# MovieMi

## Escopo do Projeto

O **Movie Data Migration** é um projeto desenvolvido para realizar migrações de dados a partir de arquivos CSV e armazená-los em um banco de dados. O objetivo é facilitar a inserção e o gerenciamento de informações relacionadas a filmes, além de fornecer funcionalidades para monitorar o progresso das migrações. As principais funcionalidades incluem:

- **Visualização das Informações da Migração**: Exibe detalhes como o arquivo utilizado, tempo de processamento, número de erros, quantidade de dados inseridos e tabela de destino.
- **Detalhes dos Filmes**: Permite a visualização de filmes cadastrados com detalhes adicionais fornecidos por uma API.
- **Filtragem e Paginação**: Oferece a capacidade de filtrar e paginar a lista de filmes.

## Referência do Dataset

O projeto utiliza o [MovieLens 20M Dataset](https://grouplens.org/datasets/movielens/20m/), que é um conjunto de dados amplamente utilizado para recomendações de filmes e análises de dados de usuários.

## Tecnologias Utilizadas

- **Django**: Framework web para desenvolvimento rápido e robusto de aplicações web.
- **Redis**: Banco de dados em memória, utilizado para cache e gerenciamento de sessões.
- **Celery**: Biblioteca para processamento assíncrono de tarefas, facilitando a execução de tarefas em segundo plano.

## Passos Seguidos

1. **Criação de Inserções de Dados**: Utilização de SQL nativo e o método `executemany` do Django para otimizar a inserção de grandes volumes de dados no banco.
2. **Validação de Dados**: Implementação de validações rigorosas para garantir a integridade dos dados importados.
3. **Registro de Dados de Migração**: Desenvolvimento de uma funcionalidade para registrar e monitorar o progresso das migrações.
4. **Configuração do Celery e Redis**: Integração do Celery e Redis para gerenciar tarefas assíncronas de processamento de dados.
5. **Criação de Interfaces de Upload e Listagem**: Desenvolvimento de telas para upload de arquivos, visualização dos dados de migração e listagem de filmes com filtros e paginação.

## Diagrama Lógico

*Espaço para inserir imagem*
![movie_data_migration](https://github.com/user-attachments/assets/dc94d6a0-a590-4e8a-a88e-f391b991141b)
