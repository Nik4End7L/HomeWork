import flet as ft
from db import main_db

def main(page: ft.Page):
    page.title = 'ToDo List'
    page.theme_mode = ft.ThemeMode.LIGHT
    task_list = ft.Column()

    filter_type = "all"

    def load_task():
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_task(filter_type):
            task_list.controls.append(create_task_row(task_id, task_text, completed))
        page.update()

    def create_task_row(task_id, task_text, completed):
        task_field = ft.TextField(value=task_text, expand=True, read_only=True)

        task_checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        def enable_edit(_):
            if task_field.read_only == False:
                task_field.read_only = True
            else:
                task_field.read_only = False
            task_field.update()

        def save_task(_):
            main_db.update_task(task_id, task_field.value)
            page.update()
            task_field.read_only = True
            task_field.update()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, tooltip='Редактировать', on_click=enable_edit)
        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)

        return ft.Row([
            task_checkbox,
            task_field,
            edit_button,
            save_button
        ])

    def add_task(_):
        if task_input.value:
            task_id = main_db.add_task(task_input.value)
            task_list.controls.append(create_task_row(task_id, task_input.value, None))
            task_input.value = ''
            page.update()

    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id, completed=int(is_completed))
        load_task()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_task()


    task_input = ft.TextField(label='Введите задачу', expand=True)
    add_button = ft.ElevatedButton('ADD', on_click=add_task)

    filter_buttons = ft.Row(controls=[
        ft.ElevatedButton("Все", on_click=lambda e: set_filter('all')),
        ft.ElevatedButton("Завершенные", on_click=lambda e: set_filter('completed')),
        ft.ElevatedButton("Незавершенные", on_click=lambda e: set_filter('uncompleted'))
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    page.add(ft.Column([
        ft.Row([task_input, add_button]),
        filter_buttons,
        task_list
    ]))

    load_task()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)