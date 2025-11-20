import flet as ft
import asyncio

def main(page: ft.Page):
    page.title = "Pomodoro"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 500
    page.window.height = 600
    page.window.center()
    page.padding = 0
    page.update()

    time_text = ft.Text("25:00", size=50, color="white")
    status_text = ft.Text("Pomodoro", size=20, color="white")
    ciclo_text = ft.Text("Ciclo 1/4", size=18, color="white")

    total = 25 * 60
    initial_total = total
    modo = "pomodoro"
    ciclo = 1
    pomodoros_completos = 0
    running = False

    def atualizar_display_por_total():
        m, s = divmod(total, 60)
        time_text.value = f"{m:02d}:{s:02d}"

    def iniciar_timer():
        nonlocal running
        if running:
            return
        running = True
        page.run_task(timer)

        
    def pausar_timer():
        nonlocal running
        running = False
    
    def reiniciar_timer():
        nonlocal total, running, modo
        running = False
        total = initial_total
        status_text.value = "Pomodoro"
        atualizar_display_por_total()
        page.update()
    
    async def timer():
        nonlocal running, total, modo, pomodoros_completos

        while total > 0 and running:
            await asyncio.sleep(1)
            total -= 1
            atualizar_display_por_total()
            page.update()

        if total == 0:

            running = False

            if modo == "pomodoro":
                pomodoros_completos += 1
                ciclo_atual = (pomodoros_completos % 4) or 4
                ciclo_text.value = f"Ciclo {ciclo_atual}/4"

                if pomodoros_completos % 4 == 0:
                    modo = "pausa_longa"
                    status_text.value = "Pausa longa"
                    total = 15 * 60

                else:
                    modo = "pausa_curta"
                    status_text.value = "Pausa curta"
                    total = 5 * 60

            else:
                modo = "pomodoro"
                status_text.value = "Pomodoro"
                total = 25 * 60

            atualizar_display_por_total()
            page.update()

    start_button = ft.FilledTonalButton(text="Iniciar", on_click=lambda e: iniciar_timer())
    pause_button = ft.FilledTonalButton(text="Pausar", on_click=lambda e: pausar_timer())
    restart_button = ft.FilledTonalButton(text="Reiniciar", on_click=lambda e: reiniciar_timer())

    todoapp = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls = [
            time_text,
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls = [
                    start_button,
                    pause_button,
                    restart_button
                ]
            )
        ]
    )
    page.add(todoapp)  

ft.app(target=main)