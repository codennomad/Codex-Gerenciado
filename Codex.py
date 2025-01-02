import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import time
from datetime import datetime, timedelta

# Configuração do banco de dados
def criar_banco():
    conn = sqlite3.connect("missoes.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS missoes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        titulo TEXT NOT NULL,
                        descricao TEXT NOT NULL,
                        pontos INTEGER NOT NULL,
                        concluida INTEGER DEFAULT 0
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS relatorios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        titulo TEXT NOT NULL,
                        texto TEXT NOT NULL,
                        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS configuracoes (
                        id INTEGER PRIMARY KEY,
                        ultima_data_reset TIMESTAMP
                    )''')
    cursor.execute("INSERT OR IGNORE INTO configuracoes (id, ultima_data_reset) VALUES (1, ?)",
                   (datetime.now() - timedelta(weeks=2),))
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS pontos (
                        id INTEGER PRIMARY KEY,
                        total_pontos INTEGER NOT NULL DEFAULT 0
                    )''')
    cursor.execute("INSERT OR IGNORE INTO pontos (id, total_pontos) VALUES (1, 0)")
    conn.commit()
    conn.close()

criar_banco()

def obter_pontos():
    conn = sqlite3.connect("missoes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT total_pontos FROM pontos WHERE id = 1")
    pontos = cursor.fetchone()[0]
    conn.close()
    return pontos

def atualizar_pontos(pontos):
    conn = sqlite3.connect("missoes.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE pontos SET total_pontos = total_pontos + ? WHERE id = 1", (pontos,))
    conn.commit()
    conn.close()
    
def resetar_pontos():
    conn = sqlite3.connect("missoes.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE pontos SET total_pontos = 0 WHERE id = 1")
    cursor.execute("UPDATE configuracoes SET ultima_data_reset = ?", (datetime.now(),))
    conn.commit()
    conn.close()
    atualizar_total_pontos()

def verificar_reset_automatico():
    conn = sqlite3.connect("missoes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT ultima_data_reset FROM configuracoes WHERE id = 1")
    ultima_data_reset = datetime.strptime(cursor.fetchone()[0].split('.')[0], '%Y-%m-%d %H:%M:%S')
    conn.close()
    
    proximo_reset = ultima_data_reset + timedelta(weeks=2)
    agora = datetime.now()
    delta = proximo_reset - agora

    if delta.total_seconds() <= 0:
        resetar_pontos()
        delta = timedelta(weeks=2)

    semanas, dias = divmod(delta.days, 7)
    horas, resto = divmod(delta.seconds, 3600)
    minutos, segundos = divmod(resto, 60)

    return semanas, dias, horas, minutos, segundos


# Função para criar uma missão
def criar_missao(frame, id_missao, titulo, descricao, pontos):
    missao_frame = tk.Frame(frame, bg="#3A3A4F", padx=10, pady=10)
    missao_frame.pack(fill="x", pady=5)

    # Grid layout
    missao_frame.grid_rowconfigure(1, weight=1)
    missao_frame.grid_columnconfigure(0, weight=1)

    # Tag "NEW" no canto superior esquerdo
    tag_label = tk.Label(missao_frame, text="NEW", font=("Arial", 7, "bold"), fg="white", bg="#F39C12", padx=5, pady=2)
    tag_label.grid(row=0, column=0, sticky="nw", padx=5)

    # Título
    titulo_label = tk.Label(missao_frame, text=titulo, font=("Arial", 14, "bold"), fg="white", bg="#3A3A4F")
    titulo_label.grid(row=0, column=0, sticky="w", padx=(40, 5))  # Move para a direita, para não sobrepor a tag

    # Pontos no canto superior direito
    recompensa_label = tk.Label(missao_frame, text=f"{pontos}💎", font=("Arial", 12, "bold"), fg="#F4D03F", bg="#3A3A4F")
    recompensa_label.grid(row=0, column=1, sticky="e", padx=5)

    # Descrição
    descricao_label = tk.Label(missao_frame, text=descricao, font=("Arial", 10), fg="#D6D6D6", bg="#3A3A4F", wraplength=400)
    descricao_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

    # Botão "Completar" no canto inferior direito
    botao_completar = tk.Button(
        missao_frame,
        text="✅ Completar",
        font=("Arial", 10, "bold"),
        bg="#5DADE2",
        fg="white",
        command=lambda: completar_missao(id_missao, pontos, missao_frame)
    )
    botao_completar.grid(row=2, column=1, sticky="e", pady=5, padx=5)

# Função para exibir as missões
def exibir_missoes(frame):
    conn = sqlite3.connect("missoes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, descricao, pontos FROM missoes WHERE concluida = 0")
    missoes = cursor.fetchall()
    conn.close()

    for widget in frame.winfo_children():
        widget.destroy()

    for missao in missoes:
        criar_missao(frame, missao[0], missao[1], missao[2], missao[3])
        

def completar_missao(id_missao, pontos, frame):
    conn = sqlite3.connect("missoes.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE missoes SET concluida = 1 WHERE id = ?", (id_missao,))
    conn.commit()
    conn.close()
    frame.destroy()
    atualizar_pontos(pontos)
    atualizar_total_pontos()

def atualizar_total_pontos():
    total_pontos_label.config(text=f"Pontos: {obter_pontos()}")
    
# Função para exibir relatórios do banco de dados
def exibir_relatorios():
    for widget in container_relatorios.winfo_children():
        widget.destroy()

    conn = sqlite3.connect("missoes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, texto, data_criacao FROM relatorios ORDER BY data_criacao DESC")
    relatorios = cursor.fetchall()
    conn.close()

    for relatorio in relatorios:
        relatorio_frame = tk.Frame(container_relatorios, bg="#3A3A4F", padx=10, pady=10)
        relatorio_frame.pack(fill="x", pady=5)

        titulo_label = tk.Label(relatorio_frame, text=relatorio[1], font=("Arial", 14, "bold"), fg="white", bg="#3A3A4F")
        titulo_label.grid(row=0, column=0, sticky="w", padx=5)
        
        
        # Data de criação
        data_label = tk.Label(relatorio_frame, text=f"Data: {relatorio[3]}", font=("Arial", 10), fg="#D6D6D6", bg="#3A3A4F")
        data_label.grid(row=0, column=1, sticky="e", padx=5)
        

        # Texto do Relatório
        texto_resumido = relatorio[2][:100] + ("..." if len(relatorio[2]) > 100 else "")
        texto_label = tk.Label(relatorio_frame, text=texto_resumido, font=("Arial", 12), fg="white", bg="#3A3A4F", wraplength=500, justify="left")
        texto_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=5, padx=5)
        
        #Botao de excluir
        botao_excluir = tk.Button(
            relatorio_frame,
            text="❌ Excluir",
            font=("Arial", 10, "bold"),
            bg="#E74C3C",
            fg="white",
            command=lambda relatorio_id=relatorio[0]: excluir_relatorio(relatorio_id, relatorio_frame)
        )
        botao_excluir.grid(row=2, column=1, sticky="e", pady=5, padx=5)
        
        #Botao detalhes
        botao_detalhes = tk.Button(
            relatorio_frame,
            text="📖 Detalhes",
            font=("Arial", 10, "bold"),
            bg="#5DADE2",
            fg="white",
            command=lambda t=relatorio[1], tx=relatorio[2]: abrir_relatorio_completo(t, tx)
        )
        botao_detalhes.grid(row=2, column=0, sticky="w", pady=5, padx=5)


def adicionar_missao():
    def salvar_missao():
        titulo = entrada_titulo.get()
        descricao = entrada_descricao.get("1.0", tk.END).strip()
        pontos = int(entrada_pontos.get())
        
        conn = sqlite3.connect("missoes.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO missoes (titulo, descricao, pontos) VALUES (?, ?, ?)", (titulo, descricao, pontos))
        conn.commit()
        conn.close()

        exibir_missoes(container)
        janela_adicionar.destroy()

    janela_adicionar = tk.Toplevel()
    janela_adicionar.title("Adicionar Missão")
    janela_adicionar.geometry("300x300")
    janela_adicionar.configure(bg="#2E2E3E")

    tk.Label(janela_adicionar, text="Título:", font=("Arial", 12), fg="white", bg="#2E2E3E").pack(pady=5)
    entrada_titulo = tk.Entry(janela_adicionar, font=("Arial", 12))
    entrada_titulo.pack(fill="x", padx=10, pady=5)

    tk.Label(janela_adicionar, text="Descrição:", font=("Arial", 12), fg="white", bg="#2E2E3E").pack(pady=5)
    entrada_descricao = tk.Text(janela_adicionar, font=("Arial", 10), height=5, wrap="word")
    entrada_descricao.pack(fill="x", padx=10, pady=5)

    tk.Label(janela_adicionar, text="Pontos:", font=("Arial", 12), fg="white", bg="#2E2E3E").pack(pady=5)
    entrada_pontos = tk.Entry(janela_adicionar, font=("Arial", 12))
    entrada_pontos.pack(fill="x", padx=10, pady=5)

    tk.Button(janela_adicionar, text="Salvar", command=salvar_missao, bg="#28B463", fg="white").pack(pady=10)
    
    
def adicionar_relatorio():
    def salvar_relatorio():
        titulo = entrada_titulo.get()
        texto = entrada_relatorio.get("1.0", tk.END).strip()

        conn = sqlite3.connect("missoes.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO relatorios (titulo, texto) VALUES (?, ?)", (titulo, texto))
        conn.commit()
        conn.close()

        exibir_relatorios()
        janela_adicionar_relatorio.destroy()

    janela_adicionar_relatorio = tk.Toplevel()
    janela_adicionar_relatorio.title("Adicionar Relatório")
    janela_adicionar_relatorio.geometry("300x350")
    janela_adicionar_relatorio.configure(bg="#2E2E3E")
    
    tk.Label(janela_adicionar_relatorio, text="Título:", font=("Arial", 12), fg="white", bg="#2E2E3E").pack(pady=5)
    entrada_titulo = tk.Entry(janela_adicionar_relatorio, font=("Arial", 12))
    entrada_titulo.pack(fill="x", padx=10, pady=5)

    tk.Label(janela_adicionar_relatorio, text="Escreva seu relatório:", font=("Arial", 12), fg="white", bg="#2E2E3E").pack(pady=10)
    entrada_relatorio = tk.Text(janela_adicionar_relatorio, font=("Arial", 10), height=10, wrap="word")
    entrada_relatorio.pack(fill="x", padx=10, pady=10)

    tk.Button(janela_adicionar_relatorio, text="Salvar", command=salvar_relatorio, bg="#28B463", fg="white").pack(pady=10)
    
def excluir_relatorio(relatorio_id, frame):
    conn = sqlite3.connect("missoes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM relatorios WHERE id = ?", (relatorio_id,))
    conn.commit()
    conn.close()

    frame.destroy()

def abrir_missoes():
    tela_inicial.pack_forget()
    tela_missoes.pack(fill="both", expand=True)
    exibir_missoes(container)

def voltar_tela_inicial():
    tela_configuracoes.pack_forget()
    tela_relatorios.pack_forget()
    tela_missoes.pack_forget()
    tela_inicial.pack(fill="both", expand=True)
    
def abrir_configuracoes():
    tela_inicial.pack_forget()
    tela_configuracoes.pack(fill="both", expand=True)
    
def resetar_pontos_manual():
    resetar_pontos()
    tk.messagebox.showinfo("Reset Manual", "Os pontos foram resetados com sucesso!")
    atualizar_temporizador()  # Inicia o temporizador ao abrir a telas
    
def atualizar_temporizador():
    semanas, dias, horas, minutos, segundos = verificar_reset_automatico()
    texto = f"Próximo reset em: {semanas} semanas, {dias} dias, {horas:02}:{minutos:02}:{segundos:02}"
    label_temporizador.config(text=texto)
    tela_configuracoes.after(1000, atualizar_temporizador)  # Atualiza a cada segundo
               
    
def abrir_relatorios():
    tela_inicial.pack_forget()
    tela_relatorios.pack(fill="both", expand=True)
    exibir_relatorios()
    
def abrir_relatorio_completo(titulo, texto):
    # Janela de detalhes
    janela_detalhes = tk.Toplevel()
    janela_detalhes.title("Detalhes do Relatório")
    janela_detalhes.geometry("600x400")
    janela_detalhes.configure(bg="#3A3A4F")

    # Frame principal
    frame_principal = tk.Frame(janela_detalhes, bg="#3A3A4F")
    frame_principal.pack(fill="both", expand=True)

    # Canvas para rolagem
    canvas = tk.Canvas(frame_principal, bg="#3A3A4F", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    # Barra de rolagem
    scrollbar = ttk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame interno no canvas
    frame_conteudo = tk.Frame(canvas, bg="#3A3A4F")
    canvas.create_window((0, 0), window=frame_conteudo, anchor="nw")

    # Ajustar a rolagem ao tamanho do conteúdo
    def ajustar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_conteudo.bind("<Configure>", ajustar_scroll)

    # Permitir rolagem com o mouse
    def rolar_mouse(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    canvas.bind_all("<MouseWheel>", rolar_mouse)

    # Adicionar título do relatório
    titulo_label = tk.Label(frame_conteudo, text=titulo, font=("Arial", 16, "bold"), fg="white", bg="#3A3A4F")
    titulo_label.pack(pady=10, padx=10, anchor="w")

    # Adicionar texto do relatório
    texto_label = tk.Label(frame_conteudo, text=texto, font=("Arial", 12), fg="white", bg="#3A3A4F", wraplength=550, justify="left")
    texto_label.pack(pady=10, padx=10, anchor="w")

    # Botão "Fechar" fixo
    botao_fechar = tk.Button(janela_detalhes, text="❌ Fechar", font=("Arial", 12, "bold"), bg="#E74C3C", fg="white", command=janela_detalhes.destroy)
    botao_fechar.pack(side="bottom", pady=10)
          
    
def ordenar_missoes(increasing = True):
    global missoes
    missoes = sorted(missoes, key=lambda x: x["pontos"], reverse=not increasing)
    exibir_missoes()

# Configuração da janela principal
janela = tk.Tk()
janela.title("Gerenciador de Missões")
janela.geometry("600x600")
janela.configure(bg="#2E2E3E")

# Tela Inicial
tela_inicial = tk.Frame(janela, bg="#2E2E3E")
tela_inicial.pack(fill="both", expand=True)

# Pontos Totais
total_pontos_label = tk.Label(tela_inicial, text=f"💎: {obter_pontos()}", font=("Arial", 16, "bold"), fg="white", bg="#2E2E3E")
total_pontos_label.pack(anchor="ne" ,padx=10, pady=10)

#Frame central para Botões
frame = tk.Frame(tela_inicial, bg="#2E2E3E")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Botões da Tela Inicial
btn_missoes = tk.Button(frame, text="ChaoSsS", bg="#5DADE2", fg="white", font=("Arial", 12))
btn_missoes.grid(row=0, column=1, padx=10, pady=10)

btn_missoes = tk.Button(frame, text="Missões", command=abrir_missoes, bg="#5DADE2", fg="white", font=("Arial", 12))
btn_missoes.grid(row=1, column=0, padx=10, pady=10)

btn_config = tk.Button(frame, text="Config ⚙", bg="#5DADE2", fg="white", font=("Arial", 12))
btn_config.grid(row=1, column=2, padx=10, pady=10)

btn_relatorios = tk.Button(frame, text="Relatórios",command=abrir_relatorios, bg="#5DADE2", fg="white", font=("Arial", 12))
btn_relatorios.grid(row=2, column=1, padx=10, pady=10)

# Tela de Missões
tela_missoes = tk.Frame(janela, bg="#2E2E3E")

frame_botoes = tk.Frame(tela_missoes, bg="#2E2E3E")
frame_botoes.pack(fill="x", pady=5)

botao_voltar = tk.Button(frame_botoes, text="Voltar", command=voltar_tela_inicial, bg="#F39C12", fg="white")
botao_voltar.pack(side="left", padx=5)

btn_increasing = tk.Button(frame_botoes, text="↑", command=lambda: ordenar_missoes(increasing = True), bg="#5DADE2", fg="white")
btn_increasing.pack(side="left", padx=5)

btn_decreasing = tk.Button(frame_botoes, text="↓", command=lambda: ordenar_missoes(increasing = False), bg="#5DADE2", fg="white")
btn_decreasing.pack(side="left", padx=5)

botao_adicionar = tk.Button(frame_botoes, text="Adicionar Missão", command=adicionar_missao, bg="#28B463", fg="white")
botao_adicionar.pack(side="left", padx=5)

frame_rolagem = tk.Frame(tela_missoes, bg="#2E2E3E")
frame_rolagem.pack(fill="both", expand=True, padx=10, pady=5)

canvas = tk.Canvas(frame_rolagem, bg="#2E2E3E", highlightthickness=0)
scrollbar = ttk.Scrollbar(frame_rolagem, orient="vertical", command=canvas.yview)
container = tk.Frame(canvas, bg="#2E2E3E")

container.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=container, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

#tela de relatorios
tela_relatorios = tk.Frame(janela, bg="#2E2E3E")

frame_botoes_relatorios = tk.Frame(tela_relatorios, bg="#2E2E3E")
frame_botoes_relatorios.pack(fill="x", pady=5)

botao_voltar_relatorios = tk.Button(frame_botoes_relatorios, text="Voltar", command=voltar_tela_inicial, bg="#F39C12", fg="white")
botao_voltar_relatorios.pack(side="left", padx=5)

botao_adicionar_relatorio = tk.Button(frame_botoes_relatorios, text="Adicionar Relatório", command=adicionar_relatorio, bg="#28B463", fg="white")
botao_adicionar_relatorio.pack(side="left", padx=5)

frame_rolagem_relatorios = tk.Frame(tela_relatorios, bg="#2E2E3E")
frame_rolagem_relatorios.pack(fill="both", expand=True, padx=10, pady=5)

canvas_relatorios = tk.Canvas(frame_rolagem_relatorios, bg="#2E2E3E", highlightthickness=0)
scrollbar_relatorios = ttk.Scrollbar(frame_rolagem_relatorios, orient="vertical", command=canvas_relatorios.yview)
container_relatorios = tk.Frame(canvas_relatorios, bg="#2E2E3E")

container_relatorios.bind(
    "<Configure>",
    lambda e: canvas_relatorios.configure(scrollregion=canvas_relatorios.bbox("all"))
)

canvas_relatorios.create_window((0, 0), window=container_relatorios, anchor="nw")
canvas_relatorios.configure(yscrollcommand=scrollbar_relatorios.set)

canvas_relatorios.pack(side="left", fill="both", expand=True)
scrollbar_relatorios.pack(side="right", fill="y")

# Tela de Configurações
tela_configuracoes = tk.Frame(janela, bg="#2E2E3E")

label_temporizador = tk.Label(tela_configuracoes, text="", font=("Arial", 12), fg="white", bg="#2E2E3E")
label_temporizador.pack(anchor="nw", pady=5, padx=5)

botao_voltar_config = tk.Button(tela_configuracoes, text="Voltar", command=voltar_tela_inicial, bg="#F39C12", fg="white")
botao_voltar_config.pack(side="top", pady=10)

botao_reset_manual = tk.Button(tela_configuracoes, text="Resetar Pontos Manualmente", command=resetar_pontos_manual, bg="#E74C3C", fg="white")
botao_reset_manual.pack(pady=20)

# Adicione isso ao botão "Configurações" na tela inicial
btn_config.config(command=abrir_configuracoes)

# Verifique o reset automático ao iniciar o aplicativo
verificar_reset_automatico()

janela.mainloop()
