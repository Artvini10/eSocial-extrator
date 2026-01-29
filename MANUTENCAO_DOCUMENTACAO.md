# 📋 Como Manter a Documentação Atualizada

## Overview

Este projeto inclui scripts automatizados para manter a documentação Word sincronizada com as mudanças no código. **Não crie novas versões** - os scripts atualizam os documentos existentes in-place.

## Documentos Monitorados

### 🇬🇧 English Version
- **Arquivo:** `eSocial_Extractor_Documentation.docx`
- **Script de Atualização:** `update_documentation_en.py`
- **Conteúdo:** Arquitetura, componentes, padrões, deployment

### 🇧🇷 Portuguese Version  
- **Arquivo:** `eSocial_Extractor_Documentacao_PTBR.docx`
- **Script de Atualização:** `update_documentation_ptbr.py`
- **Conteúdo:** Mesma estrutura em português brasileiro

## Como Atualizar a Documentação

### Opção 1: Atualizar Ambos (Recomendado)

```bash
python update_all_documentation.py
```

Isso atualiza ambos os documentos em uma única execução, mantendo sincronização perfeita.

### Opção 2: Atualizar Apenas Inglês

```bash
python update_documentation_en.py
```

### Opção 3: Atualizar Apenas Português

```bash
python update_documentation_ptbr.py
```

## O que é Atualizado

Cada execução dos scripts atualiza:

✅ **Estatísticas do Código**
- Número total de arquivos
- Total de linhas de código
- Listagem de módulos ativos

✅ **Informações de Versão**
- Data e hora da última atualização
- Hash do commit mais recente
- Mensagem do último commit

✅ **Metadados**
- Timestamp de atualização (ISO 8601 ou DD/MM/YYYY)
- Status Git atual

## Workflow Recomendado

### Após Implementar Novas Features

```bash
# 1. Commit suas mudanças
git add .
git commit -m "Implement new feature X"

# 2. Atualizar documentação
python update_all_documentation.py

# 3. Fazer commit da documentação atualizada
git add eSocial_Extractor_Documentation.docx
git add eSocial_Extractor_Documentacao_PTBR.docx
git commit -m "Update documentation for feature X"

# 4. Push para GitHub
git push origin main
```

### Após Bug Fixes Significativos

```bash
git commit -m "Fix critical bug in orchestrator"
python update_all_documentation.py
git add *.docx
git commit -m "Update docs for bug fix"
git push
```

### Antes de Releases

```bash
# Executar antes de marcar uma release
python update_all_documentation.py
git add *.docx
git commit -m "Final documentation update for v1.0.0"
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags
```

## Estrutura Dos Scripts

### `update_documentation_en.py` | `update_documentation_ptbr.py`

Cada script realiza:

```python
1. Abre o documento Word existente
2. Coleta estatísticas atuais do código
3. Obtém informações do Git (último commit)
4. Atualiza seções de estatísticas
5. Adiciona timestamp de atualização
6. Salva o arquivo (sem criar nova versão)
```

### `update_all_documentation.py`

Master script que:
- Executa ambos os scripts de atualização sequencialmente
- Fornece relatório consolidado
- Monitora sucessos/falhas
- Retorna status de saída apropriado (0 = sucesso, 1 = falha)

## O Que NÃO é Atualizado

Os scripts preservam intentionalmente:

❌ Conteúdo de seções principais (Arquitetura, Componentes, etc.)
❌ Exemplos de código
❌ Histórico de mudanças
❌ Estrutura e formatação geral
❌ Imagens e diagramas

**Por quê?** Para manter a qualidade e contexto da documentação principal. Se o conteúdo substantivo mudar, edite o documento manualmente e/ou recrie geradores mais avançados.

## Personalizações Futuras

Para adicionar mais campos de atualização automática:

1. **Abrir e editar** `update_documentation_en.py`
2. **Adicionar lógica** na função `update_documentation()`
3. **Usar python-docx** para encontrar e modificar parágrafos/tabelas
4. **Replicar mudanças** em `update_documentation_ptbr.py`
5. **Testar** com `python update_all_documentation.py`

Exemplo:
```python
# Find a specific section and update it
for para in doc.paragraphs:
    if "API Endpoints" in para.text:
        # Update next paragraph with current endpoints
        # ...
```

## Automatização com Git Hooks (Avançado)

Para atualizar documentação automaticamente antes de cada commit:

1. **Criar arquivo** `.git/hooks/pre-commit`
2. **Adicionar script:**
```bash
#!/bin/bash
python update_all_documentation.py
git add eSocial_Extractor_Documentation.docx
git add eSocial_Extractor_Documentacao_PTBR.docx
```
3. **Tornar executável:** `chmod +x .git/hooks/pre-commit`

Assim, toda vez que você fazer `git commit`, a documentação é atualizada automaticamente.

## Troubleshooting

### ❓ "Document not found"
- Verifique se os arquivos `.docx` existem no diretório raiz
- Confirme os nomes estão corretos

### ❓ "Error updating documentation"
- Verifique se `python-docx` está instalado: `pip install python-docx`
- Confirme que o documento não está aberto em Word
- Verifique permissões de escrita no diretório

### ❓ "Git Status: N/A"
- Pode ocorrer se não houver commits ou acesso ao git
- Isso não bloqueia a atualização - apenas não mostra commit info

## Best Practices

✅ **Execute regularmente** - depois de mudanças significativas
✅ **Faça commit** dos documentos atualizados junto com o código
✅ **Use master script** - evita inconsistências entre versões
✅ **Revise manualmente** - verifique se as atualizações fazem sentido
✅ **Mantenha histórico** - não delete versões antigas dos .docx (Git controla isso)

## Próximas Melhorias

Ideias para automação futura:

- [ ] Integração com GitHub Actions para atualizar automaticamente
- [ ] Análise de cobertura de testes + inclusão na documentação
- [ ] Extração automática de docstrings do código
- [ ] Sincronização com CHANGELOG.md
- [ ] Geração de índice dinâmico

---

**Última Atualização:** 29/01/2026  
**Versão:** 1.0  
**Status:** Ativo e mantido
