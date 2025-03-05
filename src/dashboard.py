import streamlit as st
from src.playground import PlaygroundWorker
from typing import Callable, Any

st.set_page_config(page_title="Playground for Python Programming", page_icon="🐍", layout="wide")

def execute_worker(create_worker: Callable[[Callable[[float], None], Callable[[str], None]], Any]) -> None:
    progress_bar = st.progress(0)
    status_text = st.empty()

    def update_progress(progress: float) -> None:
        progress_bar.progress(int(progress))

    def update_status(message: str) -> None:
        status_text.text(message)

    try:
        worker = create_worker(update_progress, update_status)
        update_status("🚀 Started!")
        result = worker.run()
        if result:
            progress_bar.progress(100)
            update_status("🎉 Completed!")
            st.balloons()
        else:
            update_status("⚠️ Failed.")
    except Exception as error:
        update_status(f"⚠️ Error: {error}")

def main() -> None:
    st.title("Playground for Python Programming")
    st.write("")
    if st.button("Start Testing"):
        execute_worker(lambda progress_cb, status_cb: PlaygroundWorker(progress_callback=progress_cb, status_callback=status_cb))

if __name__ == "__main__":
    main()