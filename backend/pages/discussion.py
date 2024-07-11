import base64
import io
from typing import Literal

import nbformat
import streamlit as st
from db import (
    add_discussion,
    get_discussions,
    get_favoritecount,
    is_favorite,
    put_favorite,
)
from PIL import Image
from streamlit_option_menu import option_menu
from utils import load_env

from setup import setup

# base64 encode された画像を読む
def read_nbimage(image: str) -> Image:
    return Image.open(io.BytesIO(base64.b64decode(image)))


def render_html_out(html: str):
    st.write(
        f"""
        <div style="overflow-x: auto;">
        {html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_notebook(notebook: bytes):
    notebook = nbformat.reads(notebook, as_version=4)
    for cell in notebook.cells:
        if cell.cell_type == "code":
            st.code(cell.source)
            for output in cell.outputs:
                if output.output_type == "display_data":
                    st.image(read_nbimage(output.data["image/png"]))
                elif output.output_type == "execute_result":
                    if "text/html" in output.data:
                        render_html_out(output.data["text/html"])
                    else:
                        st.write(output.data["text/plain"])
                elif output.output_type == "stream":
                    st.write(output.text)
                elif output.output_type == "error":
                    st.error(output.ename)
                    st.error(output.evalue)
                elif output.output_type == "dataframe":
                    st.dataframe(output.data["text/plain"])
        elif cell.cell_type == "markdown":
            st.markdown(cell.source)


def _add_favorite(username, discussion):
    if is_favorite(username, discussion.id):
        put_favorite(username, discussion.id)
        return

    put_favorite(username, discussion.id)
    st.toast(f"❤️ {discussion.title} をいいねしました!", icon="👍")


def sort_by(discussions, sort_method: Literal["新しい順", "いいねが多い順"]):
    if sort_method == "新しい順":
        return sorted(discussions, key=lambda x: x.post_date, reverse=True)
    elif sort_method == "いいねが多い順":
        return sorted(discussions, key=lambda x: get_favoritecount(x.id), reverse=True)


def select_read(env):
    discussions = get_discussions()
    # ソート順を選ぶ
    sort_method = st.radio(
        "表示順",
        ["新しい順", "いいねが多い順"],
        index=0,
    )

    discussions = sort_by(discussions, sort_method)

    for discussion in discussions:
        # 各投稿のタイトルのプレビューだけ出してクリックしたら表示
        st.write(
            f"""
            ## {discussion.title}
            by {discussion.username}
            """
        )

        # いいねボタン
        fav_count = get_favoritecount(discussion.id)

        button_text = (
            "❤️ " if is_favorite(env["username"], discussion.id) else "♡ "
        ) + str(fav_count)

        st.button(
            button_text,
            on_click=_add_favorite,
            args=(env["username"], discussion),
            key=f"fav_{discussion.id}",
        )

        with st.expander("中身を見る"):
            try:
                render_notebook(discussion.content)
            except Exception as e:
                st.error(f"ノートブックの表示に失敗しました: {e}")
            

        st.markdown("---")


def select_write(env):
    title = st.text_input("Title")
    notebook = st.file_uploader("Choose a notebook file", type="ipynb")

    def submit_notebook():
        try:
            add_discussion(title, notebook.read(), env["username"])
        except Exception as e:
            st.toast(
                f"ディスカッションの投稿に失敗しました: {e}",
                icon="😢",
            )
        else:
            st.toast(f"ディスカッション {title} を投稿しました!", icon="🥳")
        


    st.button(
        "ディスカッションを投稿する",
        on_click=submit_notebook,
    )


def main(env):
    # st.set_page_config(
    #     page_title="DacQ - Discussion",
    #     page_icon="🔈",
    #     layout="wide",
    # )
    st.header(
        """
        Discussion 🔈

        """,
        anchor="top",
        divider="orange",
    )

    st.caption(f"Login as {env['username']}")

    st.sidebar.image(
        "static/icon.svg",
        width=180,
    )

    st.sidebar.markdown(
        f"""

        ## Welcome to Discussion Page 💭
        
        「Discussion」では、 コンペに関する情報交換ができます。

        """
    )

    if st.session_state["attendee"]:
        options = ["よむ", "かく"]
    else:
        options = ["よむ"]

    selected = option_menu(
        "ディスカッションを",
        options,
        icons=["book", "pencil"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected == "よむ":
        select_read(env)

    elif selected == "かく":
        select_write(env)



if __name__ == "__main__":
    if "has_run_setup" not in st.session_state:
        setup()

    main(st.session_state["env"])
