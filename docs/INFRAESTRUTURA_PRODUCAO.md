# Descrição da Infraestrutura para Implantação em Produção

## 1. Objetivo

Este documento descreve a infraestrutura necessária para disponibilizar
o **Sistema de Gerenciamento de Requisitos com Histórias de Usuário** em
um ambiente de produção. A proposta contempla os recursos de hardware,
os componentes de software e os serviços necessários para executar a
aplicação, armazenar seus dados e disponibilizá-la aos usuários com
segurança.

O projeto atualmente corresponde a um protótipo acadêmico executado em
ambiente local. Portanto, as configurações descritas neste documento
representam uma **proposta de implantação**, e não uma infraestrutura já
contratada, configurada ou homologada.

## 2. Visão geral da arquitetura

A aplicação é organizada em três camadas principais:

1.  **Apresentação:** frontend desenvolvido com React, TypeScript e
    Vite, responsável pela interface utilizada pelos usuários.
2.  **Aplicação e regras de negócio:** backend desenvolvido com FastAPI
    e Python, responsável pela autenticação, validações, processamento
    das operações e disponibilização dos endpoints da API.
3.  **Persistência:** banco de dados PostgreSQL, acessado pelo backend
    por meio do SQLAlchemy. O Alembic é utilizado para gerenciar as
    migrações da estrutura do banco.

Em uma implantação proposta, o navegador do usuário acessará o sistema
por HTTPS. Um servidor web, como o Nginx, receberá as requisições,
disponibilizará os arquivos do frontend e encaminhará as chamadas da API
ao backend FastAPI. O backend realizará as operações no PostgreSQL, que
permanecerá protegido e sem acesso público direto.

**Fluxo da arquitetura:**

Navegador do usuário → HTTPS → Nginx → Frontend React / API FastAPI →
SQLAlchemy → PostgreSQL.

## 3. Infraestrutura de hardware

Para uma primeira implantação de pequeno porte, recomenda-se utilizar
uma máquina virtual ou servidor em nuvem. A configuração inicial abaixo
é uma estimativa de referência, que deverá ser ajustada após testes de
carga e conforme a quantidade de usuários simultâneos e o volume de
dados.

  -----------------------------------------------------------------------
  Recurso                 Configuração inicial    Finalidade
                          sugerida                
  ----------------------- ----------------------- -----------------------
  Processador             2 vCPUs                 Executar o servidor web
                                                  e a aplicação backend

  Memória RAM             4 GB                    Suportar o sistema
                                                  operacional, backend e
                                                  serviços auxiliares

  Armazenamento           40 GB SSD               Armazenar sistema
                                                  operacional, aplicação,
                                                  dependências, logs e
                                                  dados operacionais

  Rede                    Conexão estável com a   Permitir acesso dos
                          internet                usuários e comunicação
                                                  com serviços
                                                  necessários

  Infraestrutura          Máquina virtual ou      Hospedar os componentes
                          servidor em nuvem       da aplicação
  -----------------------------------------------------------------------

A configuração indicada é um ponto de partida, não uma garantia de
capacidade para qualquer volume de acesso. Caso a quantidade de
usuários, requisições ou registros aumente, será necessário reavaliar
CPU, memória, armazenamento e estratégia de hospedagem. O banco de dados
também poderá ser alocado em um serviço gerenciado separado, conforme a
necessidade operacional.

## 4. Infraestrutura de software

A implantação deverá utilizar os seguintes componentes:

  -----------------------------------------------------------------------
  Componente              Tecnologia sugerida     Responsabilidade
  ----------------------- ----------------------- -----------------------
  Sistema operacional     Ubuntu Server LTS ou    Ambiente de execução
                          outra distribuição      dos serviços
                          Linux Server suportada  

  Linguagem do backend    Python 3.12             Execução das regras de
                                                  negócio

  Framework backend       FastAPI                 Disponibilização da API
                                                  REST

  Servidor ASGI           Uvicorn                 Execução da aplicação
                                                  FastAPI

  Frontend                React + TypeScript      Construção da interface
                                                  do usuário

  Ferramenta de build     Vite                    Compilação dos arquivos
                                                  estáticos do frontend

  Banco de dados          PostgreSQL 16 ou versão Persistência dos dados
                          compatível              

  Mapeamento              SQLAlchemy              Comunicação entre o
  objeto-relacional                               backend e o banco de
                                                  dados

  Migrações               Alembic                 Controle de versões e
                                                  atualização do esquema
                                                  do banco

  Servidor web / proxy    Nginx                   Recepção das
  reverso                                         requisições, entrega do
                                                  frontend e
                                                  encaminhamento à API

  Comunicação segura      TLS/HTTPS               Criptografia do tráfego
                                                  entre usuários e
                                                  sistema
  -----------------------------------------------------------------------

As versões definitivas deverão ser fixadas e documentadas no processo de
implantação, de modo a reduzir incompatibilidades e tornar as
atualizações reproduzíveis.

## 5. Serviços necessários para produção

### 5.1 Hospedagem da aplicação

Será necessário contratar ou disponibilizar um serviço de hospedagem que
forneça uma máquina virtual ou servidor com recursos compatíveis com a
demanda do sistema. Esse ambiente executará o backend e o servidor web e
armazenará os arquivos compilados do frontend, caso a arquitetura
escolhida mantenha esses componentes no mesmo servidor.

### 5.2 Banco de dados PostgreSQL

O PostgreSQL será responsável pelo armazenamento persistente de
usuários, projetos, backlogs, sprints, épicos, histórias e critérios de
aceitação.

O serviço de banco de dados deverá:

-   Permitir conexões apenas a partir dos componentes autorizados;
-   Utilizar credenciais próprias e fortes para a aplicação;
-   Manter os dados em armazenamento persistente;
-   Possuir rotina de backup e procedimento de restauração;
-   Receber atualizações de segurança e manutenção.

O PostgreSQL não deverá ficar diretamente exposto à internet. Em uma
arquitetura com banco gerenciado, devem ser configuradas regras de rede
que permitam o acesso somente ao backend.

### 5.3 Servidor web e proxy reverso

O Nginx poderá atuar como ponto de entrada da aplicação. Suas
responsabilidades serão disponibilizar os arquivos estáticos do
frontend, encaminhar as requisições destinadas à API para o FastAPI e
aplicar configurações básicas de comunicação e segurança.

### 5.4 Domínio e DNS

Para acesso público, deverá ser registrado ou disponibilizado um
domínio. O serviço de DNS deverá direcionar esse domínio para o endereço
público do servidor ou para o serviço de hospedagem utilizado.

### 5.5 Certificado TLS e HTTPS

A aplicação deverá utilizar HTTPS para proteger as informações
transmitidas entre o navegador e o servidor. Para isso, será necessário
configurar um certificado TLS válido e renovar esse certificado dentro
do prazo estabelecido pelo emissor.

Como a aplicação utiliza cookies de sessão, a configuração de produção
deverá habilitar cookies seguros, incluindo `COOKIE_SECURE=true`, quando
o sistema estiver sendo acessado por HTTPS.

### 5.6 Backup e recuperação

Deverá existir uma rotina de cópias de segurança do banco PostgreSQL,
com armazenamento protegido e separado do ambiente principal sempre que
possível. Também será necessário definir a periodicidade dos backups, o
tempo de retenção e realizar testes de restauração para verificar se os
dados podem ser recuperados.

### 5.7 Monitoramento e registros

A operação deverá contar com mecanismos para acompanhar a
disponibilidade da aplicação, o consumo de CPU, memória e armazenamento,
além de registrar erros do backend e falhas de conexão com o banco. Os
registros deverão ser protegidos e mantidos por período compatível com
as necessidades de suporte e auditoria.

### 5.8 Gerenciamento de segredos

As credenciais do banco, a chave `APP_SECRET_KEY` e outros dados
sensíveis deverão ser fornecidos por variáveis de ambiente ou por um
serviço próprio de gerenciamento de segredos. Esses valores não deverão
ser incluídos no código-fonte, em imagens públicas ou em repositórios de
código.

## 6. Segurança e operação

Antes da disponibilização pública, deverão ser realizadas configurações
e verificações adicionais, incluindo:

-   Restringir as portas de rede às estritamente necessárias;
-   Impedir o acesso público direto ao PostgreSQL;
-   Utilizar HTTPS em todas as conexões externas;
-   Configurar corretamente cookies de sessão e proteção CSRF;
-   Manter sistema operacional, bibliotecas e dependências atualizados;
-   Aplicar controles contra tentativas repetidas de autenticação;
-   Revisar permissões de usuários e acesso aos recursos;
-   Proteger arquivos de configuração e segredos;
-   Configurar backups e testar a recuperação;
-   Executar testes funcionais, de integração, segurança e carga em
    ambiente equivalente ao de produção.

A autenticação, o controle de acesso, o armazenamento seguro de senhas e
a proteção CSRF já fazem parte das funcionalidades descritas para o
protótipo. Ainda assim, a presença desses mecanismos não elimina a
necessidade de uma revisão de segurança antes da implantação real.

## 7. Processo proposto de implantação

Uma sequência possível para a implantação é:

1.  Provisionar o servidor ou serviço de hospedagem com os recursos
    definidos.
2.  Instalar e atualizar o sistema operacional e os componentes de
    software.
3.  Criar e configurar o banco PostgreSQL com acesso restrito.
4.  Configurar as variáveis de ambiente e os segredos da aplicação.
5.  Executar as migrações do Alembic para preparar o esquema do banco.
6.  Compilar o frontend e disponibilizar seus arquivos estáticos.
7.  Iniciar o backend FastAPI como serviço gerenciado pelo sistema
    operacional ou pela plataforma de hospedagem.
8.  Configurar o Nginx, o domínio, o DNS e o certificado TLS.
9.  Executar testes de funcionamento, integração, autenticação e
    persistência com PostgreSQL.
10. Configurar backups, monitoramento e procedimentos de atualização e
    recuperação.

## 8. Dimensionamento, custos e limitações

Os recursos apresentados são estimativas iniciais e não representam uma
medição de desempenho em produção. A escolha do provedor, os custos de
hospedagem, o dimensionamento definitivo e os níveis de disponibilidade
deverão ser definidos conforme orçamento, número de usuários, volume de
dados e requisitos institucionais.

O protótipo ainda necessita de homologação com PostgreSQL em ambiente de
implantação, compilação e verificação final do frontend, testes de
carga, revisão de segurança e validação dos procedimentos operacionais.
Os resultados de testes realizados com SQLite temporário não devem ser
considerados comprovação de desempenho do PostgreSQL em produção.

## 9. Conclusão

A infraestrutura proposta contempla os recursos de hardware, software e
serviços necessários para uma possível implantação do Sistema de
Gerenciamento de Requisitos com Histórias de Usuário. A arquitetura
separa apresentação, processamento e persistência, utiliza PostgreSQL
para armazenamento e prevê hospedagem, domínio, HTTPS, backup,
monitoramento e gerenciamento seguro de credenciais.

Dessa forma, este documento descreve uma proposta de infraestrutura para
produção, sem afirmar que o protótipo acadêmico já esteja hospedado ou
pronto para exposição pública.
