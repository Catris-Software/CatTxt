import flet as ft
from flet import BorderSide, OutlineInputBorder


def main(page: ft.Page):

    def update_preview(e):
        md.value = selected_file_content.value
        page.update()

    selected_file_name = ft.Text("No file selected")
    selected_file_content = ft.TextField(
        label="Selected file content",
        multiline=True,
        autocorrect=True,
        expand=True,
        border=OutlineInputBorder(side=BorderSide(color=ft.Colors.TRANSPARENT)),
        on_change=update_preview
    )
    md = ft.Markdown(
        value=selected_file_content.value,
        selectable=True,
        extension_set="gitHubWeb",  
        on_tap_link=lambda e: page.launch_url(e.data),
    )

    save_status = ft.Text()

    async def pick_text_file(_: ft.Event[ft.FloatingActionButton]):
        files = await ft.FilePicker().pick_files(
            allow_multiple=False,
            with_data=True,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt", "md"],
        )
        if not files:
            selected_file_name.value = "Selection cancelled"
            selected_file_content.value = ""
            return

        selected = files[0]
        selected_file_name.value = f"Selected: {selected.name} ({selected.size} bytes)"
        selected_file_content.value = (
            selected.bytes.decode("utf-8", errors="replace") if selected.bytes else ""
        )
        save_status.value = ""

    async def save_text_file(_: ft.Event[ft.Button]):
        file_name = "untitled.md"
        file_path = await ft.FilePicker().save_file(
            file_name=file_name,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt"],
            src_bytes=selected_file_content.value.encode("utf-8"),
        )
        if page.web:
            save_status.value = f"Downloaded as {file_name}"
        else:
            save_status.value = (
                f"Saved to: {file_path}" if file_path else "Save cancelled"
            )

    page.appbar = ft.AppBar(
        title=selected_file_name,
        bgcolor=ft.Colors.CYAN,
        actions=[
            ft.Button(
                content="Save",
                icon=ft.Icons.SAVE_ALT_ROUNDED,
                on_click=save_text_file,
            ),
            save_status,
        ],
    )

    page.add(
        ft.Row(
            controls=[
                selected_file_content,
                save_status,
                ft.Container(
                    ft.Column(
                        [md],
                        scroll="hidden",
                    ),
                    expand=True,
                    alignment=ft.Alignment.TOP_LEFT,
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
    )


    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.FILE_OPEN_ROUNDED,
        on_click=pick_text_file,
    )


if __name__ == "__main__":
    ft.run(main)