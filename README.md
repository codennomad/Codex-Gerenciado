# Gerenciador de Missões e Relatórios

Este é um aplicativo interativo desenvolvido em Python com a biblioteca `Tkinter`. Ele permite gerenciar missões e relatórios de forma organizada e intuitiva.

## 📦 Funcionalidades

### Tela Inicial
- Navegue entre **Missões**, **Relatórios** e **Configurações**.
- Sistema de pontos acumuláveis que reflete o progresso nas missões concluídas.

### Gerenciamento de Missões
- **Adicionar missões:** Insira título, descrição e pontos associados.
- **Visualizar missões:** Liste as missões pendentes e veja detalhes.
- **Excluir missões:** Marque missões como concluídas e acumule pontos.
- **Ordenação:** Organize missões em ordem crescente ou decrescente de pontos.

### Gerenciamento de Relatórios
- **Adicionar relatórios:** Insira título e conteúdo detalhado.
- **Visualizar relatórios:** Leia relatórios na tela e veja detalhes de data e horário.
- **Excluir relatórios:** Remova relatórios que não são mais necessários.
- **Divisão de tela:** Leia relatórios lado a lado com outros documentos.

### Configurações
- Controle o sistema de pontos e o reset automático.
- Configure prazos para reinício ou ajustes manuais.

## 📸 Imagens da Interface

### Tela Inicial
Navegue para Missões, Relatórios ou Configurações:

![Tela Inicial](https://github.com/codennomad/Codex-Gerenciado/issues/1#issue-2766670572)

<div aligh = "center">
<img src = "https://github.com/codennomad/Codex-Gerenciado/issues/1#issue-2766670572" width "700px" />
</div>


### Tela de Missões
Gerencie suas tarefas e acompanhe o progresso:

![Tela de Missões](/imagens/tela_missoes.png)

### Tela de Relatórios
Adicione, visualize e organize relatórios:

![Tela de Relatórios](/imagens/tela_relatorios.png)
![Tela de detalhes dentro de Relatórios](/imagens/detalhes.png)

### Tela de Configurações
Gerencie o sistema de pontos e ajustes gerais:

![Tela de Configurações](/imagens/tela_config.png)


## 🛠️🚀 Como Executar

1. **Instale o Python 3.x:**
   Certifique-se de que o Python esteja instalado.

2. **Configure o Banco de Dados:**
   Não é necessário configurar manualmente. O banco de dados é criado automaticamente na primeira execução.

3. **Execute o Programa:**
   ```bash
   python Codex.py
   ```

4. **Explore as Funcionalidades:**
   - Navegue entre as telas usando os botões na interface principal.
   - Adicione, visualize e exclua missões e relatórios facilmente.


## 📋 Requisitos
    -Python 3.x
    -sqlite3


## 🗂️ Estrutura do Projeto

### Principais Arquivos
- `Codex.py`: Arquivo principal do programa.
- `missoes.db`: Banco de dados SQLite gerado automaticamente.

### Estrutura do Banco de Dados
1. **Tabela `missoes`:**
   - `id`: Identificador da missão.
   - `titulo`: Título da missão.
   - `descricao`: Detalhes sobre a tarefa.
   - `pontos`: Pontos associados.
   - `concluida`: Indica se foi concluída.

2. **Tabela `relatorios`:**
   - `id`: Identificador do relatório.
   - `titulo`: Título do relatório.
   - `texto`: Conteúdo do relatório.
   - `data_criacao`: Data e hora de criação.

3. **Tabela `pontos`:**
   - `id`: Controle geral.
   - `total_pontos`: Pontos acumulados.

## ⚖️ Licença

Este projeto está licenciado sob a [MIT License](LICENSE). Você pode usar, modificar e distribuir este código livremente, desde que mantenha os créditos ao autor original.

---

Divirta-se gerenciando suas missões e relatórios! 😄

