import streamlit as st
from utils import load_env
from streamlit_option_menu import option_menu

from PIL import Image
import base64
import io

from db import (
    get_discussions,
    add_discussion,
    add_favorite,
    get_favoritecount,
    is_favorite,
)

import nbformat


# base64 encode された画像を読む
def read_nbimage(image: str) -> Image:
    return Image.open(io.BytesIO(base64.b64decode(image)))


def render_notebook(notebook: bytes):
    notebook = nbformat.reads(notebook, as_version=4)
    # 各セル入出力の type に応じて表示を変える
    for cell in notebook.cells:
        if cell.cell_type == "code":
            st.code(cell.source)
            for output in cell.outputs:
                if output.output_type == "display_data":
                    st.image(read_nbimage(output.data["image/png"]))
                elif output.output_type == "execute_result":
                    st.write(output.data["text/plain"])
                elif output.output_type == "stream":
                    st.write(output.text)
                elif output.output_type == "error":
                    st.error(output.ename)
                    st.error(output.evalue)
        elif cell.cell_type == "markdown":
            st.markdown(cell.source)


def select_read(env):
    discussions = get_discussions()
    discussions = sorted(discussions, key=lambda x: x.post_date, reverse=True)

    for discussion in discussions:
        # 各投稿のタイトルのプレビューだけ出してクリックしたら表示
        st.write(
            f"""
            ## {discussion.title}
            by {discussion.username}
            """
        )

        def _add_favorite():
            add_favorite(env["username"], discussion.id)
            st.toast("いいねしました!", icon="👍")

        # いいねボタン
        fav_count = get_favoritecount(discussion.id)

        button_text = (
            "❤️ " if is_favorite(env["username"], discussion.id) else "♡ "
        ) + str(fav_count)

        st.button(
            button_text,
            on_click=_add_favorite,
        )

        with st.expander("中身を見る"):
            render_notebook(discussion.content)


def select_write(env):
    title = st.text_input("Title")
    notebook = st.file_uploader("Choose a notebook file", type="ipynb")

    def submit_notebook():
        add_discussion(title, notebook.read(), env["username"])
        st.toast(f"ディスカッション {title} を投稿しました!", icon="🥳")

    st.button(
        "ディスカッションを投稿する",
        on_click=submit_notebook,
    )


def main():
    env = load_env()

    st.header(
        """
        Discussion 🔈

        """,
        anchor="top",
        divider="orange",
    )

    st.caption(f"Login as {env['username']}")
    st.caption(f"Team: {env['teamname']}")

    st.sidebar.image(
        "static/icon_svg.svg",
        width=180,
    )

    st.sidebar.markdown(
        f"""

        ## Welcome to Discussion Page 💭
        
        「Discussion」では、 コンペに関する情報交換ができます。

        """
    )

    selected = option_menu(
        "ディスカッションを",
        ["よむ", "かく"],
        icons=["📖", "📝"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected == "よむ":
        select_read(env)

    elif selected == "かく":
        select_write(env)


if __name__ == "__main__":
    main()
