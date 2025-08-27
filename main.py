import flet as ft
from db import main_db

def main(page: ft.Page):
    page.title = 'ToDo List'
    page.theme_mode = ft.ThemeMode.LIGHT
    task_list = ft.Column()

    filter_type = "all"

    def load_task():
        task_list.controls.clear()
        for task_id, task_text, completed, date_t in main_db.get_task(filter_type):
            task_list.controls.append(create_task_row(task_id, task_text, completed, date_t))
        page.update()

    def create_task_row(task_id, task_text, completed, date_t):
        from datetime import datetime

        try:
            dt = datetime.fromisoformat(date_t)
            time_str = dt.strftime("%H:%M:%S")
        except Exception:
            time_str = date_t 

        task_field = ft.TextField(
            value=task_text,
            expand=True,
            read_only=True
        )
        time_label = ft.Text(value=time_str, )

        task_checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        def enable_edit(_):
            task_field.read_only = not task_field.read_only
            task_field.update()

        def save_task(_):
            main_db.update_task(task_id, new_task=task_field.value)
            task_field.read_only = True
            task_field.update()
            load_task()

        def delete_task(_):
            main_db.delete_task(task_id)
            load_task()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, tooltip='Редактировать', on_click=enable_edit)
        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)
        delete_button = ft.IconButton(icon=ft.Icons.DELETE, tooltip='Удалить', on_click=delete_task)

        return ft.Row([
            task_checkbox,
            task_field,
            time_label,  
            edit_button,
            save_button,
            delete_button
        ])

    warning_text = ft.Text(value="",)

    def add_task(_):
        if len(task_input.value) > 100:
            warning_text.value = "Максимальная длина предложения 100 символов"
            page.update()
            return
        if task_input.value:
            main_db.add_task(task_input.value)
            load_task()
            task_input.value = ''
            warning_text.value = ""
            page.update()

    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id, completed=int(is_completed))
        load_task()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_task()

    task_input = ft.TextField(label='Введите задачу', expand=True, max_length=100)
    add_button = ft.ElevatedButton('ADD', on_click=add_task)

    filter_buttons = ft.Row(controls=[
        ft.ElevatedButton("Все", on_click=lambda e: set_filter('all')),
        ft.ElevatedButton("Завершенные", on_click=lambda e: set_filter('completed')),
        ft.ElevatedButton("Незавершенные", on_click=lambda e: set_filter('uncompleted'))
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    page.add(ft.Column([
        ft.Row([task_input, add_button]),
        warning_text,
        filter_buttons,
        task_list
    ]))

    load_task()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)
