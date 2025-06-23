# import validators
# import streamlit as st
# from langchain.prompts import PromptTemplate
# from langchain_groq import ChatGroq
# from langchain.chains.summarize import load_summarize_chain
# from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader


# # 🛠️ Streamlit App Setup
# st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
# st.title("🦜 LangChain: Summarize Text From YT or Website")
# st.subheader('Summarize URL')

# # 🎯 Sidebar for API Key Input
# with st.sidebar:
#     groq_api_key = st.text_input("Groq API Key", value="", type="password")

# # 🔗 Input field for URL
# generic_url = st.text_input("Enter YouTube or Website URL", label_visibility="collapsed")

# # 🚀 Initialize the LLM (Gemma model via Groq API)
# if groq_api_key.strip():
#     try:
#         llm = ChatGroq(model="Gemma-7b-It", groq_api_key=groq_api_key)
#     except Exception as e:
#         st.error(f"Failed to initialize ChatGroq: {e}")
# else:
#     st.warning("Please enter your Groq API Key in the sidebar.")

# # 📝 Define Prompt Template
# prompt_template = """
# Provide a summary of the following content in 300 words:
# Content: {text}
# """
# prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# # 🎉 Button to Trigger the Summarization
# if st.button("Summarize the Content from YT or Website"):

#     # ✅ Validate API key and URL
#     if not groq_api_key.strip() or not generic_url.strip():
#         st.error("Please provide both the Groq API key and a URL to get started.")
#     elif not validators.url(generic_url):
#         st.error("Please enter a valid URL. It can be a YouTube video URL or a website URL.")
#     else:
#         try:
#             with st.spinner("Loading content..."):

#                 # 🔍 Detect YouTube URLs and handle both types
#                 if "youtube.com" in generic_url or "youtu.be" in generic_url:
#                     try:
#                         loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
#                     except Exception as yt_error:
#                         st.error(f"Failed to load YouTube video: {yt_error}")
#                         st.stop()
#                 else:
#                     try:
#                         loader = UnstructuredURLLoader(
#                             urls=[generic_url],
#                             headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
#                         )
#                     except Exception as web_error:
#                         st.error(f"Failed to load website content: {web_error}")
#                         st.stop()

#                 # 📄 Load content into documents
#                 docs = loader.load()

#                 # 🔥 Run the summarization chain
#                 chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
#                 output_summary = chain.run(docs)

#                 # ✅ Show the summary output
#                 st.success("✅ Summary generated successfully!")
#                 st.write(output_summary)

#         # 🔥 Improved error handling for exceptions
#         except Exception as e:
#             st.error(f"❌ An error occurred: {e}")

import streamlit as st
import validators
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.docstore.document import Document
import yt_dlp

# 🎯 Streamlit App Setup
st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader("Summarize any URL - YouTube or Website")

# 🚀 Sidebar: API Key Input
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")

# 🔗 URL Input Field
generic_url = st.text_input("Enter YouTube or Website URL", label_visibility="collapsed")


# ✅ Function to Extract YouTube Transcripts
def get_youtube_transcript(url):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": ["en"],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            subtitles = info_dict.get("subtitles", {})
            if "en" in subtitles:
                return ydl.extract_info(url, download=False)["description"]
            else:
                return "No subtitles available."
    except Exception as e:
        return f"Error fetching YouTube content: {e}"


# 🔥 Initialize the LLM Model via Groq API
if groq_api_key.strip():
    try:
        llm = ChatGroq(model="mixtral-8x7b-32768", groq_api_key=groq_api_key)
    except Exception as e:
        st.error(f"Failed to initialize ChatGroq: {e}")
else:
    st.warning("Please enter your Groq API Key in the sidebar.")


# ✨ Define the Prompt Template
prompt_template = """
Provide a concise summary of the following content in 300 words:
Content: {text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# 🎉 Button to Trigger Summarization
if st.button("Summarize the Content from YT or Website"):

    # ✅ Input Validation
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide both the Groq API key and a URL to get started.")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL (YouTube or website).")
    else:
        try:
            with st.spinner("Loading content..."):

                # 🔍 Detect YouTube URLs and extract content
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    transcript_text = get_youtube_transcript(generic_url)
                    if "Error" in transcript_text or "No subtitles" in transcript_text:
                        st.error(transcript_text)
                        st.stop()
                    else:
                        st.info("✅ YouTube content loaded successfully!")
                        docs = [Document(page_content=transcript_text)]

                else:
                    # 🌐 Load website content
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"},
                    )
                    docs = loader.load()

                # 🔥 Run the summarization chain
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)

                # ✅ Show the Summary Output
                st.success("✅ Summary generated successfully!")
                st.write(output_summary)

        # 🔥 Handle exceptions gracefully
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
