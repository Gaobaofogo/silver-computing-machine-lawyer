# GLOSSARY - JudisAdvocacia (Domínio do Direito)

## Entidades do domínio

- **Cliente**: pessoa física (PF) que contrata os serviços do escritório de advocacia e é representada em um ou mais processos. **ADR-0001**: Cliente é sempre PF (`Cpf` obrigatório, `EstadoCivil` obrigatório, `CNPJ` removido). Não confundir com "lead" (potencial cliente antes da contratação) nem com "parte" no sentido estritamente processual.

- **Reclamado**: parte contrária em um processo, também chamada de "parte adversa" ou "oponente" em documentos processuais. Corresponde ao campo `Reclamado` no sistema legado.

- **Processo** (`Processos`): unidade de trabalho processual gerenciada pelo escritório. Cada processo possui número (`IdProcesso`), data de autuação (`DataAutua`), valor da causa (`ValorCausa`), área jurídica (`IdArea`), rito (`IdRito`), reclamado (`IdReclamado`) e observações (`Observa`). É o coração do sistema JudisJMD.

- **Área Jurídica** (`Area`): ramo do direito sob o qual o processo se enquadra (exemplos: Direito Civil, Direito Penal, Direito Tributário, Direito do Trabalho). Classifica a natureza jurídica do caso.

- **Rito** (`Rito`): procedimento ou modalidade processual aplicada ao processo (exemplos: rito ordinário, sumário, especial). Definido pela tabela `Rito` com nomenclatura (`Nomenclatura`).

- **Estado Civil** (`EstadoCivil`): classificação do estado civil de uma pessoa física registrada no processo (solteiro, casado, divorciado, viúvo, etc.).

## Dados sensíveis

- **CPF / CNPJ**: identificador do Cliente ou Reclamado, tratado como dado pessoal sensível sob a Lei Geral de Proteção de Dados (LGPD). No glossário, o termo "Cliente" refere-se à entidade jurídica; o campo "CPF" refere-se ao dado sensível vinculado a ela. Não confundir a entidade com o dado.

- **Observação** (`Observa`): campo livre associado a Cliente, Reclamado ou Processo, utilizado para registros internos do escritório. Pode conter informações sensíveis e deve ser tratado com cautela sob LGPD.

## Sistema legado

- **JudisJMD**: nome do sistema legado de gestão de processos, implementado em Microsoft Access (`JudisJMD.accdb`), contendo as tabelas principais acima e consultas (`QryProcessos`). A transição para web não altera a definição das entidades do domínio.

## Regras do glossário

- Este arquivo é um glossário, não uma especificação técnica nem um modelo de dados. Detalhes de implementação (ex.: React, Tailwind CSS, FastAPI, PostgreSQL, Docker) pertencem ao ADR e à documentação técnica, não a este glossário.
- Termos novos só entram quando o domínio resolve uma ambiguidade ou quando uma nova entidade é introduzida.
