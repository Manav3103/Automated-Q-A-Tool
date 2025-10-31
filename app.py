import streamlit as st
import io
import tempfile
import os
from document_processor import DocumentProcessor
from question_generator import QuestionGenerator

def main():
    st.set_page_config(
        page_title="AI Question Generator",
        page_icon="📝",
        layout="wide"
    )
    
    st.title("📝 AI Question Generator")
    st.markdown("Upload PDF, DOCX, or TXT documents to generate questions")
    
    # Initialize processors
    doc_processor = DocumentProcessor()
    question_gen = QuestionGenerator()
    
    # Sidebar for question type selection
    st.sidebar.header("Question Types")
    st.sidebar.markdown("Select which types of questions to generate:")
    
    generate_short = st.sidebar.checkbox("Short Answer Questions", value=True)
    generate_long = st.sidebar.checkbox("Long Answer Questions", value=True)
    generate_mcq = st.sidebar.checkbox("Multiple Choice Questions", value=True)
    
    if not any([generate_short, generate_long, generate_mcq]):
        st.sidebar.error("Please select at least one question type")
        return
    
    # Number of questions per type
    st.sidebar.header("Question Count")
    num_questions = st.sidebar.slider("Questions per type", min_value=1, max_value=20, value=3)
    
    # File upload
    st.header("📁 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF, DOCX, or TXT file",
        type=['pdf', 'docx', 'txt'],
        help="Upload a document to extract text and generate questions"
    )
    
    if uploaded_file is not None:
        # Display file info
        st.success(f"File uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
        
        # Process document
        with st.spinner("Extracting text from document..."):
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Extract text
                text_content = doc_processor.extract_text(tmp_file_path)
                
                # Clean up temporary file
                os.unlink(tmp_file_path)
                
                if not text_content.strip():
                    st.error("No text could be extracted from the document. Please check if the file contains readable text.")
                    return
                    
            except Exception as e:
                st.error(f"Error processing document: {str(e)}")
                return
        
        # app.py

# ...
        # Display extracted text preview
        # NOTE: Using 4000 chars for preview, matching the AI input limit.
        PREVIEW_LIMIT = 4000
        
        with st.expander(f" Extracted Text Preview (first {PREVIEW_LIMIT} characters)"):
            st.text(text_content[:PREVIEW_LIMIT] + "..." if len(text_content) > PREVIEW_LIMIT else text_content)
# ...
        
        # Generate questions
        if st.button("🚀 Generate Questions", type="primary"):
            if not os.getenv("GEMINI_API_KEY"):
                st.error("Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")
                return
            
            all_questions = []
            
            # Generate different types of questions
            question_types = []
            if generate_short:
                question_types.append(("Short Answer", "short"))
            if generate_long:
                question_types.append(("Long Answer", "long"))
            if generate_mcq:
                question_types.append(("Multiple Choice", "mcq"))
            
            progress_bar = st.progress(0)
            progress_text = st.empty()
            
            for i, (type_name, type_code) in enumerate(question_types):
                progress_text.text(f"Generating {type_name} questions...")
                progress_bar.progress((i) / len(question_types))
                
                try:
                    questions = question_gen.generate_questions(
                        text_content, 
                        question_type=type_code, 
                        num_questions=num_questions
                    )
                    
                    if questions:
                        all_questions.extend(questions)
                        st.success(f"Generated {len(questions)} {type_name} question(s)")
                    else:
                        st.warning(f"No {type_name} questions were generated")
                        
                except Exception as e:
                    st.error(f"Error generating {type_name} questions: {str(e)}")
            
            progress_bar.progress(1.0)
            progress_text.text("Question generation complete!")
            
            if all_questions:
                # Display generated questions
                st.header("📋 Generated Questions")
                
                # Group questions by type
                question_groups = {}
                for q in all_questions:
                    q_type = q.get('type', 'Unknown')
                    if q_type not in question_groups:
                        question_groups[q_type] = []
                    question_groups[q_type].append(q)
                
                # Display each group
                for q_type, questions in question_groups.items():
                    st.subheader(f"{q_type} Questions")
                    
                    for i, question in enumerate(questions, 1):
                        with st.container():
                            st.markdown(f"**Question {i}:** {question['question']}")
                            
                            if question['type'] == 'Multiple Choice' and 'options' in question:
                                for j, option in enumerate(question['options'], 1):
                                    st.markdown(f"   {chr(64+j)}. {option}")
                            
                            st.markdown(f"**Answer:** {question['answer']}")
                            st.divider()
                
                # Prepare downloadable content
                download_content = prepare_download_content(all_questions, uploaded_file.name)
                
                # Download button
                st.download_button(
                    label="💾 Download Questions as Text File",
                    data=download_content,
                    file_name=f"questions_{os.path.splitext(uploaded_file.name)[0]}.txt",
                    mime="text/plain"
                )
            else:
                st.error("No questions were generated. Please try again or check your document content.")

def prepare_download_content(questions, filename):
    """Prepare formatted content for download"""
    content = []
    content.append(f"Questions Generated from: {filename}")
    content.append("=" * 50)
    content.append("")
    
    # Group questions by type
    question_groups = {}
    for q in questions:
        q_type = q.get('type', 'Unknown')
        if q_type not in question_groups:
            question_groups[q_type] = []
        question_groups[q_type].append(q)
    
    # Format each group
    for q_type, questions in question_groups.items():
        content.append(f"{q_type} Questions")
        content.append("-" * 30)
        content.append("")
        
        for i, question in enumerate(questions, 1):
            content.append(f"Question {i}: {question['question']}")
            
            if question['type'] == 'Multiple Choice' and 'options' in question:
                for j, option in enumerate(question['options'], 1):
                    content.append(f"   {chr(64+j)}. {option}")
            
            content.append(f"Answer: {question['answer']}")
            content.append("")
        
        content.append("")
    
    return "\n".join(content)

if __name__ == "__main__":
    main()