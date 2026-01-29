# Sistema de Manutenção Automática de Documentação

## 🎯 Objetivo

Manter os documentos Word em **inglês** e **português brasileiro** sempre sincronizados com o código, sem criar novas versões (in-place updates).

## 📦 O Que Foi Criado

### 1. **update_documentation_en.py**
- Atualiza `eSocial_Extractor_Documentation.docx` (versão inglês)
- Coleta estatísticas de código (arquivos, linhas)
- Obtém informações do Git (último commit)
- Usa python-docx para modificar documento existente

### 2. **update_documentation_ptbr.py**
- Atualiza `eSocial_Extractor_Documentacao_PTBR.docx` (versão português)
- Mesma funcionalidade do script inglês
- Toda saída em português brasileiro
- Data/hora no formato DD/MM/YYYY

### 3. **update_all_documentation.py**
- Script master que executa ambos os scripts
- Fornece relatório consolidado
- Retorna código de saída apropriado (0 = sucesso, 1 = falha)
- Ideal para automação e CI/CD

### 4. **MANUTENCAO_DOCUMENTACAO.md**
- Guia completo de uso e personalização
- Workflow recomendado para diferentes cenários
- Instruções para automação com Git hooks
- Troubleshooting e best practices

## 🚀 Como Usar

### Uso Simples (Recomendado)
```bash
python update_all_documentation.py
```

### Uso Específico
```bash
# Apenas inglês
python update_documentation_en.py

# Apenas português
python update_documentation_ptbr.py
```

## ✅ O Que é Atualizado

- ✅ **Número total de arquivos Python**
- ✅ **Total de linhas de código**
- ✅ **Data/hora da atualização**
- ✅ **Informações do último commit Git**

## ❌ O Que NÃO é Atualizado

Os scripts preservam intentionalmente o conteúdo substantivo:
- Descrições de arquitetura
- Explicações de componentes
- Exemplos de código
- Diagramas e imagens
- Estrutura e formatação

**Motivo:** Manter qualidade e contexto da documentação. Se o conteúdo mudar significativamente, edite manualmente ou recrie geradores mais avançados.

## 📋 Workflow Recomendado

```bash
# 1. Fazer alterações no código
# 2. Commit do código
git add .
git commit -m "Implement feature X"

# 3. Atualizar documentação
python update_all_documentation.py

# 4. Commit dos documentos atualizados
git add *.docx
git commit -m "Update docs for feature X"

# 5. Push para GitHub
git push origin main
```

## 🔄 Automação Contínua

### Git Hooks (automático antes de cada commit)

```bash
# Criar .git/hooks/pre-commit
#!/bin/bash
python update_all_documentation.py
git add eSocial_Extractor_Documentation.docx
git add eSocial_Extractor_Documentacao_PTBR.docx

# Tornar executável
chmod +x .git/hooks/pre-commit
```

### GitHub Actions (futuro)

Possível adicionar workflow que atualiza documentos automaticamente em cada push.

## 📊 Sincronização de Lingua

Ambas as versões (EN/PT-BR) são **sempre** atualizadas juntas:

| Aspecto | English | Português BR |
|---------|---------|--------------|
| Script de Update | `update_documentation_en.py` | `update_documentation_ptbr.py` |
| Arquivo de Saída | `eSocial_Extractor_Documentation.docx` | `eSocial_Extractor_Documentacao_PTBR.docx` |
| Formato de Data | ISO 8601 (YYYY-MM-DD HH:MM:SS) | DD/MM/YYYY HH:MM:SS |
| Conteúdo | 100% Inglês | 100% Português BR |
| Master Updater | `update_all_documentation.py` (atualiza ambas sequencialmente) |

## 🛠️ Personalização Futura

Para adicionar novos campos de atualização:

1. Editar `update_documentation_en.py`
2. Adicionar lógica na função `update_documentation()`
3. Usar python-docx para encontrar/modificar seções
4. Replicar em `update_documentation_ptbr.py`
5. Testar com `python update_all_documentation.py`

Exemplo:
```python
for para in doc.paragraphs:
    if "API Endpoints" in para.text:
        # Atualizar próximo parágrafo com dados atuais
        pass
```

## 🔐 Requisitos

- ✅ Python 3.7+
- ✅ Biblioteca `python-docx` (já instalada)
- ✅ Git instalado no sistema
- ✅ Documentos Word existentes (não cria novos)

## 📞 Suporte

Veja **MANUTENCAO_DOCUMENTACAO.md** para:
- FAQ completo
- Troubleshooting
- Best practices
- Ideias de melhoria futura

---

**Data de Criação:** 29/01/2026  
**Status:** ✅ Ativo e pronto para uso  
**Última Atualização:** 29/01/2026
