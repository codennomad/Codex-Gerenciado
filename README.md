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

![tela_inicial](https://github.com/user-attachments/assets/0f86b99a-9887-47b7-bb0b-103e22b2ce33)


### Tela de Missões
Gerencie suas tarefas e acompanhe o progresso:

![tela_missoes](https://github.com/user-attachments/assets/37003290-f665-4653-af14-3563dff62e43)


### Tela de Relatórios
Adicione, visualize e organize relatórios:

![tela_relatorios](https://github.com/user-attachments/assets/2ed3a901-95ae-4f55-bdec-a6f88210fb47)
![detalhes_relatorios](https://github.com/user-attachments/assets/9a6b0372-c2a5-4eab-91f5-6f14583e3e26)

### Tela de Configurações
Gerencie o sistema de pontos e ajustes gerais:

![tela_config](https://github.com/user-attachments/assets/2c638ea6-fa1f-4249-b571-58c2df86eaf3)


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

