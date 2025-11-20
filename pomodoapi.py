import flet as ft
import asyncio
from flet_audio import Audio

def main(page: ft.Page):
    page.title = "Pomodoro"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 500
    page.window.height = 600
    page.window.center()
    page.padding = 0
    page.update()

    audio = Audio(src="assets/ring.mp3", autoplay=False)
    page.overlay.append(audio)

    time_text = ft.Text("25:00", size=50, color="white")
    time_text_container = ft.Container(content=time_text, padding=ft.padding.only(left=10))
    time_edit = ft.TextField(value="25:00", visible=False, color="white")

    status_text = ft.Text("Pomodoro", size=20, color="white")
    ciclo_text = ft.Text("Ciclo 1/4", size=18, color="white")

    total = 25 * 60
    initial_total = total
    modo = "pomodoro"
    ciclo = 1
    pomodoros_completos = 0
    running = False

    time_edit_button = ft.IconButton(
        icon=ft.Icons.EDIT,
        icon_color="white",
        on_click=lambda e: habilitar_edicao_tempo()
    )

    time_save_button = ft.IconButton(
        icon=ft.Icons.SAVE,
        icon_color="white",
        visible=False,
        on_click=lambda e: salvar_edicao_tempo()
    )

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
        app_container.bgcolor = "#EF4444"
        page.update()

    def habilitar_edicao_tempo():
        time_text.visible = False
        time_edit.visible = True
        time_edit_button.visible = False
        time_save_button.visible = True
        page.update()

    def salvar_edicao_tempo():
        nonlocal total, initial_total

        novo = time_edit.value.strip()
        m, s = map(int, novo.split(":"))
        total = m * 60 + s
        initial_total = total

        time_text.value = novo
        time_text.visible = True
        time_edit.visible = False
        time_edit_button.visible = True
        time_save_button.visible = False
        page.update()
    
    async def timer():
        nonlocal running, total, modo, pomodoros_completos

        while total > 0 and running:
            await asyncio.sleep(1)
            total -= 1
            atualizar_display_por_total()
            page.update()

        if total == 0:

            audio.play()

            running = False

            if modo == "pomodoro":
                pomodoros_completos += 1
                ciclo_atual = (pomodoros_completos % 4) or 4
                ciclo_text.value = f"Ciclo {ciclo_atual}/4"
                page.update()

                if pomodoros_completos % 4 == 0:
                    modo = "pausa_longa"
                    status_text.value = "Pausa longa"
                    total = 15 * 60
                    app_container.bgcolor = "#3B82F6"
                    page.update()

                else:
                    modo = "pausa_curta"
                    status_text.value = "Pausa curta"
                    total = 5 * 60
                    app_container.bgcolor = "#22C55E"
                    page.update()

            else:
                modo = "pomodoro"
                status_text.value = "Pomodoro"
                total = 25 * 60
                app_container.bgcolor = "#EF4444"
                page.update()

            atualizar_display_por_total()
            page.update()

    start_button = ft.FilledTonalButton(text="Iniciar", on_click=lambda e: iniciar_timer())
    pause_button = ft.FilledTonalButton(text="Pausar", on_click=lambda e: pausar_timer())
    restart_button = ft.FilledTonalButton(text="Reiniciar", on_click=lambda e: reiniciar_timer())

    todoapp = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[time_text_container, time_edit, time_edit_button, time_save_button]
            ),
            status_text,
            ciclo_text,
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[start_button, pause_button, restart_button]
            )
        ]
    )

    app_container = ft.Container(
        content=todoapp,
        bgcolor="#EF4444",
        expand=True,
        padding=20,
        animate=ft.Animation(400, "ease")
    )

    page.add(app_container)  

ft.app(target=main)