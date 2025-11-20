from pip._vendor.requests.packages import target
import flet as ft

def main(page: ft.Page):
    page.title = "Pomodoro"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 500
    page.window.height = 600
    page.window.center()
    page.padding = 0
    page.update()

    time_text = ft.Text("25:00", size=50, color="white")
    running = False

    def iniciar_timer():
        nonlocal running
        running = True
        
    def pausar_timer():
        nonlocal running
        running = False
    
    def reiniciar_timer():
        nonlocal running
        running = False

    start_button = ft.FilledTonalButton(text="Iniciar", on_click=lambda e: iniciar_timer())
    pause_button = ft.FilledTonalButton(text="Pausar", on_click=lambda e: pausar_timer())
    restart_button = ft.FilledTonalButton(text="Reiniciar", on_click=lambda e: reiniciar_timer())

    todoapp = ft.Column(
        controls = [
            time_text,
            ft.Row(
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