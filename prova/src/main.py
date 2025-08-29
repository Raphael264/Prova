import flet as ft

def main(page: ft.Page):
    # Configuração da página
    page.title = "Todo App"
    page.window_width = 400
    page.window_height = 500
    page.window_resizable = False
    page.padding = 20
    page.theme_mode = "light"
    
    # Variáveis de estado
    tasks = [
        {"completed": False, "text": "Create Flet app"},
        {"completed": False, "text": "Final touches"},
        {"completed": False, "text": "Deploy app"}
    ]
    filter_status = "all"  # all, active, completed
    
    # Elementos da UI - Título centralizado com "T" maiúsculo
    title = ft.Text("Todos", size=30, weight="bold")
    
    # Container para centralizar o título
    title_container = ft.Container(
        content=title,
        alignment=ft.alignment.center,
        width=float("inf"),  # Ocupa toda a largura disponível
        padding=ft.padding.only(bottom=10)  # Espaçamento abaixo do título
    )
    
    # Campo de texto para "What needs to be done?" com contorno
    task_input = ft.TextField(
        hint_text="What needs to be done?",
        border=ft.InputBorder.OUTLINE,
        border_radius=5,
        content_padding=15,
        text_size=16,
        expand=True
    )
    
    # Botão de adição (+) quadrado com contorno
    add_button = ft.Container(
        content=ft.Text("+", size=20, weight="bold"),
        alignment=ft.alignment.center,
        width=40,
        height=40,
        border=ft.border.all(1, "#cccccc"),
        ink=True
    )
    
    # Linha com campo de texto e botão de adição
    input_row = ft.Row(
        [
            task_input,
            add_button
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        spacing=10
    )
    
    # Lista de tarefas
    task_items = ft.Column()
    
    # Filtros
    all_filter = ft.Text("all", color="blue")
    active_filter = ft.Text("active")
    completed_filter = ft.Text("completed")
    
    # Tornar os textos clicáveis
    all_filter_click = ft.GestureDetector(
        content=all_filter,
        mouse_cursor=ft.MouseCursor.CLICK
    )
    
    active_filter_click = ft.GestureDetector(
        content=active_filter,
        mouse_cursor=ft.MouseCursor.CLICK
    )
    
    completed_filter_click = ft.GestureDetector(
        content=completed_filter,
        mouse_cursor=ft.MouseCursor.CLICK
    )
    
    # Contador
    items_left = ft.Text("3 active item(s) left")
    
    # Botão "Clear completed" com contorno
    clear_completed = ft.Container(
        content=ft.Text("Clear completed"),
        border=ft.border.all(1, "#cccccc"),
        border_radius=5,
        padding=ft.padding.all(8),
        ink=True
    )
    
    clear_completed_click = ft.GestureDetector(
        content=clear_completed,
        mouse_cursor=ft.MouseCursor.CLICK
    )
    
    # Função para adicionar nova tarefa
    def add_task(e):
        if task_input.value:
            tasks.append({"completed": False, "text": task_input.value})
            task_input.value = ""
            update_task_list()
            update_footer()
            page.update()
    
    # Configurar o evento de submeter no campo de texto
    task_input.on_submit = add_task
    
    # Função para atualizar a lista de tarefas
    def update_task_list():
        task_items.controls.clear()
        
        filtered_tasks = tasks
        if filter_status == "active":
            filtered_tasks = [task for task in tasks if not task["completed"]]
        elif filter_status == "completed":
            filtered_tasks = [task for task in tasks if task["completed"]]
        
        for i, task in enumerate(filtered_tasks):
            def create_checkbox_change_handler(index):
                def handler(e):
                    tasks[index]["completed"] = e.control.value
                    update_task_list()
                    update_footer()
                return handler
            
            checkbox = ft.Checkbox(
                label=task["text"],
                value=task["completed"],
                on_change=create_checkbox_change_handler(i)
            )
            task_items.controls.append(checkbox)
        
        page.update()
    
    # Função para atualizar o rodapé
    def update_footer():
        active_count = sum(1 for task in tasks if not task["completed"])
        items_left.value = f"{active_count} active item(s) left"
        
        # Mostrar ou esconder o rodapé baseado na existência de tarefas
        if tasks:
            footer.visible = True
        else:
            footer.visible = False
            
        page.update()
    
    # Função para atualizar a aparência dos filtros
    def update_filter_buttons():
        # Resetar todas as cores
        all_filter.color = None
        active_filter.color = None
        completed_filter.color = None
        
        # Destacar o filtro ativo
        if filter_status == "all":
            all_filter.color = "blue"
        elif filter_status == "active":
            active_filter.color = "blue"
        elif filter_status == "completed":
            completed_filter.color = "blue"
        
        page.update()
    
    # Funções para os filtros
    def set_filter_all(e):
        nonlocal filter_status
        filter_status = "all"
        update_filter_buttons()
        update_task_list()
    
    def set_filter_active(e):
        nonlocal filter_status
        filter_status = "active"
        update_filter_buttons()
        update_task_list()
    
    def set_filter_completed(e):
        nonlocal filter_status
        filter_status = "completed"
        update_filter_buttons()
        update_task_list()
    
    # Configurar eventos dos filtros
    all_filter_click.on_tap = set_filter_all
    active_filter_click.on_tap = set_filter_active
    completed_filter_click.on_tap = set_filter_completed
    
    # Função para limpar tarefas completadas
    def clear_completed_tasks(e):
        nonlocal tasks
        tasks = [task for task in tasks if not task["completed"]]
        update_task_list()
        update_footer()
    
    clear_completed_click.on_tap = clear_completed_tasks
    
    # Layout dos filtros - REMOVIDO O ALINHAMENTO CENTRAL
    filters_row = ft.Row(
        [all_filter_click, active_filter_click, completed_filter_click],
        spacing=20  # Apenas espaçamento, sem alinhamento central
    )
    
    # Layout do rodapé
    footer = ft.Row(
        [items_left, clear_completed_click],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=True if tasks else False
    )
    
    # Adicionar elementos à página na nova ordem:
    # 1. Título centralizado
    # 2. Campo de texto + botão
    # 3. Filtros (all, active, completed) - AGORA DESCENTRALIZADO
    # 4. Lista de tarefas
    # 5. Rodapé (contador + clear completed)
    page.add(
        title_container,  # Título totalmente centralizado
        input_row,  # Linha com campo de texto e botão de adição
        ft.Container(height=10),  # Espaçamento
        filters_row,  # Filtros (all, active, completed) - DESCENTRALIZADO
        ft.Divider(height=1, color="#e0e0e0"),
        task_items,  # Lista de tarefas
        ft.Divider(height=1, color="#e0e0e0"),
        footer  # Rodapé (contador + clear completed)
    )
    
    # Inicializar a lista de tarefas e botões de filtro
    update_filter_buttons()
    update_task_list()

# Executar o aplicativo
ft.app(target=main)