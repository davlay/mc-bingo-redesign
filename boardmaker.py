import streamlit as st
import csv

st.markdown(
    """
    <style>
    [class*="st-key-cell_"] button {
        width: 100%;
        height: auto;
        aspect-ratio: 1 / 1;
        white-space: normal;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Board Maker")

if "items" not in st.session_state:
    st.session_state["items"] = [None] * 25

if "selected_cell" not in st.session_state:
    st.session_state["selected_cell"] = None

with st.container(border=False, width="stretch", horizontal_alignment="center"):
    menu_columns = st.columns([1, 1], gap="small")
    with menu_columns[0]:
        with st.container(border=True, width="content"):
            for row in range(5):
                columns = st.columns(5, gap="small")

                for column in range(5):
                    index = row * 5 + column
                    item = st.session_state["items"][index]
                    is_hard = isinstance(item, dict) and item.get("is_hard", False)
                    label = f":orange[{index + 1}]" if is_hard else f"{index + 1}"

                    if columns[column].button(label, key=f"cell_{index}", type="primary" if st.session_state["selected_cell"] == index else "secondary"):
                        st.session_state["selected_cell"] = index
                        st.rerun()
    with menu_columns[1]:
        # Export to CSV
        with st.container(border=True, width="stretch"):
            st.subheader("Export to CSV")
            if st.button("Export", icon=":material/file_export:"):
                with open("board_data.csv", "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["item_name", "item_id", "is_hard", "article"])
                    for item in st.session_state["items"]:
                        if isinstance(item, dict):
                            writer.writerow([item.get("item_name", ""), item.get("item_id", ""), item.get("is_hard", False), item.get("article", "")])
                        else:
                            writer.writerow([item, "", "", ""])
                st.success("Data exported to board_data.csv")
        

selected = st.session_state["selected_cell"]

if selected is not None:
    with st.container(border=True, width="stretch"):
        row = selected // 5 + 1
        column = selected % 5 + 1
        st.subheader(f"Editing Row {row} Column {column} (Cell {selected + 1})")

        is_hard = st.checkbox(
                    "Mark as :orange[Hard]",
                    value=st.session_state["items"][selected].get("is_hard", False) if isinstance(st.session_state["items"][selected], dict) else False,
                    key=f"is_hard_{selected}"
                )
        
        item_name = st.text_input(
            "Item Name :red[*]",
            value=st.session_state["items"][selected].get("item_name", "") if isinstance(st.session_state["items"][selected], dict) else st.session_state["items"][selected] or "",
            key=f"item_name_input_{selected}",
        )

        item_id_key = f"item_id_input_{selected}"
        if item_id_key not in st.session_state:
            current_item = st.session_state["items"][selected]
            existing_item_id = (
                current_item.get("item_id", "")
                if isinstance(current_item, dict)
                else current_item or ""
            )
            st.session_state[item_id_key] = existing_item_id

        if not st.session_state[item_id_key]:
            st.session_state[item_id_key] = "_".join(
                "".join(
                    character if character.isalpha() else " "
                    for character in item_name.lower()
                ).split()
            )

        item_id = st.text_input(
            "Item ID :red[*]",
            key=item_id_key,
        )

        # Flag whitespace and characters other than letters or underscores.
        if item_id:
            if any(
                not (character.isalpha() or character == "_")
                for character in item_id
            ):
                st.write(":red[Item ID should contain only letters and underscores.]")
        
        article = st.selectbox(
            "Article :red[*]",
            options=["[No Article]", "a", "an", "the"],
            index=0 if not isinstance(st.session_state["items"][selected], dict) or "article" not in st.session_state["items"][selected] else ["", "a ", "an ", "the "].index(st.session_state["items"][selected]["article"]),
            key=f"article_{selected}"
        )
        article = "" if article == "[No Article]" else article + " "

        st.write("Display Preview")
        with st.container(border=True, width="stretch"):
            if item_name:
                if is_hard:
                    st.write(f":blue[blueplayer] acquired {article}:orange[{item_name}]!")
                else:
                    st.write(f":blue[blueplayer] acquired {article}{item_name}!")
            else:
                st.write(":gray[No item name provided.]")
        
        save = st.button("Save", type="primary", icon=":material/upload:")

        if save:
            if not item_name or not item_id:
                st.error("Please fill in all the required fields.")
            else:
                st.session_state["items"][selected] = {"item_name": item_name, "item_id": item_id, "is_hard": is_hard, "article": article}
                st.session_state["selected_cell"] = None
                st.rerun()